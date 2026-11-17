---
id: computing-software.systems-network-administration.patch-management.pre-and-post-patch-checks
name: pre-and-post-patch-checks
category: computing-software
field: systems-network-administration
product: patch-management
tags: [pre-patch-checks, post-patch-checks, patch-deployment, health-check, snapshot, service-state, patch-management]
level: practitioner
status: draft
description: "Wrap every patch run in pre-checks (backup age, disk space, pending reboot, snapshot, captured service state) and post-checks (services, events, versions, app probes)."
sources:
  - https://csrc.nist.gov/pubs/sp/800/40/r4/final
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-service
  - https://docs.ansible.com/ansible/latest/collections/ansible/builtin/service_facts_module.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pre-patch and post-patch checks

**Goal:** catch problems caused by patching within minutes, and know the host was healthy before you touched it.

## Pre-checks (abort the host if any fail)
1. Last good backup within policy (query the backup tool API).
2. Free disk: Windows `C:` above ~10 GB for cumulative updates; Linux `/var` and `/boot` with room for new kernels (`df -h /boot`).
3. No pending reboot from earlier work (reboot first).
4. Cluster/HA healthy and redundancy present (other node up, load balancer pool healthy).
5. Capture state:
```powershell
Get-Service | Where-Object Status -eq Running | Select-Object Name | Export-Clixml "$env:TEMP\svc-before.xml"
```
```bash
systemctl list-units --type=service --state=running --no-legend | awk '{print $1}' > /var/tmp/svc-before.txt
```
6. Optional snapshot for fast rollback, with an expiry (delete within 72 hours).

## Post-checks
```powershell
$before = Import-Clixml "$env:TEMP\svc-before.xml"
$now = Get-Service | Where-Object Status -eq Running
Compare-Object $before.Name $now.Name | Where-Object SideIndicator -eq '<='     # services that did not come back
Get-WinEvent -FilterHashtable @{LogName='System'; Level=1,2; StartTime=(Get-Date).AddHours(-2)}
```
```bash
comm -23 /var/tmp/svc-before.txt <(systemctl list-units --type=service --state=running --no-legend | awk '{print $1}')
systemctl --failed
```
- Version check: the intended KB or package release is installed.
- Application probe: HTTP health endpoint, DB connection test, synthetic transaction.
- Return the node to the pool only after probes pass.

## Automate
Put both stages in the patch playbook or runbook so they cannot be skipped; fail the batch (stop the rollout) when post-checks fail on more than a set percentage.

## Verify
Patch reports include pre/post results per host; a deliberately stopped service is flagged by the post-check.
