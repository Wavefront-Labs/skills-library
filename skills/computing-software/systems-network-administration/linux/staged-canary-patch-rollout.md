---
id: computing-software.systems-network-administration.linux.staged-canary-patch-rollout
name: staged-canary-patch-rollout
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, staged-rollout, canary-patching, patch-management, maintenance-window, ansible-serial, rollback-plan]
level: advanced
status: draft
description: "Roll patches through a fleet in rings: canary hosts, health gates, frozen package snapshots so every ring gets the same versions, Ansible serial batches and rollback triggers."
sources:
  - https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_strategies.html
  - https://docs.redhat.com/en/documentation/red_hat_satellite/6.15/html/managing_content/managing_content_views_content-management
  - https://sre.google/workbook/canarying-releases/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Staged (canary) patch rollout

## Rings
1. **Ring 0** — lab/CI hosts, auto-patched as soon as updates appear.
2. **Ring 1 (canary)** — 1–5% of production, mixed roles, patched day N.
3. **Ring 2** — 25–50%, day N+2 if ring 1 healthy.
4. **Ring 3** — the rest, day N+5. Emergencies (actively exploited CVEs) compress the schedule, not skip the canary.

## Same versions for every ring
If each ring runs `dnf update` on a different day, they get different package sets. Freeze content:
- Satellite/Foreman content views or Pulp publications promoted ring by ring (Library → Canary → Prod).
- Snapshot mirrors: `reposync` into a dated directory, publish `/repo/2026-10-15/`; point rings at a symlink you move.
- Debian: aptly snapshots (`aptly snapshot create ... && aptly publish switch`).

## Execute with Ansible
```yaml
- hosts: "ring2"
  serial: ["10%", "25%", "100%"]     # batches within the ring
  max_fail_percentage: 5
  tasks:
    - ansible.builtin.dnf: { name: "*", state: latest, security: true }
    - ansible.builtin.reboot: { reboot_timeout: 900 }
      when: reboot_needed | default(true)
    - name: Health gate
      ansible.builtin.uri: { url: "http://{{ inventory_hostname }}:8080/health", status_code: 200 }
      retries: 10
      delay: 15
```
Take hosts out of the load balancer before patching (`pre_tasks`), re-add after the health check.

## Health gates between rings
Error rates/latency dashboards, `systemctl --failed` count, kernel taint/oops, app smoke tests, no new alerts for N hours.

## Rollback
`dnf history undo <id>`, boot previous kernel, LVM/Btrfs snapshot taken pre-patch, or rebuild from image.
Decide the rollback trigger before starting.

## Verify
- [ ] Each ring's hosts report identical package versions (`rpm -qa --qf '%{NAME}-%{VERSION}-%{RELEASE}\n' | sort | sha256sum`).
