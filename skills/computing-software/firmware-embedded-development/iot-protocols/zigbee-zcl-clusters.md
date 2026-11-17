---
id: computing-software.firmware-embedded-development.iot-protocols.zigbee-zcl-clusters
name: zigbee-zcl-clusters
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [zigbee-zcl-clusters, zigbee-stack, zigbee, zcl, cluster, endpoint, binding, iot-protocols]
level: practitioner
status: draft
description: "Zigbee Cluster Library clusters: Use ZCL clusters, attributes and reporting."
sources:
  - https://csa-iot.org/developer-resource/specifications-download-request/
  - https://csa-iot.org/all-solutions/zigbee/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Zigbee Cluster Library clusters

**Goal:** Use ZCL clusters, attributes and reporting.

## Steps
1. Application profile 0x0104 (Home Automation) and Zigbee 3.0
2. Clusters: Basic 0x0000, Power Configuration 0x0001, Identify 0x0003, Groups 0x0004, On/Off 0x0006, Level 0x0008, Color 0x0300, Temperature 0x0402
3. Commands: Read Attributes, Write, Configure Reporting (min interval, max interval, reportable change)
4. Bind a cluster to a destination for automatic reports
5. Servers hold attributes; clients send commands
6. Endpoint 1-240 holds app cluster set, endpoint 0 is ZDO

## Gotcha
Reporting configured without a binding on the target sends nothing; set both.

## Verify
- [ ] Read Attributes returns value
- [ ] Report arrives after min interval and change
- [ ] Binding table entries exist
