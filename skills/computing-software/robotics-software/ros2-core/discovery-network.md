---
id: computing-software.robotics-software.ros2-core.discovery-network
name: discovery-network
category: computing-software
field: robotics-software
product: ros2-core
tags: [discovery-config, ros-domain-id, automatic-discovery-range, static-peers, multicast, discovery-server]
level: advanced
status: docs-checked
description: "Configure discovery on real networks: domain IDs, localhost-only range, static peers and the discovery server."
sources:
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/Developer-Tools/Launch/Improved-Dynamic-Discovery.rst
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/Developer-Tools/Launch/Discovery-Server/Discovery-Server.rst
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/ROS-Framework/nodes/About-Domain-ID.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Discovery and networking
- By default ROS 2 finds all nodes on all hosts of the same subnet automatically; for DDS middleware that means any node reachable via multicast. Nodes on the same domain ID discover each other, nodes on different domains cannot.
- Restrict scope with `ROS_AUTOMATIC_DISCOVERY_RANGE` (values include `LOCALHOST`, `SUBNET` (default), `OFF`) and `ROS_STATIC_PEERS`, a semicolon-separated list of addresses to discover nodes on. Neither variable is supported by `rmw_zenoh`.
- Multicast-unfriendly networks such as Wi-Fi: use the Fast DDS Discovery Server (`fastdds discovery --server-id 0`, default port 11811; clients set `ROS_DISCOVERY_SERVER=<ip>:11811`).
- The domain ID is used by DDS to compute the UDP ports used for discovery and communication.

## Gotchas
- Different domain ids never see each other; same id on a shared LAN means other people's robots appear.

## Checked
2026-11-02. Confirmed in Improved-Dynamic-Discovery, Discovery-Server and About-Domain-ID (ros2_documentation, rolling): default subnet discovery via multicast, ROS_AUTOMATIC_DISCOVERY_RANGE and ROS_STATIC_PEERS semantics, rmw_zenoh exclusion, Discovery Server command and ROS_DISCOVERY_SERVER, port 11811, domain ID to UDP port mapping. Removed ROS_LOCALHOST_ONLY, the Iron cut-off, container advice, the firewall line and the VPN claim (not in the docs read).
Method: documentation only; no commands were run.

## Self-check
`ros2 node list` from the second machine lists the first machine's nodes.
