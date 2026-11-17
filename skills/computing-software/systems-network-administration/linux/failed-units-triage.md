---
id: computing-software.systems-network-administration.linux.failed-units-triage
name: failed-units-triage
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, systemd, failed-units, systemctl-status, systemctl-failed, reset-failed, journalctl, exit-codes, dependency-failure, start-limit, troubleshooting, runbook, sysadmin]
level: practitioner
status: docs-checked
description: "Triage failed systemd units: list them, read status result codes, pull the right journal lines, tell config, dependency, permission and start-limit failures apart, then fix and reset."
sources:
  - https://www.freedesktop.org/software/systemd/man/latest/systemctl.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html
  - https://www.freedesktop.org/software/systemd/man/latest/journalctl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Failed units triage

**Goal:** from "something is red" to the root cause of each failed unit in minutes, with
a repeatable order of checks.

## 1. List
```bash
systemctl --failed                         # = list-units --state=failed
systemctl --failed --all --type=service,mount,socket,timer
systemctl --user --failed                  # user units too
systemctl is-system-running                # degraded = at least one failed unit
```

## 2. Read the status
```bash
systemctl status nginx.service -l --no-pager
```
Key fields: `Active: failed (Result: ...)` (results include `exit-code`, `signal`, `timeout`, `core-dump`, `start-limit-hit`, `resources`, `oom-kill`),
`Main PID ... (code=exited, status=1/FAILURE)`, and the last ~10 journal lines.
| Result | Meaning | Look at |
|---|---|---|
| `exit-code` status=203/EXEC | `execve()` failed, usually a missing or non-executable binary | `ExecStart` path and permissions |
| `exit-code` status=217/USER | `User=` doesn't exist | `getent passwd` |
| `exit-code` status=226/NAMESPACE | sandboxing path missing (`ReadWritePaths=`) | unit hardening |
| `exit-code` status=1 | the app itself failed | app logs/config test |
| `timeout` | start or stop took longer than the unit timeout (`TimeoutStartSec=`) | `Type=` not matching how the daemon starts |
| `signal` / `core-dump` | crash | `coredumpctl info` |
| `start-limit-hit` | restarted too often | the first failure, not the last |
| `resources` | catch-all: a system operation failed | status lines, journal |
| `oom-kill` | memory | `MemoryMax=`, `journalctl -k -g oom` |
| (dependency) | a required unit failed | `systemctl list-dependencies <unit>`, then fix the failed requirement |

## 3. Get the full log of the failure
```bash
journalctl -u nginx -b --no-pager -n 100           # this boot
journalctl -u nginx --since "10 min ago" -o short-precise
journalctl -b -p err                               # all errors this boot — reveals the first failure
systemctl cat nginx; systemd-analyze verify /etc/systemd/system/nginx.service
```

## 4. Fix and recover
```bash
systemctl daemon-reload                    # after editing unit files
systemctl reset-failed nginx               # clear failed state and start-limit counter
systemctl restart nginx && systemctl status nginx
```
Dependency chains: fix the **first** failed unit (often a mount or network-online) — the others follow on restart.
A unit you deliberately don't need: `systemctl disable --now` or `mask` it so it stops showing up.

## Gotchas
- `systemctl status` shows only recent lines and may truncate; always check `journalctl -u`.
- Oneshot units with `RemainAfterExit=no` that succeeded show `inactive (dead)` — not failed.
- Templated units (`getty@tty1`) need the full instance name.

## Verify
- [ ] `systemctl --failed` is empty and `systemctl is-system-running` returns `running`.
- [ ] The fixed unit survives `systemctl restart` and a reboot.

## Checked

2026-10-25, against the systemd v262.1 documentation (man pages and NEWS in the systemd/systemd repository, main branch). Confirmed: `systemctl --failed`, `reset-failed`, `is-system-running` (degraded means at least one failed unit); `$SERVICE_RESULT` values exit-code, signal, timeout, core-dump, start-limit-hit, resources (catch-all), oom-kill; exit statuses 203 EXIT_EXEC, 217 EXIT_USER, 226 EXIT_NAMESPACE (`systemd.exec`); `systemd-analyze verify` takes unit files. Removed the SELinux hint, the quoted dependency job message and the application-specific config-test line.

Method: documentation only; no commands were run.
