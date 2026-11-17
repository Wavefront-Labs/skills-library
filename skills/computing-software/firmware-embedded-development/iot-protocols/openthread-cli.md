---
id: computing-software.firmware-embedded-development.iot-protocols.openthread-cli
name: openthread-cli
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [openthread-cli, thread-ipv6, openthread, ot-ctl, dataset, cli, iot-protocols]
level: practitioner
status: docs-checked
description: "OpenThread CLI: Bring up a Thread node and inspect it from the CLI."
sources:
  - https://openthread.io/reference/cli
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenThread CLI

**Goal:** Bring up a Thread node and inspect it from the CLI.

## Steps
1. Create network: dataset init new, then dataset commit active, ifconfig up, thread start
2. Join: dataset set active <hex>, ifconfig up, thread start
3. Check: state, rloc16, ipaddr, neighbor table, router table, child table
4. Diagnostics: scan, counters mac (counters mac reset clears them)
5. Use dataset channel and dataset networkkey to view or set those fields of the dataset being built; channel (get,set) reads or sets the radio channel

## Gotcha
dataset init new only initialises a new dataset; it takes effect only after dataset commit active.

## Verify
- [ ] state reaches leader, router or child
- [ ] neighbor table lists the peer node

## Checked
Confirmed 2026-11-08 against the OpenThread CLI command reference (the dataset, ifconfig, thread, state, rloc16, ipaddr, neighbor, router, child, scan, counters mac and channel entries, found by heading search; the page was not read end to end). Removed as not found on that page: ping, the sudo ot-ctl and OTBR step, the script/build OT_COMMISSIONER=ON step, and the claim about detached state on a mismatched dataset. The IPv6 addressing source was dropped as unread.
Method: documentation only; no commands were run.
