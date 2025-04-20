# scene_generator/utils.py

import random
import bpy
from mathutils import Vector
from enum import Enum


class OverlapResult(Enum):
    COMPLETE_OVERLAP = 1
    PARTIAL_OVERLAP = 0
    NO_OVERLAP = -1


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
    local_bbox_corners = [Vector(corner) for corner in obj.bound_box]

    # Transform the local coordinates to world coordinates using the object's matrix_world
    world_bbox_corners = [obj.matrix_world * corner for corner in local_bbox_corners]

    # Determine the minimum and maximum coordinates for the AABB in world space
    min_corner = Vector((
        min(corner.x for corner in world_bbox_corners),
        min(corner.y for corner in world_bbox_corners),
        min(corner.z for corner in world_bbox_corners)
    ))
    max_corner = Vector((
        max(corner.x for corner in world_bbox_corners),
        max(corner.y for corner in world_bbox_corners),
        max(corner.z for corner in world_bbox_corners)
    ))
    
    return min_corner, max_corner


def are_two_aabbs_overlapping(aabb_1, aabb_2):
    """
    Checks if two Axis-Aligned Bounding Boxes (AABBs) are overlapping.

    Parameters:
        aabb_1 (tuple): A pair of min_corner (mathutils.Vector) and max_corner (mathutils.Vector) for the first AABB.
        aabb_2 (tuple): A pair of min_corner (mathutils.Vector) and max_corner (mathutils.Vector) for the second AABB.
    
    Returns:
        OverlapResult: The overlap status:
            - OverlapResult.COMPLETE_OVERLAP: One AABB is completely within the other
            - OverlapResult.PARTIAL_OVERLAP: The AABBs partly overlap
            - OverlapResult.NO_OVERLAP: No overlap

    Example:
        >>> aabb_1 = (mathutils.Vector((0, 0, 0)), mathutils.Vector((1, 1, 1)))
        >>> aabb_2 = (mathutils.Vector((0.5, 0.5, 0.5)), mathutils.Vector((1.5, 1.5, 1.5)))
        >>> are_aabbs_overlapping(aabb_1, aabb_2)
        OverlapResult.PARTIAL_OVERLAP
    
    Notes:
        - For both cases of complete and no overlap, inclusive inequalities are
          used (>= and <=), as for all cases faces are allowed to touch each other.
    """
    o1_min = aabb_1[0]
    o1_max = aabb_1[1]
    o2_min = aabb_2[0]
    o2_max = aabb_2[1]

    # In case of complete overlap
    is_o1_contained_in_o2 = (all(a_coord >= b_coord for a_coord, b_coord in zip(o1_min, o2_min)) and
                          all(a_coord <= b_coord for a_coord, b_coord in zip(o1_max, o2_max)))
    is_o2_contained_in_o1 = (all(a_coord >= b_coord for a_coord, b_coord in zip(o2_min, o1_min)) and
                          all(a_coord <= b_coord for a_coord, b_coord in zip(o2_max, o1_max)))
    
    if (is_o1_contained_in_o2 or is_o2_contained_in_o1): 
        return OverlapResult.COMPLETE_OVERLAP

    # In case of no overlap
    if (o1_max.x <= o2_min.x or o1_min.x >= o2_max.x or
        o1_max.y <= o2_min.y or o1_min.y >= o2_max.y or
        o1_max.z <= o2_min.z or o1_min.z >= o2_max.z): 
        return OverlapResult.NO_OVERLAP
    
    # Otherwise there is partial overlap
    return OverlapResult.PARTIAL_OVERLAP


def is_aabb_overlapping_with_any_aabb(in_aabb, drawn_aabbs):
    for aabb in drawn_aabbs:
        result = are_two_aabbs_overlapping(in_aabb, aabb)
        if result.value == OverlapResult.PARTIAL_OVERLAP.value or result.value == OverlapResult.COMPLETE_OVERLAP.value:
            return True
    return False


def create_random_plane(a, b, location, rotation):
    radius = (random.random()*(b-a)+a)/2
    bpy.ops.mesh.primitive_plane_add(
        radius=radius,
        location=location,
        rotation=rotation
    )

    return radius


def create_random_box(a, b, location, rotation):
    size = [random.random()*(b-a)+a for _ in range(3)]
    bpy.ops.mesh.primitive_cube_add(
        location=location,
        rotation=rotation
    )
    box = bpy.context.object
    box.scale[0] = size[0] / 2.0
    box.scale[1] = size[1] / 2.0
    box.scale[2] = size[2] / 2.0

    return size


def create_random_sphere(a, b, location):
    size = (random.random()*(b-a)+a)/2
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=64, 
        ring_count=64, 
        size=size, 
        location=location
    )

    return size
    

def create_random_cylinder(a, b, location, rotation, vertices):
    radius = (random.random()*(b-a)+a)/2
    depth = random.random()*(b-a)+a

    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius,
        depth=depth,
        vertices=vertices,
        location=location,
        rotation=rotation
    )

    return radius, depth


def create_random_pyramid(a, b, location, rotation, vertices):
    radius = (random.random()*(b-a)+a)/2
    depth = random.random()*(b-a)+a

    bpy.ops.mesh.primitive_cone_add(
        radius1=radius,
        depth=depth,
        vertices=vertices,
        location=location,
        rotation=rotation
    )

    return radius, depth
