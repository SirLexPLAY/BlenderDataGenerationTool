# main.py

import os
import sys
import bpy

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

def main():
    scene_size = 10

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
        object_size_range=(2.0,4.0),
        object_height_distribution=(0, 2),
        allow_overlap=True
    )

    sg.clean_scene()
    sg.generate_scene(sg_params)

    scanner = bpy.data.objects["Camera"]

    sc = scanner_main.ScannerModule()
    sc_params = ScannerParams(
        scanner_object=scanner,
        scene_size=scene_size,
        frame_start=0,
        frame_end=100,
        min_angle=0,
        max_angle=180,
        add_noisy_blender_mesh=True
    )
    sc.scan_scene(sc_params)

    # sys.exit(0)

if __name__ == "__main__":
    main()


