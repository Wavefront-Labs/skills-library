---
id: computing-software.firmware-embedded-development.iot-protocols.lwm2m-object-model
name: lwm2m-object-model
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [lwm2m-object-model, lwm2m-model, lwm2m, object, resource, ipso, iot-protocols]
level: practitioner
status: draft
description: "LwM2M objects, instances and resources: Address LwM2M data correctly as /ObjectID/InstanceID/ResourceID."
sources:
  - https://www.openmobilealliance.org/lwm2m/
  - https://www.openmobilealliance.org/release/LightweightM2M/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LwM2M objects, instances and resources

**Goal:** Address LwM2M data correctly as /ObjectID/InstanceID/ResourceID.

## Steps
1. Standard objects: 0 Security, 1 Server, 2 Access Control, 3 Device, 4 Connectivity Monitoring, 5 Firmware Update, 6 Location
2. Example /3/0/0 is Device manufacturer; /3/0/4 is Reboot (executable)
3. Resources have operations R, W, E and types (string, integer, float, boolean, opaque, time)
4. Multi-instance resources add /ResourceInstanceID
5. IPSO/OMA SpecWorks objects 3300-series cover sensors; register custom objects in the OMA registry (lwm2m registry)
6. Content formats: TLV, JSON, SenML-CBOR, SenML-JSON, plain text

## Gotcha
Using an unregistered object ID in the reserved range collides with future standards; use the vendor range described in the OMA registry rules (confirm exact bounds) or register.

## Verify
- [ ] Read /3/0 returns expected resources
- [ ] Execute /3/0/4 reboots
- [ ] Object XML validates against the schema
