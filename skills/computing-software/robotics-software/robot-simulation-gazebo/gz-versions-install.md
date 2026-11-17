---
id: computing-software.robotics-software.robot-simulation-gazebo.gz-versions-install
name: gz-versions-install
category: computing-software
field: robotics-software
product: robot-simulation-gazebo
tags: [gz-versions, gazebo-harmonic, gazebo-fortress, gz-sim, ign-gazebo, gazebo-classic, gz-install-cli]
level: intro
status: docs-checked
description: "Pick the Gazebo release that pairs with your ROS 2 distro and install gz-sim by binary or source."
sources:
  - https://raw.githubusercontent.com/gazebosim/ros_gz/ros2/README.md
  - https://raw.githubusercontent.com/gazebosim/gz-sim/gz-sim9/tutorials/install.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gazebo versions and install

## ROS 2 and Gazebo pairing (ros_gz README, ros2 branch)
| ROS 2 | Gazebo | ros_gz branch | Binaries |
|---|---|---|---|
| Humble | Fortress | humble | packages.ros.org |
| Humble | Garden, Harmonic | humble | Gazebo (OSRF) packages |
| Jazzy | Harmonic | jazzy | packages.ros.org |
| Jazzy | Garden | ros2 | source only |
| Kilted | Ionic | kilted | packages.ros.org |
| Lyrical, Rolling | Jetty | ros2 | packages.ros.org |
| Lyrical, Rolling | Harmonic, Ionic | ros2 | source only |

The README marks Garden as end-of-life. Use the branch matching your ROS distro; the table
changes with each release, so re-read it.
- `ros_ign`-prefixed packages are shims that redirect to their `ros_gz` counterparts; use
  the `ros_gz` ones.
- Binary install of the integration: `sudo apt install ros-<distro>-ros-gz` (the README
  shows `ros-rolling-ros-gz`) after adding packages.ros.org.
- When building ros_gz from source, `rosdep install -r --from-paths src -i -y --rosdistro <distro>`
  installs the paired Gazebo automatically.

## Standalone gz-sim install (gz-sim9 install tutorial)
Replace `<#>` with the library major version.
- Ubuntu: add the OSRF apt repository, then `sudo apt-get install libgz-sim<#>-dev`.
- macOS: `brew tap osrf/simulation`, then `brew install gz-sim<#>`.
- Windows: Conda env, then `conda install gz-sim<#> --channel conda-forge`.
- Source: `git clone https://github.com/gazebosim/gz-sim -b gz-sim<#>`, install dependencies
  per platform, then cmake and make.

## Gotchas
- The ros_gz branch must match both the ROS distro and the Gazebo release installed.

## Self-check
`dpkg -l | grep gz-sim` (or conda list) shows the intended `gz-sim<#>` major version for the
row of the table you chose.

## Checked
Method: docs-checked 2026-11-09 against the ros_gz README.md (ros2 branch) and the gz-sim9 install.md tutorial (raw GitHub, read in full). Removed as unconfirmed: the Gazebo Classic end-of-life 2025 claim and gazebo_ros_pkgs mention, Garden-to-Ionic gz-sim number mapping, `ign` vs `gz` command and env-var rename, `ignition-gazebo-*` plugin filename change, `gz sim --versions`, the `gz sim shapes.sdf` check, and the landing-page source gazebosim.org/docs.
