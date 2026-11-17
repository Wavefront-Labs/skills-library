---
id: computing-software.firmware-embedded-development.iot-protocols.thread-commissioning-meshcop
name: thread-commissioning-meshcop
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [thread-commissioning-meshcop, thread-network, thread, meshcop, commissioner, joiner, pskd, iot-protocols]
level: practitioner
status: draft
description: "Thread commissioning (MeshCoP): Join a new device to a Thread network securely."
sources:
  - https://openthread.io/guides/thread-primer/network-formation-and-joining
  - https://www.threadgroup.org/What-is-Thread/Overview
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Thread commissioning (MeshCoP)

**Goal:** Join a new device to a Thread network securely.

## Steps
1. Commissioner (on-mesh or external via Border Agent) authenticates the Joiner using DTLS with J-PAKE and a Pre-Shared Key for the Device (PSKd, 6-32 alphanumeric characters, no I, O, Q, Z)
2. CLI flow: commissioner start, commissioner joiner add <eui64|*> <pskd>, then on the joiner ifconfig up; joiner start <pskd>; thread start
3. Commissioner then delivers Thread network key and settings
4. Network key is 128 bits, kept secret
5. Active dataset holds channel, PAN ID, network name, ext PAN ID, mesh-local prefix

## Gotcha
Wildcard joiner (*) with weak PSKd lets anyone nearby join during the timeout; use specific EUI-64 and short timeouts.

## Verify
- [ ] Joiner prints Join success
- [ ] dataset active matches
- [ ] Wrong PSKd fails
