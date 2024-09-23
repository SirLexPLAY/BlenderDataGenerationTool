# scanner/utils.py

import bpy
import blensor
from math import pi


def keyframe_setup(scanner_object, frame_start, frame_end, angle_start, angle_end):
    """
    #TODO: needs to be properly documented

    This method sets up the keyframes so that the scans can be done properly,
    like in the case of a VLP-16 scanner, where there is empty space in between
    the 16 angles, and also the scann range is limited.
    """
    scanner_object.animation_data_clear()

    scanner_object.rotation_euler = (angle_start, 0, 0)
    scanner_object.keyframe_insert(data_path="rotation_euler", frame=frame_start)

    scanner_object.rotation_euler = (angle_end, 0, 0)
    scanner_object.keyframe_insert(data_path="rotation_euler", frame=frame_end)


def scan_range(scanner, frame_start, frame_end, add_blender_mesh=False, add_noisy_blender_mesh=False):
    """
    #TODO: needs to be properly documented

    Performs the scan, but it should be considered to remove this method if it
    only calls a method passing the parameters directly without any modification on them.
    """
    
    blensor.blendodyne.scan_range(
        scanner_object=scanner,
        frame_start=frame_start,
        frame_end=frame_end,
        add_blender_mesh=add_blender_mesh,
        add_noisy_blender_mesh=add_noisy_blender_mesh
    )


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
