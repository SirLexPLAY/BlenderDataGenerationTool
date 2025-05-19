# Preview Arguments for Dataset Generator + Link to YT Playlist
https://www.youtube.com/playlist?list=PLP4Tc-iAHsng3xjIUkFZq-K6WF5E0jmRj

## Scene Generator Settings
```
scene_size: 2.5 * obj\_size 
objects_to_generate: {BOX, CONE, TRIANGULAR_PYRAMID, RECTANGULAR_PYRAMID, CYLINDER} 
object_count_range: (5, 8)
object_size_range: ds = obj\_size * 0.5, (obj_size - ds, obj_size + ds)
object_height_distribution: (0, scene_size/2)
allow_overlap: true
```

## Scanner Settings
```
scanner_object: scanner
scene_size: scene_size
frame_start: 0
frame_end: 200
min_angle: 0
max_angle: 180
add_noisy_blender_mesh: True
```
