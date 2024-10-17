# scanner/main.py
import bpy
from scanner.utils import keyframe_setup, camera_setup, scan_range
from scanner.scanner_params import ScannerParams


class ScannerModule:

    def scan_scene(self, scanner_params: ScannerParams, dir: str, filename: str, numer_of_scans: int = 1):
        camera_setup(
            scanner_params.scanner_object, 
            scanner_params.scene_size
            )
        keyframe_setup(
            scanner_params.scanner_object, 
            scanner_params.frame_start, 
            scanner_params.frame_end, 
            scanner_params.max_angle, 
            scanner_params.min_angle
            )
        scan_range(
            scanner_params.scanner_object, 
            scanner_params.frame_start, 
            scanner_params.frame_end,
            dir,
            filename,
            add_noisy_blender_mesh=scanner_params.add_noisy_blender_mesh,
            )
        