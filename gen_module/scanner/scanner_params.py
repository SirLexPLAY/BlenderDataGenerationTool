# scanner/scanner_params.py

import bpy


class ScannerParams:

    def __init__(
            self,
            scanner_object: bpy.types.Object,
            scene_size: float,
            frame_start: int,
            frame_end: int,
            min_angle: float,
            max_angle: float,
            add_blender_mesh: bool = False,
            add_noisy_blender_mesh: bool = False,
            render_filepath: str = "",
            render_fileformat: str = "",
            render_engine: str = "CYCLES"
    ):
        self.scanner_object = scanner_object
        self.scene_size = scene_size
        self.frame_start = frame_start
        self.frame_end = frame_end
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.add_blender_mesh = add_blender_mesh
        self.add_noisy_blender_mesh = add_noisy_blender_mesh
        self.render_filepath = render_filepath
        self.render_fileformat = render_fileformat
        self.render_engine = render_engine


    @property
    def scene_size(self):
        return self._scene_size


    @scene_size.setter
    def scene_size(self, value):
        # Validate scene_size
        if not isinstance(value, (float, int)):
            raise TypeError(f"'scene_size' must be a number.")
        if not value > 0:
            raise ValueError(f"'scene_size' {value} must be a positive number.")
        self._scene_size = value


    @property
    def scanner_object(self):
        return self._scanner_object
    

    @scanner_object.setter
    def scanner_object(self, value):
        self._scanner_object = value


    @property
    def frame_start(self):
        return self._frame_start


    @frame_start.setter
    def frame_start(self, value):
        if not isinstance(value, int):
            raise TypeError("frame_start must be an integer.")
        if hasattr(self, '_frame_end'):
            if value >= self._frame_end:
                raise ValueError(f"Provided frame_start ({value}) can't be equal to or bigger than frame_end ({self._frame_end})!")
        self._frame_start = value
        
    
    @property
    def frame_end(self):
        return self._frame_end
    

    @frame_end.setter
    def frame_end(self, value):
        if not isinstance(value, int):
            raise TypeError("frame_end must be an integer.")
        if hasattr(self, '_frame_start'):
            if value <= self._frame_start:
                raise ValueError(f"Provided frame_end ({value}) can't be equal to or lower than frame_start ({self._frame_start})!")
        self._frame_end = value
    

    @property
    def min_angle(self):
        return self._min_angle

    
    @min_angle.setter
    def min_angle(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("min_angle must be a number.")
        if hasattr(self, '_max_angle'):
            if value >= self._max_angle:
                raise ValueError(f"Provided min_angle ({value}) can't be equal to or higher than max_angle ({self._max_angle})!")
        if value < 0 or value > 180:
            raise ValueError(f"Provided min_angle ({value}) must be between 0 and 180 (inclusive).")
        self._min_angle = value


    @property
    def max_angle(self):
        return self._max_angle

    
    @max_angle.setter
    def max_angle(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("max_angle must be a number.")
        if hasattr(self, '_min_angle'):
            if value <= self._min_angle:
                raise ValueError(f"Provided max_angle ({value}) can't be equal to or lower than min_angle ({self._min_angle})!")
        if value < 0 or value > 180:
            raise ValueError(f"Provided max_angle ({value}) must be between 0 and 180 (inclusive).")
        self._max_angle = value
    

    @property
    def add_blender_mesh(self):
        return self._add_blender_mesh
    

    @add_blender_mesh.setter
    def add_blender_mesh(self, value):
        if not isinstance(value, bool):
            raise TypeError("add_blender_mesh must be a bool.")
        self._add_blender_mesh = value


    @property
    def add_noisy_blender_mesh(self):
        return self._add_noisy_blender_mesh


    @add_noisy_blender_mesh.setter
    def add_noisy_blender_mesh(self, value):
        if not isinstance(value, bool):
            raise TypeError("add_noisy_blender_mesh must be a bool.")
        self._add_noisy_blender_mesh = value


    @property
    def render_filepath(self):
        return self._render_filepath


    @render_filepath.setter
    def render_filepath(self, value):
        if not isinstance(value, str):
            raise TypeError("render_filepath must be a str.")
        self._render_filepath = value
    

    @property
    def render_fileformat(self):
        return self._render_fileformat


    @render_fileformat.setter
    def render_fileformat(self, value):
        if not isinstance(value, str):
            raise TypeError("render_fileformat must be a str.")
        self._render_fileformat = value
    

    @property
    def render_engine(self):
        return self._render_engine


    @render_engine.setter
    def render_engine(self, value):
        if not isinstance(value, str):
            raise TypeError("render_engine must be a str.")
        self._render_engine = value

