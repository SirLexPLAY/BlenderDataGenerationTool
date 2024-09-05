# Use of Maximum Attempts When Drawing Objects

Consider an arbitrary scene generator configuration (where overlaps are not allowed), and a situation, where an object failed to be drawn. There are some things to bear in mind:

- Retry drawing the object in different position;
  - if succeed, then there is no problem.
- What if the scene is mostly filled with bounding boxes?
  - we might end up in an endeless loop, especially if it is impossible to fit the new object without breaking the size constictions.
- A possible solution;
  - define an integer $n$ for number of maximum attempts - try drawing the object with $n$ different parameters (one could only include position, but also other parameters like size) $n$ times.
  - If failed $n$ times, then either stop generating the scene, or keep on with the next object (the last case would be a little like expanding the number for maximum attempts).
