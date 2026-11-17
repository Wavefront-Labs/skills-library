---
id: computing-software.systems-network-administration.linux.systemd-debug-shell
name: systemd-debug-shell
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, systemd, debug-shell, early-root-shell, tty9, boot-hang, systemd-debug]
level: advanced
status: docs-checked
description: "Get a root shell on tty9 during a hanging boot with systemd.debug_shell / debug-shell.service, inspect stuck jobs with systemctl list-jobs, then disable it again."
sources:
  - https://www.freedesktop.org/software/systemd/man/latest/systemd-debug-generator.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# systemd debug shell

**When:** boot hangs on a start job and you cannot log in.

## Enable for one boot
Add to the kernel command line for one boot:
```
systemd.debug_shell
```
Boot, then switch to tty9 (Ctrl+Alt+F9): `debug-shell.service` is pulled into the boot transaction and spawns a shell there during early boot. To use another tty, give it as the value, for example `systemd.debug_shell=ttyS0`.

## What to look at
```bash
systemctl list-jobs                 # jobs waiting — the 'running' one blocks the 'waiting' ones
systemctl status <stuck-unit>
journalctl -b -u <stuck-unit>
systemd-analyze critical-chain      # once it eventually finishes
systemctl cancel <job-id>           # unblock boot to get in and fix it
```
## Persistent (temporary!) enable
`systemctl enable debug-shell.service` — remove immediately after debugging:
`systemctl disable --now debug-shell.service`.

## Related kernel args
`systemd.log_level=debug systemd.log_target=console` for verbose boot output;
`systemd.unit=rescue.target` / `emergency.target` to skip most units.

## Verify
- [ ] After the fix, `systemctl is-enabled debug-shell.service` is `disabled` and boot completes without jobs left in `list-jobs`.

## Checked

2026-10-25, against the systemd v262.1 documentation (man pages and NEWS in the systemd/systemd repository, main branch). Confirmed: `systemd.debug_shell` pulls in `debug-shell.service` and spawns a debug shell on tty9 by default, with an optional tty value (`systemd-debug-generator`, `kernel-command-line`); `systemctl list-jobs`, `cancel`, `status`; `systemd-analyze critical-chain`; `systemctl enable debug-shell.service` has existed since v186 (NEWS); `systemd.log_level`, `systemd.log_target`, `systemd.unit=`. Removed the older option spelling, the list of typical causes and the quoted boot message.

Method: documentation only; no commands were run.
