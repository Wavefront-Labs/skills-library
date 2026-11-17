---
id: computing-software.systems-network-administration.virtualisation.proxmox-memory-ballooning-and-ksm
name: proxmox-memory-ballooning-and-ksm
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pve-ballooning, ksm, proxmox-vm, memory-overcommit, zfs-arc, proxmox]
level: practitioner
status: docs-checked
description: "Configure Proxmox VM memory: minimum vs maximum ballooning, the 80% host threshold, KSM sharing tuning, and the interaction with ZFS ARC and Windows balloon drivers."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-qm.html#qm_memory
  - https://github.com/proxmox/pve-docs/blob/master/kernel-samepage-merging.adoc
  - https://pve.proxmox.com/pve-docs/chapter-sysadmin.html#sysadmin_zfs_limit_memory_usage
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Memory ballooning and KSM on Proxmox VE

## Ballooning settings
VM → Hardware → Memory: **Memory** (maximum) and **Minimum memory** (with "Ballooning
Device" checked).
```sh
qm set 101 --memory 16384 --balloon 4096    # max 16 GB, can shrink to 4 GB
qm set 101 --balloon 0                       # disable the balloon device
```
- If min == max, the balloon device is still useful: it reports guest memory usage to PVE
  (GUI shows real guest usage instead of full allocation).
- When the minimum is lower than the maximum, PVE keeps the minimum available and adds memory up to the maximum while host RAM usage is below the target percentage (default 80%, set per node with `pvenode config set --ballooning-target <percent>`); when the host runs low on RAM the VM releases memory back, swapping processes and invoking the oom killer as a last resort. `--shares` (default 1000, 0 disables auto-ballooning) sets each VM's relative share of the free host memory; auto-ballooning is done by pvestatd.

## Guest requirements
- Linux: all distributions released after 2010 include the balloon kernel driver.
- Windows: the balloon driver must be added manually (see the Proxmox Windows VirtIO Drivers article) and can slow the guest, so the docs do not recommend it on critical systems.

## KSM (Kernel Samepage Merging)
KSM is an optional kernel memory deduplication feature that is enabled by default in Proxmox VE and managed by `ksmtuned`.
```sh
cat /sys/kernel/mm/ksm/pages_sharing     # pages being shared
systemctl status ksmtuned
```
KSM has security implications (side-channel attacks against merged pages); the docs suggest considering disabling it for hosts that run VMs for untrusted users, and checking local regulations. Disable on a node with `systemctl disable --now ksmtuned` and `echo 2 > /sys/kernel/mm/ksm/run` to unmerge, or per VM with `qm set <vmid> --allow-ksm 0` (default 1).

## ZFS ARC interaction
ZFS ARC counts as used host memory, so a large ARC can push the host above the ballooning target. Installations from Proxmox VE 8.1 write an ARC limit of 10% of host memory, at most 16 GiB, to `/etc/modprobe.d/zfs.conf`; older installations used the ZFS default (50%, or 62.5% from ZFS 2.3.0) and need a manual `zfs_arc_max` setting. Set `zfs_arc_max` deliberately and run `update-initramfs -u` afterwards.

## Gotchas
- Overcommit with ballooning can end in the oom killer inside guests or on the host; keep the sum of minimums below host RAM minus host and ARC needs.
- Memory-encrypted (AMD SEV) VMs report host memory usage wrongly and do not support PCI passthrough or snapshots with RAM.

## Verify
Under host pressure, VMs' memory shrinks toward their minimum without guest OOM; the host does not swap heavily; `cat /sys/kernel/mm/ksm/pages_sharing` is non-zero when KSM is active.

## Checked

2026-10-26 against the Proxmox VE admin guide sources (github.com/proxmox/pve-docs master, last commit 2026-10-17: qm.adoc Memory section, kernel-samepage-merging.adoc, pvenode.adoc ballooning-target, local-zfs.adoc Limit ZFS Memory Usage, generated qm.conf.5-opts.adoc balloon, shares and allow-ksm) and confirmed the balloon and shares semantics, the 80% default target and node option, the KSM disable commands and allow-ksm option, and the ARC defaults. Removed the unconfirmed ksmtuned threshold variable, Windows Balloon Service detail and PCI passthrough memory claim.

Method: documentation only; no commands were run.
