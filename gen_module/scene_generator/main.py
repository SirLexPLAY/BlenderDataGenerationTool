# scene_generator/main.py
import bpy
import random
import math
from scene_generator_params import SceneGeneratorParams, PrimitiveObjects
from scene_generator.utils import (
    generate_random_height,
    create_random_plane, 
    create_random_box,
    create_random_cylinder,
    create_random_pyramid,
    is_aabb_overlapping_with_any_aabb,
    get_aabb)


class SceneGeneratorModule():

    NUMBER_OF_VERTICES = 32  # used by primitive_cylinder_add and primitive_cone_add


    def generate_scene(self, scene_params: SceneGeneratorParams):
        number_of_objs = random.randint(*scene_params.object_count_range)
        objects = [random.choice(list(scene_params.objects_to_generate)) for _ in range(number_of_objs)]
        object_params = []

        aabbs = []

        for obj in objects:
            a,b = scene_params.object_size_range
            location = [
                random.random()*scene_params.scene_size - scene_params.scene_size/2,  # x
                random.random()*scene_params.scene_size - scene_params.scene_size/2,  # y
                generate_random_height(*scene_params.object_height_distribution)      # z
            ]

            rotation = [random.random()*math.pi*2 for _ in range(3)]

            if obj.value == PrimitiveObjects.PLANE.value:
                size = create_random_plane(a, b, location, rotation)
                object_params.append({
                    "type": "plane",
                    "location": location,
                    "rotation": rotation,
                    "size": size
                })

            if obj.value == PrimitiveObjects.BOX.value:
                size = create_random_box(a, b, location, rotation)
                object_params.append({
                    "type": "box",
                    "location": location,
                    "rotation": rotation,
                    "size": size
                })

            elif obj.value == PrimitiveObjects.CYLINDER.value:
                radius, depth = create_random_cylinder(a, b, location, rotation, self.NUMBER_OF_VERTICES)
                object_params.append({
                    "type": "cylinder",
                    "location": location,
                    "rotation": rotation,
                    "radius": radius,
                    "depth": depth
                })

            else:
                vertices = 0
                if obj.value == PrimitiveObjects.CONE.value:
                    vertices = self.NUMBER_OF_VERTICES
                elif obj.value == PrimitiveObjects.TRIANGULAR_PYRAMID.value:
                    vertices = 3
                elif obj.value == PrimitiveObjects.RECTANGULAR_PYRAMID.value:
                    vertices = 4
                radius, depth = create_random_pyramid(a, b, location, rotation, vertices)

                object_params.append({
                    "type": "cylinder",
                    "location": location,
                    "rotation": rotation,
                    "radius": radius,
                    "depth": depth
                })

            obj = bpy.context.object
            obj_aabb = get_aabb(obj)
            if scene_params.allow_overlap: 
                aabbs.append(obj_aabb)
                continue

            if is_aabb_overlapping_with_any_aabb(obj_aabb, aabbs):
                obj.select = True
                bpy.ops.object.delete()
            else:
                aabbs.append(obj_aabb)
        return aabbs, object_params
    


    def clean_scene(self):
        """
        Removes all 3D objects.
        """

        # objects_to_delete = [obj for obj in bpy.context.scene.objects if obj.type not in {'CAMERA', 'LAMP'}]
        # bpy.ops.object.select_all(action='DESELECT')

        # for obj in objects_to_delete:
        #     obj.select = True
        # bpy.ops.object.delete()
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                bpy.data.objects.remove(obj, do_unlink=True)
    
