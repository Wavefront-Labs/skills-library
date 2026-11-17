---
id: computing-software.networking-hardware-and-wireless.arista-eos.change-control
name: change-control
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, change-control, cv-change-control, approval, rollback-snapshot]
level: practitioner
status: draft
description: "Stage, approve, schedule and roll back changes with CloudVision change controls."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CloudVision change control
Goal: safe, auditable network changes.

```
# CloudVision UI
Change Control > New > add Actions (config push, image upgrade, custom script) > Stage order (series/parallel)
> Review > Approve > Execute (or schedule) > Rollback if needed
```

- Actions can be run in series or parallel and gated with approval.
- Snapshots are captured before and after to compare device state.
- Custom actions are Python scripts running on CloudVision (needs approval); examples in the Arista scripts repository.
- Rollback restores the pre-change configuration but not operational state.

Gotcha: a change control that stays unapproved blocks other tasks on the same devices. Always assign an approver.

Operational tip: add a pre-change snapshot action and a post-change validation (BGP, MLAG, EVPN neighbor counts) so a failed state triggers a rollback decision quickly.

## Verify
- The change control summary shows each action as success, and the post-change snapshot matches expectations.
