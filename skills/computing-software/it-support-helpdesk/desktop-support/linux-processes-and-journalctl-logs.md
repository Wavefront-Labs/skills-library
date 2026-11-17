---
id: computing-software.it-support-helpdesk.desktop-support.linux-processes-and-journalctl-logs
name: linux-processes-and-journalctl-logs
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, linux-client, journalctl, systemctl, ps, top, htop, kill, dmesg, systemd, frozen-desktop, oom-killer, comptia-a-plus, systemd-service-management]
level: practitioner
status: docs-checked
description: "Diagnose hung apps and failing services on Linux desktops with top/ps, systemctl status and --failed, journalctl filters, kernel messages, systemd-oomd and a frozen GUI."
sources:
  - "https://www.freedesktop.org/software/systemd/man/latest/journalctl.html"
  - "https://www.freedesktop.org/software/systemd/man/latest/systemctl.html"
  - "https://www.freedesktop.org/software/systemd/man/latest/journald.conf.html"
  - "https://www.freedesktop.org/software/systemd/man/latest/systemd-oomd.service.html"
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# linux-processes-and-journalctl-logs

Goal: find what's eating the machine or why a service died, from logs not
guesses.

## Processes
```bash
top            # or htop
ps aux
pgrep -a firefox
kill <pid>
pkill -f "some-script.py"
```

## Services (systemd)
```bash
systemctl status cups              # unit state and recent log lines
systemctl --failed                 # only failed units
sudo systemctl restart NetworkManager
systemctl list-timers
```
`systemctl status` shows only the last 10 lines by default; widen with `--lines` and `--full`,
or use `journalctl -u NAME`.

## Logs
```bash
journalctl -b                 # this boot
journalctl -b -1 -p err       # previous boot, errors only (after a crash/reboot)
journalctl -u cups --since "1 hour ago"
journalctl -f                 # follow live while user reproduces
journalctl --user -u pipewire # per-user services (audio)
journalctl -k                 # kernel messages (like dmesg)
```
Previous boots and `--user` need persistent logging: set `Storage=persistent` in
`/etc/systemd/journald.conf` (see `journald.conf`; per-user journals are unsupported without it).

## Memory exhaustion
`systemd-oomd` is systemd's userspace out-of-memory killer; it acts on units that set
`ManagedOOMSwap=` or `ManagedOOMMemoryPressure=`. Check `journalctl -u systemd-oomd` and
`journalctl -k` for what was killed.

## Gotchas
- Restarting the display manager ends the user's session and loses unsaved work; warn them.

## Verify
`systemctl --failed` lists no units, and no new out-of-memory entries appear in `journalctl -k`.

## Checked
2026-11-01. Confirmed in the systemd man pages (journalctl, systemctl, journald.conf,
systemd-oomd.service): -b/-p/-u/--since/-f/--user/-k options, --user needing persistent
storage via Storage=, --failed, list-timers, systemd-oomd role and ManagedOOM directives,
status line limit. Removed: ps sort flags, kill signal notes, load-average and nproc rule, the D-state note,
dmesg and grep recipes, Ctrl+Alt+F3 and gdm recovery steps, /var/log/syslog and distro version
claims, which those pages do not cover.
Method: documentation only; no commands were run.
