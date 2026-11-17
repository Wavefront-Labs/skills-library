---
id: computing-software.systems-network-administration.virtualisation.qemu-img-disk-format-conversion
name: qemu-img-disk-format-conversion
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [qemu-img, disk-format-conversion, vmdk, qcow2, vhdx, vpc, raw, v2v]
level: practitioner
status: docs-checked
description: "Convert virtual disks between VMDK, QCOW2, VHD(X) and raw with qemu-img, including Azure fixed-VHD sizing, sparse handling, and integrity checks."
sources:
  - https://www.qemu.org/docs/master/tools/qemu-img.html
  - https://learn.microsoft.com/en-us/azure/virtual-machines/linux/create-upload-generic
  - https://github.com/qemu/qemu/blob/master/docs/system/qemu-block-drivers.rst.inc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Convert disk formats with qemu-img

**Goal:** move a disk image between hypervisors or clouds without corrupting it.

## Inspect first
```bash
qemu-img info app01.vmdk            # format, virtual size, backing file, subformat
qemu-img check app01.qcow2          # qcow2/vhdx/vdi consistency
```
Only `qcow2`, `qed`, `parallels`, `vhdx`, `vmdk` and `vdi` support `qemu-img check`.

## Common conversions
```bash
qemu-img convert -p -f vmdk  -O qcow2 app01.vmdk app01.qcow2
qemu-img convert -p -f qcow2 -O vhdx -o subformat=dynamic app01.qcow2 app01.vhdx
qemu-img convert -p -f vhdx  -O raw   app01.vhdx  app01.raw
qemu-img convert -p -f raw   -O vmdk  -o adapter_type=lsilogic,subformat=streamOptimized app01.raw app01.vmdk
```
Add `-c` for compressed output (qcow/qcow2, or vmdk with the streamOptimized subformat only), `-m N` to change the number of parallel coroutines (default 8). `-W` allows out-of-order writes; the manual recommends it only for preallocated targets such as raw block devices, and it cannot be combined with compression.

## Azure: fixed VHD on a 1 MiB boundary
```bash
qemu-img convert -f raw -O vpc -o subformat=fixed,force_size app01.raw app01.vhd
```
Azure requires the VHD virtual size to be a multiple of 1 MB, so resize the raw image up to a whole MB first if needed (`qemu-img resize -f raw app01.raw <size rounded up>`). Azure's guidance for QEMU 2.6 and later is to pass `force_size` with `subformat=fixed`; without it the VHD geometry can differ from the actual size.

## Gotchas
- Only the disk changes; drivers inside the guest do not (see v2v driver fixups). Windows guests moving to virtio need drivers before or after.
- Never convert a disk in use; snapshot or power off first.
- qcow2 with a backing file: convert the top image to flatten the chain (`-O qcow2` output has no backing file unless `-b` is given).

## Verify
`qemu-img info` on the output shows the expected virtual size, and `qemu-img compare src dst` reports images identical.

## Checked

Checked 2026-10-27 against the QEMU master documentation (docs/tools/qemu-img.rst and docs/system/qemu-block-drivers.rst.inc), QEMU source for the vpc and vmdk create options (block/vpc.c, block/vmdk.c) and Microsoft's Linux VHD preparation article. Confirmed: the convert synopsis (`-c`, `-p`, `-m` default 8, `-W` scope and the compression limit, `-b` for a backing file), check support by format, `subformat=dynamic|fixed` for vpc, the vmdk subformats including streamOptimized, the vmdk `adapter_type` values, the `force_size` vpc option, `compare`, and Azure's 1 MB virtual-size alignment and fixed-VHD requirement. Removed the unconfirmed ESXi `scp` remark.

Method: documentation only; no commands were run.
