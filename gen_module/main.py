# main.py

import os
import sys
import bpy
import numpy as np
import math
import mathutils
import time
import random

# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Append project to sys.path
project_root = os.path.abspath(os.path.join(script_dir, '.'))
sys.path.append(project_root)

# Append subfolders to sys.path
runtime_path = os.path.join(project_root, 'runtime')
sys.path.append(runtime_path)

scanner_path = os.path.join(project_root, 'scanner')
sys.path.append(scanner_path)

scene_generator_path = os.path.join(project_root, 'scene_generator')
sys.path.append(scene_generator_path)


from scanner import main as scanner_main
from scanner.scanner_params import ScannerParams
from scene_generator import main as scene_generator_main
from scene_generator.scene_generator_params import SceneGeneratorParams, PrimitiveObjects

def direction_to_rotation(direction):
    """
    Calculate rotation from direction vector.
    
    Args:
        direction (tuple): The direction vector.
    
    Returns:
        rotation: The rotation as a Quaternion.
    """
    direction_vector = mathutils.Vector(direction)
    rot_quat = direction_vector.to_track_quat('-Z', 'Y')  # -Z to point forward, Y to point upward by default
    return rot_quat


def animate_camera_circular(camera_obj, center=(0, 0, 0), radius=10, frames=250):
    """
    Animate the camera around a central point in a circular path.
    
    Args:
        camera_obj: The camera object to be animated.
        center (tuple): The central point around which the camera will move.
        radius (float): The radius of the circular path.
        frames (int): The total number of frames for a full circle.
    """
    for frame in range(frames):
        angle = (2 * math.pi * frame) / frames
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        z = center[2] + radius * math.sin(angle)/4  # Assuming a flat circular path
        
        camera_obj.location = (x, y, z)
        camera_obj.keyframe_insert(data_path="location", frame=frame)
        
        # Make the camera face the center point
        direction = (center[0] - x, center[1] - y, center[2] - z)
        rot_quat = direction_to_rotation(direction)
        camera_obj.rotation_euler = rot_quat.to_euler()
        camera_obj.keyframe_insert(data_path="rotation_euler", frame=frame)


def record(radius=10, frames=250, video_title=f"video.mp4"):
    camera_obj = bpy.data.objects["Camera"]
    animate_camera_circular(camera_obj, center=(0, 0, 0), radius=radius, frames=frames)

    # Set the frame range
    bpy.context.scene.frame_start = 0
    bpy.context.scene.frame_end = frames

    scene = bpy.context.scene
    render = scene.render


    # Set render resolution
    render.resolution_x = 1920
    render.resolution_y = 1080
    render.resolution_percentage = 100  # Scale percentage

    # Set output path and file format
    render.image_settings.file_format = 'FFMPEG'

    # Configure FFMPEG settings
    render.ffmpeg.format = 'MPEG4'
    render.ffmpeg.codec = 'H264'
    render.ffmpeg.audio_codec = 'AAC'
    render.ffmpeg.video_bitrate = 6000
    render.ffmpeg.audio_bitrate = 192
    render.ffmpeg.maxrate = 6000
    render.ffmpeg.minrate = 0
    render.ffmpeg.gopsize = 12
    render.ffmpeg.buffersize = 224


    # Set the output path for rendered frames
    render.filepath = f"/media/dawid/blensor data/jan2025/{video_title}"

    # Render the animation
    bpy.ops.render.render(animation=True)
    
def main():
    random.seed(2025)

    s = 10_000
    # f = open("/media/dawid/blensor data/run3/test.txt", "w")

    # 1 arg. 0.8[cm]/100[cm/m] = 0.008m (8mm), size of a 1x1 lego brick
    # 2 arg. 1m
    # 3 arg. 10 000 values
    object_sizes = np.linspace(0.8/100, 1, s)
    #bpy.ops.wm.read_factory_settings(use_empty=True)

    start_time = time.time()
    for n in range(5506, s):
        f = open(f"/media/dawid/blensor data/jan2025/test_{n}.txt", "w+")
        dirname = f"scanning{n}"
        dir = f"/media/dawid/blensor data/jan2025/{dirname}"
        os.makedirs(f"/media/dawid/blensor data/jan2025/{dirname}")
        obj_size = object_sizes[n]
        scene_size = obj_size*2.5
        ds = obj_size*0.5
        min_size = obj_size - ds
        max_size = obj_size + ds

        sg = scene_generator_main.SceneGeneratorModule()
        sg_params = SceneGeneratorParams(
            scene_size=scene_size,
            objects_to_generate={
                PrimitiveObjects.BOX,
                PrimitiveObjects.CONE,
                PrimitiveObjects.TRIANGULAR_PYRAMID,
                PrimitiveObjects.RECTANGULAR_PYRAMID,
                PrimitiveObjects.CYLINDER,
            },
            object_count_range=(5,8),
            object_size_range=(min_size, max_size),
            object_height_distribution=(0, scene_size/2),
            allow_overlap=True
        )

        sg.clean_scene()
        aabbs = sg.generate_scene(sg_params)
        
        #cam = bpy.data.objects.new("Camera", bpy.data.cameras.new("Camera"))
        #bpy.context.scene.objects.link(cam)
        #bpy.context.scene.camera = cam

        bpy.ops.wm.save_as_mainfile(filepath=f"{dir}/scene.blend")
        if n % 100 == 0:
            record(radius=scene_size*4, frames=100, video_title=f"scene_{n}.mp4")

        f.write(f"Scene: {n} at {time.time()-start_time:.2f}s\n")
        f.write(f"scene_size: {scene_size:.3f}\n")
        f.write(f"object_count_range: (5, 8)\n")
        f.write(f"object_size_range: ({min_size:.3f}, {max_size:.3f})\n")
        f.write(f"object_height_distribution: (0, {scene_size/2:.3f})\n")
        f.write(f"========================================================\n")
        f.close()
        
        scanner = bpy.data.objects["Camera"]
        sc = scanner_main.ScannerModule()
        sc_params = ScannerParams(
            scanner_object=scanner,
            scene_size=scene_size,
            frame_start=0,
            frame_end=200,
            min_angle=0,
            max_angle=180,
            add_noisy_blender_mesh=True
        )
        sc.scan_scene(sc_params, aabbs, dir=dir, filename="scan1.pcd")
        sc.scan_scene(sc_params, aabbs, dir=dir, filename="scan2.pcd")
        sc.scan_scene(sc_params, aabbs, dir=dir, filename="scan3.pcd")


    end_time = time.time()
    print("Total scan time: %.2f s"%(end_time-start_time))
    sys.exit(0)

if __name__ == "__main__":
    main()



# bpy.ops.wm.read_factory_settings(use_empty=True)
# # Explicitly clear all objects except the camera, if required.
# for obj in bpy.context.scene.objects:
#     if obj.type != 'CAMERA':
#         print(f"objtype: {obj.type}")
#         bpy.data.objects.remove(obj, do_unlink=True)
# cam = bpy.data.objects.new("Camera", bpy.data.cameras.new("Camera"))
# bpy.context.scene.objects.link(cam)
# bpy.context.scene.camera = cam