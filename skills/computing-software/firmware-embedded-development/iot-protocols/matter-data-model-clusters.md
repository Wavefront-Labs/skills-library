---
id: computing-software.firmware-embedded-development.iot-protocols.matter-data-model-clusters
name: matter-data-model-clusters
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [matter-data-model-clusters, matter-core, matter, cluster, attribute, endpoint, iot-protocols]
level: practitioner
status: draft
description: "Matter data model and clusters: Navigate endpoints, clusters, attributes and commands."
sources:
  - https://csa-iot.org/developer-resource/specifications-download-request/
  - https://csa-iot.org/all-solutions/matter/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Matter data model and clusters

**Goal:** Navigate endpoints, clusters, attributes and commands.

## Steps
1. Node has endpoints (endpoint 0 is the root node with Basic Information, General Commissioning, Network Commissioning, Operational Credentials, Access Control)
2. Each endpoint has a device type and clusters
3. Cluster contains attributes, commands, events
4. Common clusters: On/Off (0x0006), Level Control (0x0008), Color Control (0x0300), Temperature Measurement (0x0402), Door Lock (0x0101), Thermostat (0x0201)
5. Attributes are typed and may be reportable, fabric-scoped
6. Use chip-tool onoff toggle <node> <endpoint> to test

## Gotcha
Do not invent attribute IDs; use the cluster XML in the SDK data model so IDs and quality flags stay correct.

## Verify
- [ ] chip-tool read returns attribute
- [ ] Command ack returns status
- [ ] Endpoint composition matches device type
