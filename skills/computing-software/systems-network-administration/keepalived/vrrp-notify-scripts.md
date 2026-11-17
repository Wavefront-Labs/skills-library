---
id: computing-software.systems-network-administration.keepalived.vrrp-notify-scripts
name: vrrp-notify-scripts
category: computing-software
field: systems-network-administration
product: keepalived
tags: [systems-network-administration, keepalived, vrrp, notify-master, notify-backup, notify-fault, notify-scripts, state-transition]
level: practitioner
status: docs-checked
description: "notify_master, notify_backup and notify_fault run a script (with optional arguments) on VRRP state transitions, in a forked process; valid in instances and sync groups."
sources:
  - https://keepalived.readthedocs.io/en/latest/configuration_synopsis.html
  - https://keepalived.readthedocs.io/en/latest/software_design.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Notify scripts

Keywords: `notify_master`, `notify_backup`, `notify_fault`. Each takes a script path, optionally with arguments, run when the instance enters that state:
```
notify_master /path/to/transit.sh <arg_list>
```
They are valid in both `vrrp_instance` and `vrrp_sync_group`.

Design note: scripts run in a forked process so the VRRP timer is not disturbed, so keep them short and do not depend on them finishing before the next advertisement.

The synopsis lists only these three; it does not document a generic notify keyword or the arguments passed.

Verify: force a transition and confirm the script ran (log or side effect) for the expected state.

## Checked

2026-11-04. Confirmed the three keywords, the quoting of arguments and their presence in both blocks on the configuration synopsis page, and the forked-process execution on the Software Design page. Removed the claim about when group scripts fire, which the pages do not state.

Method: documentation only; no commands were run.
