# scanner/utils.py

import bpy
import blensor
import random
from math import pi


def keyframe_setup(scanner_object, frame_start, frame_end, min_angle, max_angle):
    """
    #TODO: needs to be properly documented

    This method sets up the keyframes so that the scans can be done properly,
    like in the case of a VLP-16 scanner, where there is empty space in between
    the 16 angles, and also the scann range is limited.
    """
    scanner_object.animation_data_clear()

    scanner_object.rotation_euler = (min_angle/180*pi, 0, 0)
    scanner_object.keyframe_insert(data_path="rotation_euler", frame=frame_start)

    scanner_object.rotation_euler = (max_angle/180*pi, 0, 0)
    scanner_object.keyframe_insert(data_path="rotation_euler", frame=frame_end)


def camera_setup(scanner_object: bpy.types.Object, scene_size: float, aabbs):
    
    isTrapped = True
    while isTrapped:
        location = [
                    random.random()*scene_size - scene_size/2,  # x
                    random.random()*scene_size - scene_size/2,  # y
                    random.random()*scene_size - scene_size/2   # z
                ]
        
        is_inside_any_aabb = False

        for aabb in aabbs:
            min_aabb = aabb[0]
            max_aabb = aabb[1]

            # Check if cam location is inside or outside the AABB
            greater_than_min = min_aabb[0] <= location[0] and min_aabb[1] <= location[1] and min_aabb[2] <= location[2]
            smaller_than_max = max_aabb[0] >= location[0] and max_aabb[1] >= location[1] and max_aabb[2] >= location[2]

            # The check. If it's inside one object, new location must be picked.
            # Leave the loop.
            if greater_than_min and smaller_than_max:
                is_inside_any_aabb = True
                break

        # If no test from above was positive, we have found a good camera location.
        if not is_inside_any_aabb:
            scanner_object.location = location
            isTrapped = False

"""
vlp16_parameters = {
    "angle_resolution": 0.1,  # Page 52
    "rotation_speed": 5,      # Page 52 # in Hz, equivalent to 300 RPM
    "max_dist": 100,          # Page could not be found
    "noise_mu": 0.0,          
    "noise_sigma": 0.01,
    "start_angle": 0,
    "end_angle": 360,
    "distance_bias_noise_mu": 0,
    "distance_bias_noise_sigma": 0.014,
    "reflectivity_distance": 50,
    "reflectivity_limit": 0.1,
    "reflectivity_slope": 0.01,
    "noise_types": [("gaussian", "Gaussian", "Gaussian distribution (mu/simga)"),
                    ("laplace", "Laplace", "Laplace distribution (sigma=b)")],
    
}


"models": [(BLENSOR_VELODYNE_HDL64E2, "HDL-64E2", "HDL-64E2"), (BLENSOR_VELODYNE_HDL32E, "HDL-32E", "HDL-32E"),
               (BLENSOR_VELODYNE_VLP16, "VLP-16", "VLP-16")]
"""


def scan_range(scanner_object, frame_start, frame_end, dir, file_name, add_blender_mesh=False, add_noisy_blender_mesh=False):
    """
    #TODO: needs to be properly documented

    Performs the scan, but it should be considered to remove this method if it
    only calls a method passing the parameters directly without any modification on them.
    """
    scanner_object.velodyne_model = "vlp16"
    
    blensor.blendodyne.scan_range(
        scanner_object=scanner_object,
        frame_start=frame_start,
        frame_end=frame_end,
        add_blender_mesh=add_blender_mesh,
        add_noisy_blender_mesh=add_noisy_blender_mesh,
        world_transformation=scanner_object.matrix_world,

        angle_resolution=0.1,
        rotation_speed=5,
        max_distance=100,
        noise_mu=0.0,
        noise_sigma=0.1,
        depth_map=True,
        filename=f"{dir}/{file_name}"
    ) 
    """
    Other possible parameters:
    - filename="/tmp/landscape.evd",
    - frame_time = (1.0/24.0),
    - rotation_speed = 10.0,
    - angle_resolution = 0.1728,
    [-] max_distance = 120.0,
    [-] noise_mu = 0.0,      
    [-] noise_sigma= 0.02,
    - last_frame = True,
    - output_laser_id_as_color=False,
    - add_beam_divergence=False,
    - use_incidence_angle=False,
    - depth_map=False
    """


def render_image(filepath, fileformat, engine="CYCLES"):
    """
    #TODO: needs to be properly documented

    Maybe not necessary the same way as the scan_range method.
    It just renders the image of the cameras exact position (num 0 for preview).

    Might consider adding some more functionality:
    - whether the image should be taken outside the boundary box of objects
    - set the location of the camera to some input location, or
        - something more convinient; take an arbitrary position, see if the objects
          are more or less covered by the cameras range of sight - if not, adjust
          positions and angles, then render the image.
    """
    bpy.context.scene.render.engine = engine
    bpy.context.scene.render.filepath = filepath
    bpy.context.scene.render.image_settings.file_format = fileformat
    bpy.ops.render.render(write_still=True)


def is_camera_trapped(cam_location, aabbs):
    for aabb in aabbs:
            min_aabb = aabb[0]
            max_aabb = aabb[1]

            greater_than_min = min_aabb[0] <= location[0] and min_aabb[1] <= location[1] and min_aabb[2] <= location[2]
            smaller_than_max = max_aabb[0] >= location[0] and max_aabb[1] >= location[1] and max_aabb[2] >= location[2]

            if greater_than_min and smaller_than_max:
                continue
            else:
                isTrapped = False
                break