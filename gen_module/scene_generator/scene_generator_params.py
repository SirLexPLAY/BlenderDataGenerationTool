from dataclasses import dataclass, field
from typing import List, Tuple
from enum import Enum

class PrimitiveObjects(Enum):
    BOX = "box"
    CONE = "cone"
    TRIANGULAR_PYRAMID = "triangular_pyramid"
    RECTANGULAR_PYRAMID = "rectangular_pyramid"
    CYLINDER = "cylinder"

@dataclass(frozen=True)
class SceneGeneratorParams:
    scene_size: List[float]
    objects_to_generate: List[PrimitiveObjects]
    object_count_range: Tuple[int, int]
    object_size_range: Tuple[float, float]
    object_height_distribution: Tuple[float, float]
    allow_overlap: bool

    def __post_init__(self):
        # Validate scene_size
        if not isinstance(self.scene_size, list):
            raise TypeError(f"'scene_size' expected to be of type list, but got {type(self.scene_size).__name__}")
        if len(self.scene_size) not in [1, 3]:
            raise ValueError(f"'scene_size' must be of length 1 or 3. Got length {len(self.scene_size)}")
        if not all(isinstance(n, (float, int)) and n > 0 for n in self.scene_size):
            raise ValueError(f"All elements in 'scene_size' must be positive numbers (float or int). Got {self.scene_size}")
        
        # Validate objects_to_generate
        if not isinstance(self.objects_to_generate, list):
            raise TypeError(f"'objects_to_generate' expected to be of type list, but got {type(self.objects_to_generate).__name__}")
        if not self.objects_to_generate:
            raise ValueError(f"'objects_to_generate' cannot be empty")
        if not all(isinstance(obj, PrimitiveObjects) for obj in self.objects_to_generate):
            raise ValueError(f"All elements in 'objects_to_generate' must be instances of PrimitiveObjects. Got {self.objects_to_generate}")

        # Validate object_count_range
        if not isinstance(self.object_count_range, tuple):
            raise TypeError(f"'object_count_range' expected to be of type tuple, but got {type(self.object_count_range).__name__}")
        if len(self.object_count_range) != 2:
            raise ValueError(f"'object_count_range' must be of length 2. Got length {len(self.object_count_range)}")
        if not all(isinstance(n, int) for n in self.object_count_range):
            raise TypeError(f"All elements in 'object_count_range' must be integers. Got {self.object_count_range}")
        if self.object_count_range[0] > self.object_count_range[1] or self.object_count_range[0] < 0:
            raise ValueError(f"First element of 'object_count_range' must be non-negative and not greater than the second. Got {self.object_count_range}")
        
        # Validate object_size_range
        if not isinstance(self.object_size_range, tuple):
            raise TypeError(f"'object_size_range' expected to be of type tuple, but got {type(self.object_size_range).__name__}")
        if len(self.object_size_range) != 2:
            raise ValueError(f"'object_size_range' must be of length 2. Got length {len(self.object_size_range)}")
        if not all(isinstance(n, (float, int)) for n in self.object_size_range):
            raise TypeError(f"All elements in 'object_size_range' must be numbers (float or int). Got {self.object_size_range}")
        if self.object_size_range[0] > self.object_size_range[1] or self.object_size_range[0] < 0:
            raise ValueError(f"First element of 'object_size_range' must be non-negative and not greater than the second. Got {self.object_size_range}")

        # Validate object_height_distribution
        if not isinstance(self.object_height_distribution, tuple):
            raise TypeError(f"'object_height_distribution' expected to be of type tuple, but got {type(self.object_height_distribution).__name__}")
        if len(self.object_height_distribution) != 2:
            raise ValueError(f"'object_height_distribution' must be of length 2. Got length {len(self.object_height_distribution)}")
        if not all(isinstance(n, (float, int)) for n in self.object_height_distribution):
            raise TypeError(f"All elements in 'object_height_distribution' must be numbers (float or int). Got {self.object_height_distribution}")
        
        # Validate allow_overlap
        if not isinstance(self.allow_overlap, bool):
            raise TypeError(f"'allow_overlap' expected to be of type bool, but got {type(self.allow_overlap).__name__}")

