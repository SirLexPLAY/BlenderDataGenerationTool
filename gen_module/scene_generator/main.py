# scene_generator/main.py
import bpy
import random
from scene_generator_params import SceneGeneratorParams, PrimitiveObjects
from scene_generator.utils import (generate_random_height,
                   create_box,
                   create_cylinder,
                   create_pyramid,
                   is_aabb_overlapping_with_any_aabb,
                   get_aabb)


class SceneGenerator():

    NUMBER_OF_VERTICES = 32  # used by primitive_cylinder_add and primitive_cone_add
    

    def __init__(self):
        return


    def generate_scene(self, scene_params: SceneGeneratorParams):
        number_of_objs = random.randint(*scene_params.object_count_range)
        objects = [random.choice(list(scene_params.objects_to_generate)) for _ in range(number_of_objs)]

        aabbs = []

        for obj in objects:
            a,b = scene_params.object_size_range
            location = [
                random.random()*scene_params.scene_size - scene_params.scene_size/2,    # x
                random.random()*scene_params.scene_size - scene_params.scene_size/2,    # y
                generate_random_height(*scene_params.object_height_distribution)  # z
            ]

            if obj.value == PrimitiveObjects.BOX.value:
                create_box(a, b, location)
                
            elif obj.value == PrimitiveObjects.CYLINDER.value:
                create_cylinder(a, b, location, self.NUMBER_OF_VERTICES)

            else:
                vertices = 0
                if obj.value == PrimitiveObjects.CONE.value:
                    vertices = self.NUMBER_OF_VERTICES
                elif obj.value == PrimitiveObjects.TRIANGULAR_PYRAMID.value:
                    vertices = 3
                elif obj.value == PrimitiveObjects.RECTANGULAR_PYRAMID.value:
                    vertices = 4
                create_pyramid(a, b, location, vertices)

            if scene_params.allow_overlap: 
                continue

            obj = bpy.context.object
            obj_aabb = get_aabb(obj)
            if is_aabb_overlapping_with_any_aabb(obj_aabb, aabbs):
                obj.select = True
                bpy.ops.object.delete()
            else:
                aabbs.append(obj_aabb)
    

    
