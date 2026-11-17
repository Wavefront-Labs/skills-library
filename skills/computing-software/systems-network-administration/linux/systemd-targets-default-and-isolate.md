---
id: computing-software.systems-network-administration.linux.systemd-targets-default-and-isolate
name: systemd-targets-default-and-isolate
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, systemd, systemd-targets, default-target, set-default, isolate, systemctl-isolate, multi-user-target, graphical-target, runlevels, rescue-target, rhcsa, lpic-1, sysadmin]
level: practitioner
status: docs-checked
description: "Choose and switch boot targets: get/set the default target, multi-user vs graphical, switch live with systemctl isolate, and the runlevel mapping still asked about in exams."
sources:
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.special.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemctl.html
  - https://www.freedesktop.org/software/systemd/man/latest/bootup.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Targets: default, isolate, multi-user vs graphical

**Goal:** make a server boot to text mode (or a workstation to GUI), switch targets without
rebooting, and know what each standard target pulls in.

## 1. The standard targets
| Target | Meaning |
|---|---|
| `rescue.target` | single-user mode: base system and all file systems mounted, a rescue shell, almost no services |
| `multi-user.target` | non-graphical multi-user system; runlevels 2, 3, 4 map here |
| `graphical.target` | `multi-user.target` plus the display manager (`Wants=display-manager.service`); runlevel 5 maps here |
| `emergency.target` | much more reduced than rescue: no file systems or most basic services |

`graphical.target` has `Requires=multi-user.target`. The runlevel mapping 2, 3, 4 to `multi-user.target` and 5 to `graphical.target` is hard-coded (NEWS, v220).

## 2. Default target
```bash
systemctl get-default
systemctl set-default multi-user.target     # server: no GUI at boot
systemctl set-default graphical.target
ls -l /etc/systemd/system/default.target    # set-default just rewrites this symlink
```
One-boot override: add `systemd.unit=multi-user.target` (or `rescue.target`, `emergency.target`) to the kernel command line; legacy `3`, `1`, `single` also work.

## 3. Switch now
```bash
systemctl isolate multi-user.target   # stops the display manager and everything not wanted by the target
systemctl isolate graphical.target    # starts GUI again
systemctl rescue                      # = isolate rescue.target
systemctl emergency
```
Only units with `AllowIsolate=yes` can be isolated (`graphical.target` and `emergency.target` set it; custom targets need it explicitly). `isolate` **stops** units not required by the new target — running it
over SSH to `rescue.target` drops your session and the network.

## 4. Inspect what a target brings up
```bash
systemctl list-dependencies multi-user.target          # tree
systemctl list-dependencies --reverse sshd.service    # which targets want sshd
systemctl list-units --type=target                     # active targets now
ls /etc/systemd/system/multi-user.target.wants/        # what `enable` linked in
```

## Gotchas
- `systemctl enable` uses the unit's `[Install] WantedBy=` — a service wanted only by
  `graphical.target` won't start on a multi-user server.

## Verify
- [ ] `systemctl get-default` shows the intended target; after reboot
      `systemctl list-units --type=target --state=active` includes it.
- [ ] On a server, `systemctl is-active display-manager` is inactive after reboot.

## Checked

2026-10-25, against the systemd v262.1 documentation (man pages and NEWS in the systemd/systemd repository, main branch). Confirmed: `rescue.target` and `emergency.target` descriptions (`systemd.special`); `systemctl rescue`/`emergency` equal `isolate`; `set-default`/`get-default` symlink `default.target`; `isolate` stops units not required by the new target; `graphical.target` unit file (`Requires=multi-user.target`, `Wants=display-manager.service`, `AllowIsolate=yes`); runlevel numbers 2-5 mapping (NEWS v220); kernel command-line words `1 2 3 4 5 s single emergency`. Removed the runlevel 0/1/6 column, the runlevelN.target symlink claim and the telinit remark, which current documentation does not state.

Method: documentation only; no commands were run.
