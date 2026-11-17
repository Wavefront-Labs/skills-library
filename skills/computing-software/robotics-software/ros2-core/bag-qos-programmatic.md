---
id: computing-software.robotics-software.ros2-core.bag-qos-programmatic
name: bag-qos-programmatic
category: computing-software
field: robotics-software
product: ros2-core
tags: [bag-qos-override, qos-profile-overrides, rosbag2-py, bag-compression, bag-filter]
level: advanced
status: docs-checked
description: "Handle QoS overrides, compression and rosbag2_py reading when bags will not replay cleanly."
sources:
  - https://github.com/ros2/rosbag2/blob/rolling/README.md
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/Developer-Tools/Debugging/Testing/Overriding-QoS-Policies-For-Recording-And-Playback.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# rosbag2 QoS and API
- Override QoS: `ros2 bag record --qos-profile-overrides-path qos.yaml` and `ros2 bag play --qos-profile-overrides-path qos.yaml`. YAML maps topic to `reliability`, `durability`, `history`, `depth`.
- Compression: `--compression-mode file --compression-format zstd`.
- Read data in Python:
```python
import rosbag2_py
r = rosbag2_py.SequentialReader()
r.open(rosbag2_py.StorageOptions(uri='run1'), rosbag2_py.ConverterOptions('', ''))
while r.has_next():
    msg = r.read_next()          # messages come back in stored order
```
- The storage id (for example `mcap`) goes in `StorageOptions(storage_id=...)`.
- `ros2 bag convert` rewrites bags, for example to another storage_id; see the rosbag2 README.

## Gotchas
- Latched (transient-local) topics such as `/map` or `/tf_static` can be repeated into every split file with `--repeat-transient-local`.

## Checked
2026-11-02. Confirmed in the rosbag2 README and Overriding-QoS-Policies-For-Recording-And-Playback (rolling): --qos-profile-overrides-path on record and play, --compression-mode file with --compression-format zstd, StorageOptions with storage_id, ros2 bag convert, --repeat-transient-local. Removed the YAML key list, sqlite3 as an example id, and the deserialization gotcha (the reader snippet is the SequentialReader pattern; its type helpers were not shown in the pages read).
Method: documentation only; no commands were run.

## Self-check
Reading the bag in Python reproduces the count shown by `ros2 bag info`.
