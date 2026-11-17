---
id: computing-software.systems-network-administration.backup-and-recovery.tape-drive-status-mt-and-tapeinfo
name: tape-drive-status-mt-and-tapeinfo
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [mt-st, tapeinfo, tape, lto, autochanger, mtx]
level: practitioner
status: gated
description: "Operate and diagnose LTO tape drives on Linux: nst vs st and sg devices, mt status and positioning, tapeinfo TapeAlert flags, sg_logs, and library moves with mtx."
sources:
  - https://linux.die.net/man/1/tapeinfo
  - https://linux.die.net/man/1/mtx
  - https://github.com/iustin/mt-st
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Tape drive status with mt and tapeinfo

## Devices
- The Linux SCSI tape driver provides auto-rewind devices (`/dev/st0`) and non-rewind devices (`/dev/nst0`; minor number is 128 plus the device number). Use **`/dev/nst0`** for multi-file tapes and backup software, because the `st` device rewinds on close.
- `/dev/sgN`: SCSI generic, used by tapeinfo and mtx (`tapeinfo -f` takes the SCSI generic device).

## mt (package mt-st)
```sh
mt -f /dev/nst0 status         # print status information about the tape unit
mt -f /dev/nst0 rewind
mt -f /dev/nst0 fsf 2          # forward 2 files
mt -f /dev/nst0 eod            # to end of data (append)
mt -f /dev/nst0 setblk 0       # setting the block size to zero puts the drive in variable block mode
mt -f /dev/nst0 erase          # long erase: can take many hours and usually cannot be aborted; count 0 = non-secure quick erase if the drive supports it
mt -f /dev/nst0 offline        # rewind and, if applicable, unload
```
Counts take the postfix `k`, `M` or `G`. Not all operations work on all drives. `setblk` is for SCSI tapes and, per the mt manual, the block size set by `setblk` overrides the default until a new tape is inserted (superuser only).

## tapeinfo (package mtx)
```sh
tapeinfo -f /dev/sg3
```
`tapeinfo` reads various information from SCSI tape drives and, on drives that support TapeAlert, reports a more exact description of what went wrong. Use the T10 TapeAlert definitions or the drive vendor's table to interpret individual flag numbers (gated: unconfirmed, source is paywalled or blocked), because they are not on the readable pages.
## Deeper diagnostics (sg3_utils)
```sh
sg_logs /dev/sg3               # SCSI log pages
sg_inq /dev/sg3
```
The sg3_utils man pages (not read for this check) list the available log pages and options.

## Library moves (mtx)
```sh
mtx -f /dev/sg4 status         # slots and drives
mtx -f /dev/sg4 load 12 0      # slot 12 -> drive 0
mtx -f /dev/sg4 unload 12 0
mtx -f /dev/sg4 transfer 12 40 # slot to slot
mtx -f /dev/sg4 inventory      # robot arm checks slot contents
```
`status` reports drive and slot counts and whether each is full or empty (drives numbered from 0, slots from 1); `load <slot> [drive]` assumes drive 0 if omitted; `unload [slot] [drive]` returns the tape to its source slot if the slot is omitted; `inventory` makes the robot arm check slot contents. Let backup software own moves in normal operation.

## Gotchas
- `/dev/st0` rewinds when closed, so backup software that closes the device between files will not append correctly; use `/dev/nst0`.
- Check generation compatibility and firmware levels with the drive vendor; they are not covered by the mt or mtx manuals.

## Verify
`tapeinfo` shows no TapeAlert flags after cleaning; `mtx status` barcodes match the backup
catalog; a write/read verify job passes.

## Checked

Checked 2026-10-27 against the mt-st manual (iustin/mt-st), the Linux kernel SCSI tape driver documentation (Documentation/scsi/st.rst) and the mtx and tapeinfo manual pages. Confirmed: auto-rewind and non-rewind tape devices, the `mt` operations `status`, `rewind`, `fsf`, `eod`, `setblk` (zero selects variable block mode), `erase` (long erase, count 0 for quick erase) and `offline`, `tapeinfo -f` taking the SCSI generic device, and the `mtx` `status`, `load`, `unload`, `transfer` and `inventory` semantics. Gated: interpretation of individual TapeAlert flag numbers, which are not on the readable pages. Removed the unconfirmed persistent by-id names, `lsscsi`, example product string, LTO generation compatibility rule and backup-product command remarks.

Method: documentation only; no commands were run.
