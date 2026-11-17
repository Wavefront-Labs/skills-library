---
id: computing-software.robotics-software.ros2-core.rclcpp-node
name: rclcpp-node
category: computing-software
field: robotics-software
product: ros2-core
tags: [rclcpp-node, rclcpp, cpp, ament-cmake, spin, ros2-nodes]
level: practitioner
status: docs-checked
description: "Write a ROS 2 node in C++ with rclcpp: Node subclass, timers, spin, and CMake dependencies."
sources:
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/ROS-Framework/client-libraries/Working-with-Client-Libraries/Writing-A-Simple-Cpp-Publisher-And-Subscriber.rst
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/Capabilities/Simulation/URDF/Using-URDF-with-Robot-State-Publisher-cpp.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# rclcpp node
**Goal:** a minimal C++ node that builds under colcon.

```cpp
#include "rclcpp/rclcpp.hpp"
class Tick : public rclcpp::Node {
 public:
  Tick() : Node("tick") {
    timer_ = create_wall_timer(std::chrono::seconds(1), [this]{ RCLCPP_INFO(get_logger(), "tick"); });
  }
 private: rclcpp::TimerBase::SharedPtr timer_;
};
int main(int argc, char** argv){ rclcpp::init(argc, argv); rclcpp::spin(std::make_shared<Tick>()); rclcpp::shutdown(); }
```
CMake: `find_package(rclcpp REQUIRED)`, `add_executable(...)`, link dependencies with `target_link_libraries`, and `install(TARGETS <exe> DESTINATION lib/${PROJECT_NAME})`. Add `<depend>rclcpp</depend>` to package.xml.

## Gotchas
- Keep the timer and publisher handles as class members (the tutorials store `timer_` as a member).

## Checked
2026-11-02. Confirmed in the C++ publisher/subscriber tutorial and URDF robot-state-publisher C++ page (ros2_documentation, rolling): rclcpp::spin of a shared_ptr node, create_wall_timer, timer_ member, find_package/add_executable/target_link_libraries, install(TARGETS ... DESTINATION lib/${PROJECT_NAME}), <depend>rclcpp</depend>. Removed ament_target_dependencies and the missing-install gotcha claim (not in the docs read).
Method: documentation only; no commands were run.

## Self-check
After `colcon build` and sourcing the workspace, `ros2 run <pkg> tick` logs once per second.
