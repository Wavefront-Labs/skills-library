---
id: computing-software.systems-network-administration.linux.dracut-rdsosreport-early-boot-debug
name: dracut-rdsosreport-early-boot-debug
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, dracut, rdsosreport, rd-debug, emergency-shell, dracut-initqueue-timeout, early-boot, boot-failure]
level: advanced
status: docs-checked
description: "Debug a boot stuck in the dracut emergency shell: read rdsosreport.txt, use rd.debug and udev logging, identify missing root/LVM/LUKS, and save logs off the box."
sources:
  - https://github.com/dracut-ng/dracut-ng/blob/main/man/dracut.cmdline.7.adoc
  - https://github.com/dracut-ng/dracut-ng/blob/main/man/dracut.8.adoc
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Debugging early boot with rdsosreport

**Symptom:** the initramfs cannot find or mount root, waits in the dracut initqueue (`rd.timeout` default is forever), and eventually drops you into an emergency shell where `/run/initramfs/rdsosreport.txt` has been created.

## 1. Read what dracut already captured
At the `dracut:/#` prompt:
```bash
less /run/initramfs/rdsosreport.txt      # cmdline, blkid, lvm, md, udev, journal
blkid ; lsblk
cat /proc/cmdline
```
Look for: the `root=` UUID not appearing in `blkid` (wrong UUID / missing driver), LVs listed by
`lvm lvs` but inactive (`rd.lvm.lv` mismatch), no disks at all (storage driver not in a host-only image). The file contains the logs and the output of some tools; attach it to any dracut bug report.

## 2. Get more detail
Reboot, edit the kernel line in the boot loader and add `rd.debug` (it runs the dracut shell with `set -x`) and `rd.udev.log_level=debug`. The extra logs are included in rdsosreport.txt.

## 3. Get the report off the machine
```bash
mkdir /mnt/usb; mount /dev/sdX1 /mnt/usb; cp /run/initramfs/rdsosreport.txt /mnt/usb/; umount /mnt/usb
```
Or read it via serial console scrollback.

## 4. Common causes → fixes
| Finding | Fix |
|---|---|
| UUID in `root=`/fstab not in blkid | fs recreated/cloned: correct GRUB args + fstab |
| LV exists but inactive | `rd.lvm.lv=` only activates the named LVs: fix the argument (or activate by hand and `exit` to continue) |
| No disk visible | driver missing: boot another kernel/image that has it, then `dracut -f --add-drivers "nvme megaraid_sas"` or `--no-hostonly` |
| LUKS never prompted | `rd.luks.uuid` wrong (`rd.luks=0` disables LUKS detection) or the crypt module missing (`dracut -f --add crypt`) |
| md array inactive | `mdadm --assemble --scan`; rebuild initramfs after updating mdadm.conf |

After a manual fix, leaving the shell lets the boot continue.

## Gotchas
- Hardware/VM migrations (VMware → KVM, new RAID controller) are the classic host-only failure —
  build a generic image before migrating: `dracut -f --no-hostonly`.
- A generic (non host-only) image, if your distribution ships one, is the way back in to rebuild.

## Verify
- [ ] After the fix, `lsinitrd | grep -E 'nvme|dm-crypt|lvm'` shows the needed pieces and a cold boot reaches login without intervention.

## Checked
Checked 2026-10-25 against the dracut-ng man page sources (dracut-ng/dracut-ng man/*.adoc and doc_site, main as of 2026-10-24; latest release 112). Confirmed: `/run/initramfs/rdsosreport.txt` is created on entering the emergency shell and holds the logs and tool output; `rd.debug` (`set -x`), `rd.udev.log_level`, `rd.timeout` default 0 (wait forever), `rd.lvm.lv` and `rd.luks.uuid`/`rd.luks=0` semantics, `--add-drivers`, `--no-hostonly`, `--add`. Removed unconfirmed claims: the exact kernel and dracut warning strings, rescue image naming, and `lvm vgchange` as the fix.

Method: documentation only; no commands were run.
