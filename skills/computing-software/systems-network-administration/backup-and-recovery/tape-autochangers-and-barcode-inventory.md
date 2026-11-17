---
id: computing-software.systems-network-administration.backup-and-recovery.tape-autochangers-and-barcode-inventory
name: tape-autochangers-and-barcode-inventory
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [autochanger, mtx, tape-library, barcode, bacula-autochanger, tape]
level: advanced
status: docs-checked
description: "Operate tape libraries from Linux: find the changer with lsscsi, mtx status/load/unload/transfer, and Bacula autochanger and slot configuration."
sources:
  - https://linux.die.net/man/1/mtx
  - https://www.bacula.org/15.0.x-manuals/en/main/Autochanger_Support.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Autochangers and barcode inventory

**Goal:** drive a tape library reliably from the command line and the backup software.

## Find the devices
```bash
lsscsi -g
```
`lsscsi -g` lists SCSI devices; the changer shows as type `mediumx` with a generic `/dev/sgN` device, tape drives as `tape` with `/dev/stN`. The generic SCSI device is what `mtx -f` and Bacula's Changer Device use, while the tape device is the Archive Device. Make sure the Storage daemon has permission to access the changer device.

## mtx
`mtx [-f <scsi-generic-device>] command ...` controls SCSI media changers. Drives are numbered from 0 and storage slots from 1. If the drive number is omitted it defaults to drive 0.
```bash
mtx -f /dev/sg2 status          # drives, storage slots, import/export slots, volume tags
mtx -f /dev/sg2 inventory       # robot checks which elements are in the slots
mtx -f /dev/sg2 load 5 0        # slot 5 -> drive 0
mtx -f /dev/sg2 unload 5 0      # drive 0 -> slot 5
mtx -f /dev/sg2 transfer 5 24   # slot to slot, usually to or from an import/export port
```
- `status` reports for each drive whether media is loaded and which slot it came from, and for each slot whether it is empty or full, plus volume tags when the changer can read barcodes. `nobarcode` makes the loader not request barcodes.
- `inventory` is needed for a few libraries that do not check their inventory at startup.
- You may need to eject the tape with the OS tape tools before `mtx unload`.
- `eepos` extends or retracts the import/export tray on some libraries; its values 1 and 2 vary by library.

## Bacula autochanger
Bacula's Device resource uses `Autochanger = yes`, `Changer Device`, `Changer Command` and `Maximum Changer Wait` (default 120 seconds). The documented example command is:
```text
Changer Command = "/opt/bacula/scripts/mtx-changer %c %o %S %a %d"
```
(%c changer device, %o command, %S slot base 1, %a archive device, %d drive index base 0). Adapt the path to where the mtx-changer script lives.
- Multi-drive changers: group the Device resources in an Autochanger resource and have the Director's Storage resource reference the Autochanger. Set `Drive Index` (from 0) in each Device; later drives share the Changer Device but have a different Archive Device.
- Every Volume must be labelled and have a slot and the InChanger flag in the catalog; with a slot of zero or none Bacula will not use the changer. Use the Console `label barcodes` and `update slots` commands for barcode-equipped changers, and `list Volumes` to check slot and InChanger.
- Test the changer with the `auto` command in `btape`.

## Verify
`mtx status` volume tags match the backup software's slot inventory, and a load and unload cycle works on every drive.

## Checked

2026-11-09. Confirmed against the mtx man page (options, status, inventory, load, unload, transfer, eepos, defaults) and the Bacula 15.0.x "Autochanger Support" chapter (lsscsi example, Device directives, Changer Command example, Drive Index, Autochanger resource, slots, `label barcodes`, `update slots`, btape `auto`). Partial read: some lines on the Bacula page are elided. Removed: LTO barcode format and generation codes, CLN cleaning-tape convention, persistent `/dev/tape/by-id` names, `mt` commands, `Media Type`, and the two-programs-one-changer and drive-order gotchas (not stated).

Method: documentation only; no commands were run.
