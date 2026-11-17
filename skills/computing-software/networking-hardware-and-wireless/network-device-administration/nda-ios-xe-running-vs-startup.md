---
id: computing-software.networking-hardware-and-wireless.network-device-administration.nda-ios-xe-running-vs-startup
name: nda-ios-xe-running-vs-startup
category: computing-software
field: networking-hardware-and-wireless
product: network-device-administration
tags: [ios-xe-config-management, config-replace-rollback, startup-config, nda-config-models]
level: practitioner
status: draft
description: "Save, compare, archive and roll back IOS-XE configuration with copy, configure replace and the archive feature."
sources:
  - https://www.cisco.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IOS-XE configuration lifecycle

- Changes apply immediately to running-config; they survive reload only after `copy running-config startup-config` (or `write memory`).
- `show archive config differences` and `configure replace flash:backup.cfg` (with `list`/`time` safety options such as `configure terminal revert timer`) support diffs and rollbacks. The archive feature must be enabled; confirm exact syntax for the release.
- `reload in 10` with an unsaved risky change is a classic safety net: cancel with `reload cancel` if the change works.
- Keep an off-box copy (TFTP/SCP/Git) after every approved change.
- Use `show running-config | section interface` and `| include` filters rather than reading full configs.

## Verify
- [ ] The diff between running and the off-box golden copy shows only the intended change.
