# scene_generator/utils.py

import random
import bpy
import mathutils

def generate_random_height(mean, std):
    """
    Generates a random height based on a specific mean and standard deviation.
    
    Parameters:
        mean (float or int): The mean value arounnd which the height is calculated.
        std (float or int): The standard deviation which defines the range for the random value.
    
    Returns:
        float: The generated random height.

    Raises:
        TypeError: If either 'mean' or 'std' is not a float or int.
    
    Example:
        >>> generate_random_height(170, 5)
        173.2  # This value vill vary as it is randomly generated.
    """
    if not (isinstance(mean, (float, int))):
        raise TypeError("mean must be a float or int.")
    if not (isinstance(std, (float, int))):
        raise TypeError("std must be a float or int.")
    
    return mean + random.uniform(-std, std)

def get_aabb(obj):
    """
    Calculates the Axis-Aligned Bounding Box (AABB) for a Blender object.

    Parameters:
        obj (bpy.types.Object): The Blender object for which the AABB is to be calculated.

    Returns:
        tuple: A pair of the mathutils.Vector representing the minimum and maximum coordinates for the AABB in world space.
    
    Notes:
        - This function ensures the scene is updated with bpy.context.scene.update() to reflect the latest transformations.
        - The @ operator is used for matrix multiplication to transform coordinates.
    """

    # Ensure the scene is updated
    bpy.context.scene.update()

    # Retrieve the bounding box corners in the object's local space
    local_bbox_corners = [mathutils.Vector(corner) for corner in obj.bound_box]

    # Transform the local coordinates to world coordinates using the object's matrix_world
    world_bbox_corners = [obj.matrix_world @ corner for corner in local_bbox_corners]

    # Determine the minimum and maximum coordinates for the AABB in world space
    min_corner = mathutils.Vector((min(corner.x for corner in world_bbox_corners),
                                   min(corner.y for corner in world_bbox_corners),
                                   min(corner.z for corner in world_bbox_corners)))
    max_corner = mathutils.Vector((max(corner.x for corner in world_bbox_corners),
                                   max(corner.y for corner in world_bbox_corners),
                                   max(corner.z for corner in world_bbox_corners)))
    
    return min_corner, max_corner