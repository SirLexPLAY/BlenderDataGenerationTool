# scene_generator/tests/test_utils.py

import unittest
from mathutils import Vector
from scene_generator import utils
from enum import Enum
import gc


class TestVectors(Enum):
    """
    Enum class representing translation vectors for testing the 
    translation invariance of Axis-Aligned Bounding Box (AABB) 
    overlap detection.

    Each vector shifts AABBs to validate that the overlap detection 
    algorithm produces consistent results regardless of global position.
    """

    VECTOR1 = Vector((100, 0, 0))
    VECTOR2 = Vector((0, 100, 0))
    VECTOR3 = Vector((0, 0, 100))
    VECTOR4 = Vector((100, 100, 0))
    VECTOR5 = Vector((0, 100, 100))
    VECTOR6 = Vector((100, 0, 100))
    VECTOR7 = Vector((100, 100, 100))
    VECTOR8 = Vector((-100, 0, 0))
    VECTOR9 = Vector((0, -100, 0))
    VECTOR10 = Vector((0, 0, -100))
    VECTOR11 = Vector((-100, -100, -100))
    VECTOR12 = Vector((1e6, 1e6, 1e6))
    VECTOR13 = Vector((-1e6, -1e6, -1e6))
    VECTOR14 = Vector((1e-6, 1e-6, 1e-6))
    VECTOR15 = Vector((-1e-6, -1e-6, -1e-6))


class TestAreAABBsOverlapping(unittest.TestCase):
    """
    Notes:
        - Some test cases have been generated with help of ChatGPT 4.0 Omni
          in order to get good coverage of edge cases.
    """

    def test_complete_overlap(self):
        """
        Cases to test:
            - One AABB entirely inside another
            - Aligned but within (both min-points start at the same point)
            - Different sizes and positions
        """

        o1 = [Vector((3, 3, 3)), Vector((7, 8, 9))]
 
        o2 = [Vector((4, 5, 5)), Vector((6, 6, 7))] # Is inside o1, no touching
        o3 = [Vector((3, 3, 3)), Vector((6, 6, 7))] # Has common min-point with o1
        o4 = [Vector((6.2, 4.4, 4.6)), Vector((6.4, 7.6, 6.8))] # Is inside o1, different size, no touching

        objs = [o2, o3, o4]
        
        self._compare_aabbs(o1, objs, utils.OverlapResult.COMPLETE_OVERLAP)

    def test_no_overlap(self):
        """
        Cases to test:
            - Completely separate in all dimensions
            - Very close but not touching
            - Different sizes and positions
        """


        o1 = [Vector((3, 3, 3)), Vector((4, 4, 4))]
 
        o2 = [Vector((15, 15, 15)), Vector((16, 16, 16))] # Completely seperated from o1 in all dims
        o3 = [Vector((3, 3, 1)), Vector((3, 3, 2.9))]     # Very close o1 but not touching 
        o4 = [Vector((1, 1, 1)), Vector((2, 2, 2))]       # Smaller and far from o1
        o5 = [Vector((10, 10, 10)), Vector((20, 20, 20))] # Significantly larger and far from o
        o6 = [Vector((5, 5, 5)), Vector((6, 8, 10))]      # Different aspect ratio, no overlap
        o7 = [Vector((2.8, 2.8, 2.8)), Vector((2.9, 2.9, 2.9))] # o7 small gap with o1


        objs = [o2, o3, o4, o5, o6, o7]
        
        self._compare_aabbs(o1, objs, utils.OverlapResult.NO_OVERLAP)

    def test_partial_overlap(self):
        """
        Cases to test:
            - When a corner is inside another AABB
            - When one face is completely inside another AABB
            - When an edge is partially inside another AABB
            - Different placements
        """

        o1 = [Vector((3, 3, 3)), Vector((7, 8, 9))]

        o2 = [Vector((2, 2, 2)), Vector((3.5, 3.5, 3.5))] # Max_point inside o1
        o3 = [Vector((1, 3, 3)), Vector((4, 8, 9))]       # yz-plane with max corner entirely inside o1
        o4 = [Vector((6, 2, 2)), Vector((8, 7, 7))]       # Edge partially inside o1
        o5 = [Vector((5, 5, 5)), Vector((10, 10, 10))]    # Diagonal partial overlap
        o6 = [Vector((2, 2, 2)), Vector((6, 4, 4))]       # Complex partial overlap
        objs = [o2, o3, o4, o5, o6]
        
        self._compare_aabbs(o1, objs, utils.OverlapResult.PARTIAL_OVERLAP)

    def test_touching_edges(self):
        """
        Cases to test:
            - Touching edges exactly, but no overlap
            - Touching at a corner, but no overlap
            - Touching faces, but no overlap
        """

        o1 = [Vector((3, 3, 3)), Vector((7, 8, 9))]
 
        o2 = [Vector((3, 1, 1)), Vector((7, 3, 3))] # Touches the edge exactly
        o3 = [Vector((1, 1, 1)), Vector((3, 3, 3))] # Touches the corner exactly
        o4 = [Vector((3, 1, 3)), Vector((7, 3, 9))] # Touches the face exactly

        objs = [o2, o3, o4]
        
        self._compare_aabbs(o1, objs, utils.OverlapResult.NO_OVERLAP)

    def test_exactly_equal_aabbs(self):
        """
        Cases to test:
            - Identically positioned and sized AABBs
        """

        o1 = [Vector((3, 3, 3)), Vector((7, 8, 9))]
 
        o2 = [Vector((3, 3, 3)), Vector((7, 8, 9))]

        objs = [o2]
        
        self._compare_aabbs(o1, objs, utils.OverlapResult.COMPLETE_OVERLAP)

    def _compare_aabbs(self, ref_aabb, aabbs, expected_results):
        for ob in aabbs:
            result = utils.are_aabbs_overlapping(ref_aabb, ob)
            self.assertEqual(result, expected_results, f"\nob: {ob}, \nref: {ref_aabb}")

            for shift in TestVectors:
                ob_shifted = shift_aabb(ob, shift.value)
                ref_shifted = shift_aabb(ref_aabb, shift.value)
                result = utils.are_aabbs_overlapping(ref_shifted, ob_shifted)
                self.assertEqual(result, expected_results, f"\nShifted ob: {ob_shifted}, \nref: {ref_shifted}, \nshift: {shift}")
        

def shift_aabb(aabb, shift):
    return [aabb[0]+shift, aabb[1]+shift]


if __name__ == '__main__':
    unittest.main(verbosity=2, exit=False)
