---
id: computing-software.systems-network-administration.linux.magic-sysrq-and-panic-behaviour
name: magic-sysrq-and-panic-behaviour
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, sysctl, kernel-sysrq, panic-on-oops, sysrq-trigger, kernel-panic, hung-system, reisub]
level: advanced
status: docs-checked
description: "Use and configure Magic SysRq (kernel.sysrq, /proc/sysrq-trigger, REISUB) and panic sysctls (panic, panic_on_oops, hung_task_panic) to recover or capture hung systems."
sources:
  - https://docs.kernel.org/admin-guide/sysrq.html
  - https://docs.kernel.org/admin-guide/sysctl/kernel.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Magic SysRq and panic behaviour

## SysRq
Enable: `sysctl kernel.sysrq=1` (all functions) or a bitmask of allowed functions; `0` disables it. The default comes from `CONFIG_MAGIC_SYSRQ_DEFAULT_ENABLE`, so read it rather than assuming. Persist in `/etc/sysctl.d/90-sysrq.conf`.
Trigger from a shell (always allowed for an admin, even when the bitmask restricts the keyboard): `echo t > /proc/sysrq-trigger`.
Keyboard on x86: Alt+SysRq+<key>; serial: send BREAK, then within 5 seconds the key.

| Key | Action |
|---|---|
| `w` | dump blocked (D-state) tasks — first thing for "hung" systems |
| `t` | dump all task stacks |
| `m` | memory info |
| `l` | backtrace all CPUs |
| `f` | invoke OOM killer |
| `s` / `u` / `b` | sync / remount read-only / reboot immediately |
| `c` | crash (triggers kdump if configured) |
Safe hard reboot sequence: **R E I S U B** (`unraw`, terminate, kill, sync, remount read-only, reboot), one key at a time.

## Panic sysctls
```ini
# /etc/sysctl.d/90-panic.conf
kernel.panic = 10              # reboot 10 s after a panic (0 = do not reboot)
kernel.panic_on_oops = 1       # oops => panic (=> kdump/reboot) instead of limping on
kernel.hung_task_timeout_secs = 120
kernel.hung_task_panic = 0     # panic when this many hung tasks are found in one scan; 1 only where a stuck node must fence itself
kernel.softlockup_panic = 0
vm.panic_on_oom = 0
```
Pair `panic_on_oops=1` with kdump so the reboot leaves a vmcore.

## Gotchas
- `kernel.sysrq` can be a security issue on shared consoles (anyone at the keyboard can reboot).
- `echo b > /proc/sysrq-trigger` reboots without sync or unmount — data loss; use `s`,`u` first.

## Verify
- [ ] `sysctl kernel.sysrq kernel.panic kernel.panic_on_oops` shows intended values; `echo w > /proc/sysrq-trigger` writes stacks to `dmesg`.

## Checked

Checked against the Linux kernel documentation tree (torvalds/linux master, latest commit 2026-10-25) (sysrq, sysctl/kernel) on 2026-10-26. Confirmed: `kernel.sysrq` 0/1/bitmask and its Kconfig default, `/proc/sysrq-trigger` always allowed to admins, keys `w`, `l`, `m`, `f`, `c`, `s`, `u`, `b`, serial BREAK within 5 seconds, `hung_task_panic` (a count threshold), `hung_task_timeout_secs`, `softlockup_panic`, `panic_on_oops`. Removed: Debian/Ubuntu/RHEL default bitmask values, the IPMI key sequence, cloud serial-console claim.

Method: documentation only; no commands were run.
