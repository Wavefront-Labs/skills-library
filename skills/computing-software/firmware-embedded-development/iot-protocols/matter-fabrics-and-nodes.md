---
id: computing-software.firmware-embedded-development.iot-protocols.matter-fabrics-and-nodes
name: matter-fabrics-and-nodes
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [matter-fabrics-and-nodes, matter-core, matter, fabric, noc, node-id, iot-protocols]
level: practitioner
status: draft
description: "Matter fabrics, nodes and operational credentials: Understand how Matter identifies devices and controllers."
sources:
  - https://csa-iot.org/developer-resource/specifications-download-request/
  - https://csa-iot.org/all-solutions/matter/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Matter fabrics, nodes and operational credentials

**Goal:** Understand how Matter identifies devices and controllers.

## Steps
1. A fabric is a trust domain with a Root CA; each node holds a NOC (Node Operational Certificate) signed by it, with Node ID and Fabric ID
2. Fabric index is local; a node supports several fabrics (multi-fabric), typically 5 minimum
3. Fabric ID plus Root public key give Compressed Fabric ID used in DNS-SD names
4. CASE (Certificate Authenticated Session Establishment) builds secure sessions between nodes using SIGMA
5. PASE is the passcode-based session used in commissioning

## Gotcha
Removing the last fabric returns the device to uncommissioned state; confirm before issuing RemoveFabric.

## Verify
- [ ] Operational Credentials cluster lists fabrics
- [ ] Node reachable via CASE from each fabric
- [ ] Fabric label set
