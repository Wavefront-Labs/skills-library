---
id: computing-software.systems-network-administration.patch-management.dependent-service-reboot-ordering
name: dependent-service-reboot-ordering
category: computing-software
field: systems-network-administration
product: patch-management
tags: [reboot-ordering, dependency-mapping, patch-reboots, maintenance-window, patch-management]
level: practitioner
status: docs-checked
description: "Order reboots of dependent systems during patching: map dependencies, reboot back-end to front-end in waves, health gates between waves, and ConfigMgr/SSM/Ansible patterns."
sources:
  - https://learn.microsoft.com/en-us/mem/configmgr/sum/deploy-use/service-a-server-group
  - https://learn.microsoft.com/en-us/intune/configmgr/sum/deploy-use/orchestration-groups
  - https://docs.aws.amazon.com/systems-manager/latest/userguide/maintenance-windows.html
  - https://docs.ansible.com/ansible/latest/collections/ansible/builtin/reboot_module.html
  - https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_strategies.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dependent service reboot ordering

Rebooting everything at once in a window produces app outages that look like patch failures: apps start before their database, cluster nodes all drop together, DCs vanish simultaneously.

## Map dependencies
From CMDB relationships, app owner interviews and observed connections (flow records, per-host connection listings), build tiers per application:
```text
Wave 1  infrastructure: 1 of 2 DCs/DNS, then the other; PKI; file servers (one per cluster)
Wave 2  data: DB secondaries -> failover -> DB primaries; message brokers (one node at a time)
Wave 3  middleware/app servers (half, then half behind LB)
Wave 4  web/front-end, RDS/Citrix session hosts (drain first)
```
Rule: **within a redundant pair, never reboot both members in the same wave**.

## Health gates between waves
- Service checks: ports listening, services running, cluster/AG healthy, replication caught up.
- Proceed only when the gate passes; otherwise halt.

## Implementations
- **ConfigMgr**: server group settings on a device collection let you set how many, what percentage, or in what order computers install updates, plus pre- and post-deployment PowerShell scripts. The "maintenance sequence" option updates clients one at a time in the order you list. From version 2002 server groups are replaced by orchestration groups (same idea); all members of a server group must be assigned to the same site.
- **AWS SSM**: Maintenance Windows schedule disruptive actions such as patching; Run Command tasks need one or more targets. Use several tasks with a health-check task between waves (check the Maintenance Windows task priority and target options in the user guide for ordering).
- **Ansible**: `serial` sets how many hosts a play manages at a time and accepts a number or a percentage; the `reboot` module has `reboot_timeout` (default 600 seconds) and `post_reboot_delay` (default 0 seconds):
```yaml
- hosts: db_secondaries
  serial: 1
  tasks:
    - ansible.builtin.reboot: {reboot_timeout: 1800, post_reboot_delay: 60}
- hosts: app
  serial: "50%"
  ...
```
- Add your own health-check task after each play as the gate; the example above does not include one.

## Gotchas
- Hidden dependencies (license servers, SMTP relays, time sources, SQL linked servers) only show when they break; observed traffic beats documentation.
- Boot storms in VDI/VM clusters: stagger even independent hosts.
- Apps that do not reconnect to a restarted DB need their own restart after wave 2.

## Verify
Wave plan documented per app; window report shows gate results between waves; no outage tickets for dependency failures.

## Checked
Date: 2026-11-09. Confirmed against the ConfigMgr server group and orchestration group pages (percentage, count, sequence, scripts, same-site rule, replacement in 2002), the SSM Maintenance Windows overview (patching schedule, Run Command targets), the Ansible reboot module page (reboot_timeout 600 default, post_reboot_delay 0 default) and the Ansible strategies page (serial number and percentage). Removed: the tag name and Priority claim for SSM, wait_for example, repadmin, Cluster-Aware Updating, and named OS commands (not on the cited pages). The wave model is practice advice, not a documented standard.
Method: documentation only; no commands were run.
