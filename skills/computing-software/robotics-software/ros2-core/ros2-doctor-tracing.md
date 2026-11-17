---
id: computing-software.robotics-software.ros2-core.ros2-doctor-tracing
name: ros2-doctor-tracing
category: computing-software
field: robotics-software
product: ros2-core
tags: [ros2-doctor, ros2-wtf, ros2-trace, ros2-launch-log, log-level, rcutils-logging]
level: advanced
status: docs-checked
description: "Diagnose with ros2 doctor, log levels and ros2_tracing; read ROS logs."
sources:
  - https://github.com/ros2/ros2_documentation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Diagnostics and tracing
```bash
ros2 doctor --report                       # full report, includes a QoS compatibility list
ros2 node info /my_node                    # pubs, subs, services, actions
ros2 run my_pkg exe --ros-args --log-level debug
ros2 run my_pkg exe --ros-args --log-level my_node:=warn
ros2 daemon stop ; ros2 daemon start       # restart the CLI daemon
```
- Logs go to `~/.ros/log` (override with `ROS_LOG_DIR`); `RCUTILS_COLORIZED_OUTPUT=1`, `RCUTILS_CONSOLE_OUTPUT_FORMAT` customize console format.
- `ros2_tracing` (LTTng) traces callback and message latency: install `ros-<distro>-ros2trace` and `ros-<distro>-tracetools-analysis`, run `ros2 trace`, analyze with tracetools_analysis (the `trace` tool is Linux only).
- Use `RCLCPP_INFO_THROTTLE(get_logger(), *get_clock(), 1000, ...)` to rate-limit logs.

## Gotchas
- Stop any existing daemon (`ros2 daemon stop`) before starting one in the foreground; match `ROS_DOMAIN_ID` to the daemon you want to control.

## Self-check
`ros2 doctor` reports no errors, and `--log-level debug` output appears for one node only.

## Checked
2026-11-03. Confirmed in the ros2_documentation source (Logging-and-logger-configuration, About-Command-Line-Tools, ROS2-Tracing-Trace-and-Analyze, Galactic release notes): `ros2 doctor --report` and its QoS compatibility list, `ROS_LOG_DIR`, default `~/.ros/log`, `RCUTILS_COLORIZED_OUTPUT`, `RCUTILS_CONSOLE_OUTPUT_FORMAT`, `--log-level node:=LEVEL`, `ros2 daemon stop/start`, `ros2 node info`, `ros2 trace`, apt packages `ros2trace` and `tracetools-analysis`, `RCLCPP_INFO_THROTTLE`. Fixed: package name `tracetools-trace` does not exist in the tutorial (it uses `ros2trace`). Removed: unconfirmed stale-daemon and debug-starvation claims.
Method: documentation only; no commands were run.
