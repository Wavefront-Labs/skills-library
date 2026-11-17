---
id: computing-software.cloud-infrastructure-engineering.kubespray.upgrade-batch-size-and-pauses
name: upgrade-batch-size-and-pauses
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [upgrade, serial, pause, confirm, uncordon]
level: advanced
status: docs-checked
description: "Control rollout speed in upgrade-cluster.yml with serial and pause the run before or after each node using the upgrade_node_* confirm and pause_seconds variables."
sources:
  - https://kubespray.io/docs/operations/upgrades.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default upgrade-cluster.yml upgrades nodes in batches of 20% of the available nodes. Change the Ansible `serial` variable to alter this; `serial=1` upgrades one node at a time:

```ShellSession
ansible-playbook upgrade-cluster.yml -b -i inventory/sample/inventory.ini -e kube_version=1.20.7 -e "serial=1"
```

You can pause for manual control.

**Before upgrading each node** (to inspect pods or do manual actions):
- `upgrade_node_confirm: true` pauses until you type "yes" at the terminal.
- `upgrade_node_pause_seconds: 60` pauses 60 seconds, then resumes automatically.

**After upgrading each node, before uncordoning** (to reboot for kernel updates or test the still-cordoned node):
- `upgrade_node_post_upgrade_confirm: true` waits for a manual "yes".
- `upgrade_node_post_upgrade_pause_seconds: 60` waits 60 seconds.

## Checked

2026-11-04. Default batch size, the serial example and all four pause variables were confirmed on the Upgrading page. Removed an unattended-run remark the page does not make.

Method: documentation only; no commands were run.
