---
id: computing-software.firmware-embedded-development.iot-protocols.matter-multi-admin
name: matter-multi-admin
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [matter-multi-admin, matter-commissioning, matter, multi-admin, administrator-commissioning, acl, iot-protocols]
level: practitioner
status: draft
description: "Matter multi-admin: Share one device between ecosystems."
sources:
  - https://csa-iot.org/developer-resource/specifications-download-request/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Matter multi-admin

**Goal:** Share one device between ecosystems.

## Steps
1. Existing admin opens a window: Administrator Commissioning cluster OpenCommissioningWindow (enhanced, with new passcode and discriminator) or OpenBasicCommissioningWindow
2. Second ecosystem commissions with the new code and receives its own fabric and NOC
3. Access Control cluster ACL entries per fabric grant subjects privilege levels (View, Operate, Manage, Administer)
4. Each fabric sees only its own ACL and bindings
5. RevokeCommissioning closes the window

## Gotcha
Devices have a limited number of fabrics (5 minimum); a 6th ecosystem add fails with a resource error.

## Verify
- [ ] Both ecosystems control the device
- [ ] ACL lists per fabric
- [ ] Window times out
