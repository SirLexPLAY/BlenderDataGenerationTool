# scene_generator/utils.py

import random
import bpy
import mathutils

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

