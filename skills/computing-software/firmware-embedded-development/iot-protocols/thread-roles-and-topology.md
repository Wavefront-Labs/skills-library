---
id: computing-software.firmware-embedded-development.iot-protocols.thread-roles-and-topology
name: thread-roles-and-topology
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [thread-roles-and-topology, thread-network, thread, router, leader, partition, iot-protocols]
level: practitioner
status: docs-checked
description: "Thread device roles and topology: forwarding roles, FTD/MTD device types, Leader, partitions and role limits."
sources:
  - https://openthread.io/guides/thread-primer/node-roles-and-types
  - https://www.threadgroup.org/What-is-Thread/Overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Thread device roles and topology

**Goal:** Understand how a Thread mesh is divided into roles and what happens when it splits.

## Steps
1. Forwarding roles: a Mesh Extender (router) forwards packets, helps devices join, and keeps its radio on. An End Device talks to one Mesh Extender, its Parent, and can switch its radio off.
2. Device types: Full Thread Devices (FTD) keep the radio on and subscribe to the all-routers multicast. They are either Extender-Capable Devices (ECD) or Full End Devices (FED, always a child).
3. Minimal Thread Devices (MTD) are always End Devices and send everything via their Parent: Minimal End Device (radio always on, no polling) or Sleepy End Device (wakes periodically to poll its parent).
4. A standby ECD upgrades to Mesh Extender when it is the only node in reach of a joining device, or when it attaches while there are fewer than 16 Mesh Extenders. A Mesh Extender with no children can downgrade.
5. Thread tries to keep 16 to 23 Mesh Extenders. Limits: 1 Leader per partition, 32 Mesh Extenders, 511 End Devices per Mesh Extender.
6. The Leader is a Mesh Extender, self-elected dynamically, that manages the set of Mesh Extenders and aggregates and distributes network-wide configuration.
7. A partition forms when groups lose contact. Each has its own Leader, Router ID assignments and network data, but all share the same security credentials. They merge automatically when connectivity returns.
8. A Border Router passes data between Thread and a non-Thread network such as Wi-Fi; a network can have more than one.

## Gotcha
A sleepy device with a single possible parent loses its link if that parent dies. Plan for more than one Mesh Extender in range (design advice, not stated on the cited pages).

## Verify
- [ ] Device state shows leader, router or child as designed
- [ ] Router and child tables list the expected neighbours
- [ ] Sleepy device re-attaches after its parent is powered off

## Checked

2026-11-08. Confirmed on the OpenThread node roles page: forwarding roles, FTD/MTD types, upgrade and downgrade, the 16 to 23 target, role limits (1, 32, 511), Leader, partitions and merging, Border Router. The page uses the terms Mesh Extender and standby ECD, so those are used here. Removed as unsupported: MLE on UDP 19788, the RLOC16 bit layout, and the claim that the Leader assigns router IDs (the page only says each partition has its own Router ID assignments). The Thread Group overview page is a marketing overview and supports only the general description. The Gotcha is marked as design advice.
Method: documentation only; no commands were run.
