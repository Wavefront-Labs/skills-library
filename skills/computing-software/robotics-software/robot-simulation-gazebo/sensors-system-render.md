---
id: computing-software.robotics-software.robot-simulation-gazebo.sensors-system-render
name: sensors-system-render
category: computing-software
field: robotics-software
product: robot-simulation-gazebo
tags: [render-engine, ogre2, headless-rendering, gpu-requirements, sdf-sensor]
level: advanced
status: docs-checked
description: "Run Gazebo with sensors headless via EGL (OGRE2) on servers, and set common SDF sensor elements."
sources:
  - https://raw.githubusercontent.com/gazebosim/gz-sim/gz-sim9/tutorials/headless_rendering.md
  - https://raw.githubusercontent.com/gazebosim/sdformat/sdf14/sdf/1.11/sensor.sdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sensors and headless rendering

## Headless rendering (Gazebo headless tutorial)
GPU-dependent sensors historically needed an X server; EGL creates rendering surfaces
without one. Gazebo exposes it as `--headless-rendering`, available only with OGRE2:
```bash
DISPLAY= gz sim -v 4 -s -r --headless-rendering sensors_demo.sdf
```
- As a library: `ServerConfig::SetHeadlessRendering(bool)`; the world must use OGRE2.
- A GPU instance is recommended for render-based sensors; without a GPU, OGRE falls back to
  software rendering.
- Tutorial's cloud recipe (AWS, Ubuntu 20.04 or newer, GPU instance type such as
  `g3.4xlarge`): `sudo apt install ubuntu-drivers-common && sudo ubuntu-drivers install`,
  add the user to the `render` group (`sudo usermod -a -G render ubuntu`), reboot, install
  Gazebo, then run the command above.
- Verify data flows: `gz topic -ft /thermal_camera` shows a frequency.
- Verify EGL was used: `grep -R "EGL Subsystem" ~/.gz/rendering/ogre2.log` must be non-empty.

## SDF `<sensor>` common elements (SDF 1.11)
- `name` (unique) and `type` attributes. Types include camera, depth_camera,
  rgbd_camera, thermal_camera, segmentation_camera, boundingbox_camera, lidar, gpu_lidar,
  imu, magnetometer, altimeter, air_pressure, air_speed, contact, force_torque, navsat,
  logical_camera, sonar, custom, and others. `ray`, `gpu_ray` and `gps` are legacy aliases
  of `lidar`, `gpu_lidar` and `navsat`; the spec prefers the new names.
- `always_on` (default false), `update_rate` (default 0: generate every cycle),
  `visualize` (default false), `topic` (needed for visualisation), `enable_metrics`
  (default false).

## Self-check
The server runs with `DISPLAY=` unset and the camera topic reports a steady frequency.

## Checked
Method: docs-checked 2026-11-09 against the gz-sim9 headless_rendering.md tutorial and the sdformat 1.11 sensor.sdf (raw GitHub, read in full). Removed as unconfirmed: the Sensors system plugin snippet and `render_engine` element, the Imu system plugin, "ogre2 default in newer releases", `xvfb-run`, container `/dev/dri` and Mesa advice, noise model element names, Wayland/VM symptoms, `gz sim -v4` diagnosis, and the landing-page source gazebosim.org/docs.
