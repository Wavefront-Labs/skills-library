---
id: computing-software.networking-hardware-and-wireless.network-device-administration.nda-ios-xe-show-and-debug-practice
name: nda-ios-xe-show-and-debug-practice
category: computing-software
field: networking-hardware-and-wireless
product: network-device-administration
tags: [ios-xe-show-commands, conditional-debug, embedded-event-manager, nda-ios-xe-troubleshooting]
level: advanced
status: draft
description: "Collect state with show commands and counters, use conditional debugs and packet capture safely, and automate with EEM."
sources:
  - https://www.cisco.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IOS-XE troubleshooting practice

- Start with show commands: `show interfaces counters errors`, `show ip route`, `show ip protocols`, `show logging`, `show processes cpu sorted`, `show tech-support` for TAC.
- Debugs can overload the CPU. Use conditional debugging (`debug condition ...`), limit output, send to buffer logging, and `undebug all` immediately after.
- Embedded Packet Capture (EPC) captures on the data plane for a specific interface and ACL.
- EEM applets run commands on events (syslog patterns, interface down, scheduled) to collect evidence automatically.
- Use `terminal length 0`, and record timestamps; keep a change log.

## Verify
- [ ] The debug/capture was removed and CPU returned to baseline after troubleshooting.
