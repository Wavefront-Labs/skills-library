---
id: computing-software.systems-network-administration.linux.signals-sigterm-sigkill-sighup
name: signals-sigterm-sigkill-sighup
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, signals, kill, sigterm, sigkill, sighup, sigint, sigstop, sigcont, sigusr1, graceful-shutdown, lpic-1, rhcsa, sysadmin]
level: practitioner
status: docs-checked
description: "Choose the right signal: SIGTERM vs SIGKILL escalation, SIGHUP reloads, SIGSTOP/SIGCONT, SIGUSR1/2 conventions, and why some processes ignore kill -9."
sources:
  - https://man7.org/linux/man-pages/man7/signal.7.html
  - https://man7.org/linux/man-pages/man1/kill.1.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.kill.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Signals: what each one does and when to send it

**Goal:** stop, reload or pause processes without corrupting data, and know what to do when
they don't respond.

## 1. The signals that matter
| # | Name | Default | Use |
|---|---|---|---|
| 1 | SIGHUP | terminate | terminal closed; by convention many daemons **reload config** (check the daemon's docs) |
| 2 | SIGINT | terminate | Ctrl-C |
| 3 | SIGQUIT | core dump | Ctrl-\ |
| 9 | SIGKILL | terminate | cannot be caught/ignored — last resort |
| 15 | SIGTERM | terminate | polite stop; default for `kill` and systemd |
| 10/12 | SIGUSR1/2 | terminate | app-defined; check the program's documentation |
| 17 | SIGCHLD | ignore | child exited |
| 18/19 | SIGCONT/SIGSTOP | continue/stop | pause a runaway without killing; STOP can't be caught |
| 20 | SIGTSTP | stop | Ctrl-Z |
`kill -l` lists names/numbers (numbers differ on non-x86 architectures — use names).

## 2. Graceful stop with escalation
```bash
kill -TERM 1234; sleep 30; kill -0 1234 && kill -KILL 1234
systemctl stop app       # TERM to main process (KillMode=control-group: whole cgroup), then KILL after TimeoutStopSec (default from DefaultTimeoutStopSec)
kill -HUP $(cat /run/<daemon>.pid)    # reload; check the daemon's docs — some just die on HUP
kill -STOP 1234; kill -CONT 1234   # freeze/thaw (e.g. while you take a snapshot)
kill -0 1234 && echo alive         # existence/permission test, sends nothing
```
SIGKILL skips cleanup: no buffer flush, temp files and lock files remain, DB may need
recovery, children may be orphaned. Always TERM first and wait.

## 3. When kill -9 "doesn't work"
- **State D** (uninterruptible sleep): blocked in the kernel on I/O (dead NFS server, failing
  disk). The signal is delivered when the syscall returns. Fix the I/O (bring the
  storage back) or reboot. `cat /proc/PID/stack` (root) shows where it waits.
- **Zombie (Z)**: already dead; only its parent can reap it. Signal/restart the PPID.
- **PID 1**: signals it has no handler for are ignored; check your init's documentation.
- Permission: you can only signal your own processes unless root (`EPERM`).

## 4. Inspect handling
```bash
grep -E 'Sig(Blk|Ign|Cgt)' /proc/1234/status   # hex masks: blocked, ignored, caught
```
Bit n-1 set = signal n. A process ignoring SIGTERM (bit 14 in SigIgn) needs another method.

## Gotchas
- Shell scripts: `trap 'cleanup' TERM INT EXIT` or they leave temp files on stop.
- `kill -9 -1` as root kills everything you're allowed to — including your session.

## Verify
- [ ] After `kill -TERM`, the process exits within its normal shutdown time and logs a clean stop.
- [ ] After `kill -HUP` for reload, the PID is unchanged and the new config is in effect.

## Checked

Checked 2026-10-27 against Linux man-pages (capabilities(7), signal(7), proc(5), kill(2), xattr(7); mkerrisk/man-pages master), systemd systemd.kill, systemd.service and systemd.exec man pages, 2026-10-27. Confirmed: signal names, default actions and numbers (architecture-dependent), SIGKILL and SIGSTOP uncatchable, kill -0, kill -1 semantics, systemd KillMode=control-group and SIGTERM then SIGKILL after TimeoutStopSec, /proc/PID/status SigBlk/SigIgn/SigCgt and /proc/PID/stack, uninterruptible sleep state. Removed or softened: nginx/dd/JVM signal conventions, nohup remark, tini advice, umount flags, the 90 s figure.

Method: documentation only; no commands were run.
