---
id: computing-software.systems-network-administration.patch-management.linux-reboot-required-and-kernel-version-check
name: linux-reboot-required-and-kernel-version-check
category: computing-software
field: systems-network-administration
product: patch-management
tags: [reboot-required, pending-reboot, needs-restarting, needrestart, reboot-management, linux-patching]
level: practitioner
status: docs-checked
description: "Detect Linux hosts that need a reboot after patching: reboot-required files, needs-restarting -r, running vs newest installed kernel, and reporting across a fleet."
sources:
  - https://man7.org/linux/man-pages/man1/uname.1.html
  - https://dnf-plugins-core.readthedocs.io/en/latest/needs_restarting.html
  - https://github.com/mvo5/unattended-upgrades/blob/master/README.md
  - https://github.com/liske/needrestart
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linux reboot-required detection

A patched-but-not-rebooted kernel, glibc or systemd leaves the vulnerability live.
Scanners checking installed packages say "fixed" while the old kernel runs.

## Debian/Ubuntu
```sh
[ -f /var/run/reboot-required ] && cat /var/run/reboot-required
```
unattended-upgrades treats this file as the signal that a reboot was requested after an
upgrade. needrestart reports services and kernel status; in batch mode `needrestart -b -k`
prints `NEEDRESTART-KCUR` (running kernel), `NEEDRESTART-KEXP` (expected kernel, when it
differs) and `NEEDRESTART-KSTA` (kernel status code); `-r l` lists without restarting.

## RHEL family
```sh
dnf needs-restarting -r     # exit 1 = reboot needed, exit 0 = not needed
dnf needs-restarting -s     # affected systemd services
```

## Universal kernel check
```sh
running=$(uname -r)
# RPM
newest=$(rpm -q --last kernel-core 2>/dev/null | head -1 | awk '{print $1}' | sed 's/^kernel-core-//')
# DEB
newest=$(ls -1 /boot/vmlinuz-* | sed 's#/boot/vmlinuz-##' | sort -V | tail -1)
[ "$running" != "$newest" ] && echo "REBOOT: running $running, newest $newest"
```
Live-patched kernels (kpatch/Livepatch) may legitimately run an old version with fixes
applied; check the live-patching tool's status before flagging.

## Fleet reporting
Ansible:
```yaml
- name: Check reboot needed (RHEL)
  command: dnf needs-restarting -r
  register: nr
  failed_when: false
  changed_when: nr.rc == 1
```
Or a custom node_exporter textfile metric that you define (for example `reboot_required 1`)
with an alert when it has been 1 for longer than the reboot SLA. Uptime above the policy
maximum is a second signal.

## Gotchas
- Containers: reboot-required inside a container is meaningless; the host kernel matters.

## Verify
Fleet report lists zero hosts with running ≠ newest kernel (excluding documented livepatch
hosts) after each patch cycle's reboot window.

## Checked

Checked 2026-10-27 against the dnf-plugins-core needs-restarting page (4.4.2), the unattended-upgrades README, the needrestart manual page and source, and the uname manual page.
- `dnf needs-restarting -r` (exit 1 reboot needed, 0 not) and `-s` (services): confirmed.
- `/var/run/reboot-required` as the reboot signal (unattended-upgrades Automatic-Reboot): confirmed.
- needrestart `-b`, `-k`, `-r l` and the NEEDRESTART-KCUR/KEXP/KSTA batch keys: confirmed.
- Removed unconfirmed: the `.pkgs` file, the numeric KSTA meaning, RHEL 7 yum-utils note, kpatch/Livepatch commands, and the claim about when the reboot file is cleared.
Method: documentation only; no commands were run.
