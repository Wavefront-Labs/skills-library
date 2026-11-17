---
id: computing-software.robotics-software.ros2-core.bag-record-play
name: bag-record-play
category: computing-software
field: robotics-software
product: ros2-core
tags: [bag-record, ros2-bag, rosbag2, record, play, mcap, sqlite3, ros2-rosbag2]
level: practitioner
status: docs-checked
description: "Record and replay topics with ros2 bag record, info and play, including rate, loop and clock options."
sources:
  - https://github.com/ros2/rosbag2/blob/rolling/README.md
  - https://github.com/ros2/rosbag2/blob/rolling/ros2bag/ros2bag/verb/play.py
  - https://github.com/ros2/rosbag2/blob/rolling/ros2bag/ros2bag/verb/record.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# rosbag2 record and play
```bash
ros2 bag record -o run1 /scan /tf /tf_static /odom        # or -a for all topics
ros2 bag info run1
ros2 bag play run1 --rate 0.5 --loop --clock              # --clock publishes /clock
ros2 bag play run1 --topics /scan
```
- Storage plugins include sqlite3 and mcap; `-s`/`--storage <storage_id>` picks one on record, and the current default is `mcap`. The player detects the storage automatically.
- Latched (transient-local) topics such as `/map` or `/tf_static` can be kept in every split file with `--repeat-transient-local` or `--repeat-all-transient-local`.
- Split files: `-b`/`--max-bag-size` (bytes) and `-d`/`--max-bag-duration` (seconds); both default to 0, a single file.

## Gotchas
- `-a` records all topics; `-e`/`--regex` filters topics by regular expression.

## Checked
2026-11-02. Confirmed in the rosbag2 README and the ros2bag record.py and play.py option lists (rolling): -o, -a, -s/--storage, --topics, -e/--regex, -b/--max-bag-size, -d/--max-bag-duration, -r/--rate, -l/--loop, --clock, --repeat-transient-local, mcap as default storage, auto-detected storage on play. Removed --remap example, the use_sim_time advice and the stored-QoS replay claim (not in the docs read).
Method: documentation only; no commands were run.

## Self-check
`ros2 bag info` message counts match expectations; playback drives RViz identically.
