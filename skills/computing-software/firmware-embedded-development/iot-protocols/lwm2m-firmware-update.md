---
id: computing-software.firmware-embedded-development.iot-protocols.lwm2m-firmware-update
name: lwm2m-firmware-update
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [lwm2m-firmware-update, lwm2m-operations, lwm2m, object-5, firmware-update, pull-push, iot-protocols]
level: practitioner
status: draft
description: "LwM2M firmware update object: Update firmware via Object 5."
sources:
  - https://www.openmobilealliance.org/lwm2m/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LwM2M firmware update object

**Goal:** Update firmware via Object 5.

## Steps
1. Resources: 0 Package (push), 1 Package URI (pull), 2 Update (execute), 3 State, 5 Update Result, 6 PkgName, 8 Delivery Method
2. States: 0 Idle, 1 Downloading, 2 Downloaded, 3 Updating
3. Server writes URI, client downloads over CoAP or HTTP(S) with block-wise, moves state, then executes Update
4. Update Result 1 means success, other values give failure reasons
5. Client reboots and re-registers with new Device object version
6. Observe /5/0/3 and /5/0/5 for progress

## Gotcha
Verify image signature before Update; the object has no built-in signature requirement.

## Verify
- [ ] State machine transitions logged
- [ ] Result 1 after update
- [ ] Bad image leaves state Idle with error result
