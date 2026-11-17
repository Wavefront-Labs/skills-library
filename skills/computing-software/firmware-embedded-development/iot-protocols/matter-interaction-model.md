---
id: computing-software.firmware-embedded-development.iot-protocols.matter-interaction-model
name: matter-interaction-model
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [matter-interaction-model, matter-interaction, matter, interaction-model, invoke, im, iot-protocols]
level: practitioner
status: draft
description: "Matter read write invoke: Use Matter interactions correctly."
sources:
  - https://csa-iot.org/developer-resource/specifications-download-request/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Matter read write invoke

**Goal:** Use Matter interactions correctly.

## Steps
1. Four actions: Read, Write, Invoke (commands), Subscribe
2. Paths address endpoint/cluster/attribute-or-command, wildcards allowed on reads
3. Messages use secure Message Layer (UDP, TCP for large) with MRP (Message Reliable Protocol) acks and retransmission
4. Timed Invoke needed for sensitive commands such as door lock; send TimedRequest first
5. Data versioning uses DataVersion filters
6. Status codes: SUCCESS, UNSUPPORTED_ACCESS, UNSUPPORTED_ENDPOINT

## Gotcha
Writing without access privilege returns UNSUPPORTED_ACCESS, not a transport error; check the ACL first.

## Verify
- [ ] Wildcard read returns all attributes
- [ ] Timed invoke enforced
- [ ] Status code mapping handled
