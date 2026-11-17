---
id: computing-software.systems-network-administration.patch-management.patch-deployment-halt-criteria
name: patch-deployment-halt-criteria
category: computing-software
field: systems-network-administration
product: patch-management
tags: [deployment-halt-criteria, stop-the-line, rollout-pause, patch-deployment, patch-management]
level: practitioner
status: draft
description: "Set and enforce halt criteria for patch deployments: failure-rate thresholds, health signals, who can pause, how to pause in WSUS/Intune/SSM/Ansible and how to resume."
sources:
  - https://learn.microsoft.com/en-us/mem/intune/protect/windows-update-for-business-configure
  - https://docs.aws.amazon.com/systems-manager/latest/userguide/run-command.html
  - https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_error_handling.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Halt criteria for patch deployments

Agree in advance what stops a rollout, so nobody debates it at 02:00.

## Typical halt triggers
| Signal | Threshold |
|---|---|
| Install failures | > 5% of a wave, or any tier-1 server |
| Boot/health failures after reboot | any 2 hosts in the same role |
| Sev-1/2 incident plausibly linked | any |
| Crash/BSOD telemetry | 2x baseline in pilot |
| Vendor pulls or re-releases the update | immediate |
| Change window overrun | maintenance window end minus rollback time |

## Who can halt
Anyone on the patch bridge can call a pause; only the change owner resumes. Write it in the runbook.

## How to pause, per tool
- **Intune / WUfB:** update ring > Pause quality updates (35 days max) or feature updates; Autopatch: pause per ring.
- **WSUS / ConfigMgr:** decline/unapprove the update or disable the deployment; ConfigMgr phased deployments have built-in success criteria to stop moving phases.
- **AWS SSM Run Command / Patch Manager:** `--max-errors 5%` stops new invocations automatically; maintenance window task with `MaxErrors`.
- **Azure Update Manager:** cancel the running maintenance run; remove machines from the config assignment.
- **Ansible:** `serial: "10%"` plus `max_fail_percentage: 5` stops the play; `any_errors_fatal: true` for strict roles.
- **Salt:** `--batch` with `--failhard` on states.

## After halting
1. Freeze the current state; do not roll back blindly.
2. Triage: patch vs coincidence (compare with unpatched peers).
3. Decide: roll back affected, resume with exclusion, or wait for vendor fix.
4. Communicate status to stakeholders with next update time.

## Gotchas
- Automatic thresholds based on small waves trip on one bad host; use absolute minimums too.
- Pausing does not stop devices that already downloaded and staged the update; they may still install at the next reboot.

## Verify
Halt drill run once per year; every real halt has a timeline, decision record and resume approval in the change.
