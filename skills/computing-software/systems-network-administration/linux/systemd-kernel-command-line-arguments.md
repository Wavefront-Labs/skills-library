---
id: computing-software.systems-network-administration.linux.systemd-kernel-command-line-arguments
name: systemd-kernel-command-line-arguments
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, systemd, systemd-unit-kernel-param, systemd-log-level, kernel-cmdline, systemd-mask, rescue-target, boot-debug]
level: advanced
status: docs-checked
description: "Steer systemd from the kernel command line: systemd.unit=, systemd.mask=, systemd.log_level/log_target, systemd.show_status, emergency/rescue shortcuts and fsck.mode."
sources:
  - https://www.freedesktop.org/software/systemd/man/latest/kernel-command-line.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd-debug-generator.html
  - https://docs.kernel.org/admin-guide/kernel-parameters.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# systemd kernel command-line arguments

Add these to the kernel command line in your boot loader (for one boot, or persistently).

## Choosing what boots
| Argument | Effect |
|---|---|
| `systemd.unit=rescue.target` (or `1`, `single`, `s`) | rescue shell with all file systems mounted and only the most basic services |
| `systemd.unit=emergency.target` (or `emergency`, `-b`) | emergency shell, much more reduced than rescue: no file systems or most basic services |
| `systemd.unit=multi-user.target` (or `3`) | skip the graphical session |
| `systemd.mask=foo.service` | mask a unit for this boot (debug generator) |
| `systemd.wants=debug-shell.service` | pull in an extra unit |
| `systemd.debug_shell` | root shell on tty9 |

## Debug output
| Argument | Effect |
|---|---|
| `systemd.log_level=debug` | PID 1 debug logging |
| `systemd.log_target=console` / `kmsg` | where PID 1 logs go |
| `systemd.show_status=1` / `0` | enable / disable status messages on the console |
| `systemd.journald.forward_to_console=1` | journal to console |
| `printk.devkmsg=on` | do not rate-limit userspace writes to `/dev/kmsg` (kernel default: `ratelimit`) |

## Filesystems and misc
`fsck.mode=force|skip`, `fsck.repair=yes|no|preen`, `systemd.gpt_auto=0`, `rd.systemd.unit=` (initramfs),
`systemd.firstboot=off`, `systemd.machine_id=`.

## Verify
- [ ] `cat /proc/cmdline` shows the args; `systemctl get-default` unchanged (cmdline overrides only this boot).

## Checked

2026-10-25, against the systemd v262.1 documentation (man pages and NEWS in the systemd/systemd repository, main branch). Confirmed: `systemd.unit=` (default `default.target`, can select rescue or emergency), compatibility words `1 2 3 4 5 s S single emergency -b`, `systemd.mask=`, `systemd.wants=`, `systemd.debug_shell` (tty9), `systemd.log_level=`/`log_target=console|kmsg`, `systemd.show_status=1|0`, `systemd.journald.forward_to_console`, `fsck.mode=auto|force|skip` and `fsck.repair=preen|yes|no` (`systemd-fsck@.service`), `systemd.gpt_auto=`, `rd.systemd.unit=`, `systemd.firstboot=`, `systemd.machine_id=` (`kernel-command-line`); `printk.devkmsg={on,off,ratelimit}` default `ratelimit` (kernel parameters). Removed GRUB and grubby specifics, the SYSTEMD_SULOGIN_FORCE remark and the serial-console remark.

Method: documentation only; no commands were run.
