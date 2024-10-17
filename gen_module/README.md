# Genmodule Doc

## Generating 10 000 date set parameters

### Scene gen params

- `object_size`
  - starting at 0.008m (8mm) which is size of a 1x1 Lego brick
  - ending at 1m
  - 10 000 values
- `scene_size`
  - should be proportional to size of objects
  - suggestion: 50 times bigger than object size?
- `objects_to_generate`
  - all primitive objects
- `object_count_range`
  - range of objects, or a specific number of objects everytime?
  - maybe 10 is ok?
- `object_height_distribution`
  - average at middle Z-value
  - deviation over entire box
- `allow_object_overlap`
  - set to `true`

### Scanning params

- `Scanning Angle Range`
  - from 0 degree to 180 degrees
- `Height Density`
  - the slower the better
- `Number of Rotations`
  - one is enough

### Render params

- for 1% of data
  - every 100th scene
  - starting at 1st scene
  - 100 rendered videoes and 300 rendered images
