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


from runtime import main as runtime_main
from scanner import main as scanner_main
from scene_generator import main as scene_generator_main
from scene_generator.scene_generator_params import SceneGeneratorParams, PrimitiveObjects

def main():
    # read system parameters
    print("this works!")

    sg = scene_generator_main.SceneGenerator()
    sg_params = SceneGeneratorParams(
        scene_size=10,
        objects_to_generate={
            PrimitiveObjects.BOX,
            PrimitiveObjects.CONE,
            PrimitiveObjects.TRIANGULAR_PYRAMID,
            PrimitiveObjects.RECTANGULAR_PYRAMID,
            PrimitiveObjects.CYLINDER,
        },
        object_count_range=(5,8),
        object_size_range=(2.0,4.0),
        object_height_distribution=(5, 2),
        allow_overlap=True
    )


    sg.generate_scene(sg_params)



    # sys.exit(0)

if __name__ == "__main__":
    main()


