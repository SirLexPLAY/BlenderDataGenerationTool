from typing import Tuple, Set
from enum import Enum
from system_parameters import SystemConfiguration

config = SystemConfiguration()
PrimitiveObjects = Enum('PrimitiveObjects', config.get("primitive_objects"))


class SceneGeneratorParams:
    
    def __init__(
            self,
            scene_size: float,
            objects_to_generate: Set[PrimitiveObjects],
            object_count_range: Tuple[int, int],
            object_size_range: Tuple[float, float],
            object_height_distribution: Tuple[float, float],
            allow_overlap: bool,
    ):
        self._scene_size = scene_size
        self._objects_to_generate = objects_to_generate
        self._object_count_range = object_count_range
        self._object_size_range = object_size_range
        self._object_height_distribution = object_height_distribution
        self._allow_overlap = allow_overlap


    @property
    def scene_size(self):
        return self._scene_size


    @scene_size.setter
    def scene_size(self, value):
        # Validate scene_size
        if not isinstance(value, (float, int)):
            raise TypeError(f"'scene_size' expected to be of type float, but got {type(value).__name__}")
        if not value > 0:
            raise ValueError(f"'scene_size' must be a positive number (float or int). Got {value}")
        self._scene_size = value


    @property
    def objects_to_generate(self):
        return self._objects_to_generate


    @objects_to_generate.setter
    def objects_to_generate(self, value):
        # Validate objects_to_generate
        if not isinstance(value, set):
            raise TypeError(f"'objects_to_generate' expected to be of type set, but got {type(value).__name__}")
        if not value:
            raise ValueError(f"'objects_to_generate' cannot be empty")
        if not all(isinstance(obj, PrimitiveObjects) for obj in value):
            raise ValueError(f"All elements in 'objects_to_generate' must be instances of PrimitiveObjects. Got {value}")
        self._objects_to_generate = value


    @property
    def object_count_range(self):
        return self._object_count_range


    @object_count_range.setter
    def object_count_range(self, value):
        # Validate object_count_range
        if not isinstance(value, tuple):
            raise TypeError(f"'object_count_range' expected to be of type tuple, but got {type(value).__name__}")
        if len(value) != 2:
            raise ValueError(f"'object_count_range' must be of length 2. Got length {len(value)}")
        if not all(isinstance(n, int) for n in value):
            raise TypeError(f"All elements in 'object_count_range' must be integers. Got {value}")
        if value[0] > value[1] or value[0] < 0:
            raise ValueError(f"First element of 'object_count_range' must be non-negative and not greater than the second. Got {value}")
        self._object_count_range = value


    @property
    def object_size_range(self):
        return self._object_size_range


    @object_size_range.setter
    def object_size_range(self, value):
        # Validate object_size_range
        if not isinstance(value, tuple):
            raise TypeError(f"'object_size_range' expected to be of type tuple, but got {type(value).__name__}")
        if len(value) != 2:
            raise ValueError(f"'object_size_range' must be of length 2. Got length {len(value)}")
        if not all(isinstance(n, (float, int)) for n in value):
            raise TypeError(f"All elements in 'object_size_range' must be numbers (float or int). Got {value}")
        if value[0] > value[1] or value[0] < 0:
            raise ValueError(f"First element of 'object_size_range' must be non-negative and not greater than the second. Got {value}")
        self._object_size_range = value

    @property
    def object_height_distribution(self):
        return self._object_height_distribution


    @object_height_distribution.setter
    def object_height_distribution(self, value):
        # Validate object_height_distribution
        if not isinstance(value, tuple):
            raise TypeError(f"'object_height_distribution' expected to be of type tuple, but got {type(value).__name__}")
        if len(value) != 2:
            raise ValueError(f"'object_height_distribution' must be of length 2. Got length {len(value)}")
        if not all(isinstance(n, (float, int)) for n in value):
            raise TypeError(f"All elements in 'object_height_distribution' must be numbers (float or int). Got {value}")
        self._object_height_distribution = value


    @property
    def allow_overlap(self):
        return self._allow_overlap


    @allow_overlap.setter
    def allow_overlap(self, value):
        # Validate allow_overlap
        if not isinstance(value, bool):
            raise TypeError(f"'allow_overlap' expected to be of type bool, but got {type(value).__name__}")
        self._allow_overlap = value
