---
id: computing-software.networking-hardware-and-wireless.network-device-administration.nda-junos-commit-model
name: nda-junos-commit-model
category: computing-software
field: networking-hardware-and-wireless
product: network-device-administration
tags: [junos-commit-model, commit-confirmed, junos-rollback]
level: practitioner
status: draft
description: "Use Junos candidate and active configuration, commit check, commit confirmed and rollback to change devices safely."
sources:
  - https://www.juniper.net/documentation/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Junos commit model

- Edits go into a candidate configuration; nothing is live until `commit`. Use `show | compare` to see the diff before committing.
- `commit check` validates; `commit confirmed 5` auto-rolls back after 5 minutes unless you commit again - the key safety net for remote changes.
- `rollback 1` loads the previous committed config into the candidate (then commit); Junos keeps 50 rollbacks by default. `show system commit` lists history.
- `commit comment "ticket-123 add vlan"` documents the change.
- Groups and apply-groups reduce repetition; `display inheritance` shows resulting config.
- Private/exclusive config modes avoid editing collisions.

## Verify
- [ ] After a confirmed commit, you confirmed connectivity then ran a final `commit` before the timer expired.
