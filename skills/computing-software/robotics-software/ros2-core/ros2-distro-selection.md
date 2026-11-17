---
id: computing-software.robotics-software.ros2-core.ros2-distro-selection
name: ros2-distro-selection
category: computing-software
field: robotics-software
product: ros2-core
tags: [ros-distros, humble, jazzy, rep-2000, lts, ros2-distros-environment]
level: intro
status: docs-checked
description: "Choose a ROS 2 distribution (Humble, Jazzy, Rolling) by Ubuntu release, LTS status and end-of-life date."
sources:
  - https://www.ros.org/reps/rep-2000.html
  - https://github.com/ros2/ros2_documentation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Choosing a ROS 2 distribution
**Goal:** pick a release that matches your OS and support window.

- Humble Hawksbill: Ubuntu Jammy (22.04), supported May 2022 to May 2027. Jazzy Jalisco: Ubuntu Noble (24.04), supported May 2024 to May 2029. Rolling is the continuously updated development distribution and can have breaking changes. Check the release table on docs.ros.org and REP 2000 for current dates.
- Binary packages: `sudo apt install ros-jazzy-desktop` (use `ros-humble-desktop` on 22.04). - Nodes are not guaranteed to communicate across distributions; rebuild against the distro you deploy.
- Pick a release with a long support window for products; pick the newest only if you need a specific feature.

## Gotchas
- REP 2000 lists the target platforms per distro; other platforms are on you.
- Docs URLs are versioned (`docs.ros.org/en/jazzy/`); a tutorial for another distro may differ.

## Self-check
`printenv ROS_DISTRO` after sourcing prints the expected name.

## Checked
2026-11-03. Confirmed in REP 2000 (Humble May 2022 - May 2027 on Ubuntu Jammy; Jazzy May 2024 - May 2029 on Ubuntu Noble), the ros2_documentation Releases page (EOL table, Rolling description, cross-distribution note), the Ubuntu install page (`ros-{DISTRO}-desktop`) and the environment page (`ROS_DISTRO`). Removed: "LTS" label (not stated in the pages read), apt-prefix claim, `ros2 doctor` currency claim.
Method: documentation only; no commands were run.
