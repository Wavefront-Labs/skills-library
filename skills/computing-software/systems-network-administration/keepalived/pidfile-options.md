---
id: computing-software.systems-network-administration.keepalived.pidfile-options
name: pidfile-options
category: computing-software
field: systems-network-administration
product: keepalived
tags: [systems-network-administration, keepalived, pidfile, command-line, vrrp-pid, checkers-pid, init-script]
level: practitioner
status: docs-checked
description: "Keepalived pidfile defaults and options: -p parent, -r VRRP child, -c checker child, with the default /var/run paths."
sources:
  - https://keepalived.readthedocs.io/en/latest/programs_synopsis.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pidfile options

Three processes, three pidfiles:

| Option | Process | Default |
|---|---|---|
| `-p`, `--pid=FILE` | parent | /var/run/keepalived.pid |
| `-r`, `--vrrp_pid=FILE` | VRRP child | /var/run/keepalived_vrrp.pid |
| `-c`, `--checkers_pid=FILE` | checker child | /var/run/keepalived_checkers.pid |

Override them when your init script expects a different location. Keep the init script and the daemon options in agreement.

Verify: the files exist at the chosen paths after start and contain the PIDs seen in the process list.

## Checked

2026-11-04. Confirmed the three options and their default paths on the Keepalived programs synopsis page, and the parent plus two children layout on the Software Design page. Removed the multiple-instances suggestion, which the page does not make.

Method: documentation only; no commands were run.
