---
id: computing-software.robotics-software.robot-simulation-gazebo.gz-cli-topics-services
name: gz-cli-topics-services
category: computing-software
field: robotics-software
product: robot-simulation-gazebo
tags: [gz-cli, gz-sim-r, gz-topic, gz-service]
level: practitioner
status: docs-checked
description: "Run worlds and inspect or control them with gz sim, gz topic and gz service."
sources:
  - https://raw.githubusercontent.com/gazebosim/gz-sim/gz-sim9/tutorials/pause_run_simulation.md
  - https://raw.githubusercontent.com/gazebosim/gz-sim/gz-sim9/tutorials/headless_rendering.md
  - https://raw.githubusercontent.com/gazebosim/ros_gz/ros2/ros_gz_bridge/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# gz CLI

## Run a world
```bash
gz sim default.sdf                                   # GUI + server
DISPLAY= gz sim -v 4 -s -r --headless-rendering sensors_demo.sdf
```
In the Gazebo tutorials `-s` runs the server only (no GUI window, used for headless runs),
`-r` runs immediately and `-v 4` raises verbosity. Without `-r` the world starts paused
(the ros_gz service example notes Gazebo "will be paused by default").

## Pause and run over the transport API
The service `/world/<world_name>/control` takes `gz.msgs.WorldControl` and returns
`gz.msgs.Boolean`; the `pause` field starts or stops simulation. Paused means time stops and
physics does not run.
```bash
gz service -s /world/default/control --reqtype gz.msgs.WorldControl --reptype gz.msgs.Boolean --timeout 3000 --req 'pause: false'
gz service -s /world/default/control --reqtype gz.msgs.WorldControl --reptype gz.msgs.Boolean --timeout 3000 --req 'pause: true'
```
The GUI World Control plugin has a play/pause button.

## Topics
```bash
gz topic -l                                   # list topics (the bridge README pipes this to grep image)
gz topic --echo --topic /stats -n 1           # one stats message: sim_time, real_time, iterations, real_time_factor
gz topic -e -t /chatter                       # echo a topic
gz topic -ft /thermal_camera                  # frequency of a sensor topic
gz topic -t /chatter -m gz.msgs.StringMsg -p 'data:"Hello"'   # publish
```
- Gazebo Transport topics carry `gz.msgs.*` messages, not ROS messages; `ros_gz_bridge`
  converts between them.
- `/stats` includes a `paused` field when the simulator is paused.

## Self-check
After `pause: true` the `/stats` sim_time stops increasing; `pause: false` resumes it.

## Checked
Method: docs-checked 2026-11-09 against the gz-sim9 pause_run_simulation and headless_rendering tutorials and the ros_gz_bridge README (raw GitHub, read in full). Removed as unconfirmed: the `-g` GUI-only flag, `gz service -l`, `gz model --list`, `gz sdf -k` and `gz sdf -p` validation/conversion, the `/world/default/stats` topic name, the Twist publish example, and the landing-page source gazebosim.org/docs. Resource-path variables are covered in the sdf-fuel-includes skill.
