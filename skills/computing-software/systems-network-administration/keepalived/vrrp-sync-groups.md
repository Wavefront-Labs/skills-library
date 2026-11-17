---
id: computing-software.systems-network-administration.keepalived.vrrp-sync-groups
name: vrrp-sync-groups
category: computing-software
field: systems-network-administration
product: keepalived
tags: [systems-network-administration, keepalived, vrrp, vrrp-sync-group, synchronization, failover]
level: practitioner
status: docs-checked
description: "vrrp_sync_group keeps listed vrrp_instances in the same state so related interfaces fail over together; group block syntax and the case-study behaviour."
sources:
  - https://keepalived.readthedocs.io/en/latest/configuration_synopsis.html
  - https://keepalived.readthedocs.io/en/latest/case_study_failover.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VRRP synchronization groups

```
vrrp_sync_group VG1 {
    group {
        VI_1
        VI_2
    }
}
```
`group` lists instance names (the case study writes the names directly inside the group). Members change state together, which keeps a consistent routing path across, for example, an outside and an inside interface.

Case-study behaviour: if eth0 fails on director 1, VI_1 becomes MASTER on director 2; synchronisation forces VI_2 to BACKUP on director 1, so all four instances end up MASTER on director 2. When eth0 recovers the original distribution returns.

`notify_master`, `notify_backup` and `notify_fault` can also be set on the group.

Verify: break one member's interface and confirm the other member leaves MASTER on the same node.

## Checked

2026-11-04. Confirmed the group syntax and notify_master, notify_backup and notify_fault on the group in the configuration synopsis, the case-study failover sequence, and the guarantee that synchronised instances stay in the same state on the Failover case study and Software Design pages. Nothing removed.

Method: documentation only; no commands were run.
