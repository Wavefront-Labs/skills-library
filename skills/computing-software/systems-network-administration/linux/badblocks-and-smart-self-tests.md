---
id: computing-software.systems-network-administration.linux.badblocks-and-smart-self-tests
name: badblocks-and-smart-self-tests
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, smartctl, smartctl-selftest, smartd, badblocks, disk-health, reallocated-sectors, nvme-smart, disk-burn-in, fsck-repair, lpic-1, sysadmin]
level: practitioner
status: docs-checked
description: "Judge disk health: smartctl attributes and self-tests (short/long), NVMe health logs, smartd alerting, and badblocks scans for burn-in or marking bad sectors on ext4."
sources:
  - https://github.com/smartmontools/smartmontools/blob/main/src/smartctl.8.in
  - https://github.com/smartmontools/smartmontools/blob/main/src/smartd.conf.5.in
  - https://github.com/smartmontools/smartmontools/blob/main/drivedb/drivedb.h
  - https://github.com/tytso/e2fsprogs/blob/master/misc/badblocks.8.in
  - https://github.com/tytso/e2fsprogs/blob/master/e2fsck/e2fsck.8.in
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# badblocks and SMART self-tests

**Goal:** decide whether a disk should be replaced, catch failing disks before they fail, and
burn in new disks before trusting them with data.

## 1. Read SMART
```bash
smartctl -i /dev/sda                  # model, serial, SMART supported/enabled
smartctl -H /dev/sda                  # overall PASSED/FAILED (FAILED = replace now)
smartctl -A /dev/sda                  # attributes
smartctl -a /dev/nvme0                # NVMe device: health information
smartctl -a -d megaraid,2 /dev/sda    # disk behind a MegaRAID controller (also -d sat, -d cciss,N)
```
Attributes that predict failure (raw value > 0 and growing = bad): `5 Reallocated_Sector_Ct`,
`187 Reported_Uncorrect`, `188 Command_Timeout`, `197 Current_Pending_Sector`,
`198 Offline_Uncorrectable`. `199 UDMA_CRC_Error_Count` = cable/backplane, not media.
"PASSED" overall with rising pending/reallocated counts still means replace soon.

## 2. Self-tests
```bash
smartctl -t short /dev/sda            # short self-test (smartctl prints the time estimate)
smartctl -t long /dev/sda             # extended self-test
smartctl -l selftest /dev/sda         # self-test log
smartctl -l error /dev/sda            # ATA error log
```

## 3. smartd (continuous monitoring)
```
# /etc/smartd.conf (smartmontools.conf on some distros)
DEVICESCAN -a -o on -S on -n standby,q -s (S/../.././02|L/../../6/03) -W 4,45,55 -m root@example.com
```
Short test daily 02:00, long test Saturday 03:00 (`-s` regexp is `T/MM/DD/d/HH`, day of week 1-7 from Monday), temperature
warnings (`-W DIFF,INFO,CRIT`), mail on problems (`-m`).

## 4. badblocks
```bash
badblocks -sv /dev/sdb                        # read-only scan (safe on data)
badblocks -nsv /dev/sdb                       # non-destructive read-write (unmounted; slow)
badblocks -wsv -b 4096 /dev/sdb               # DESTRUCTIVE write test — burn-in of new/empty disks only
e2fsck -fcc /dev/sdb1                         # -c twice: non-destructive read-write scan; bad blocks go on the fs bad-block list
```
Drives normally remap bad sectors themselves; errors that badblocks still finds suggest the drive is failing → replace
rather than mark. Burn-in: one long SMART test + one `badblocks -w` pass, then compare SMART attributes before/after.

## Gotchas
- `badblocks` default block size is 1024 bytes (`-b`); it tests 64 blocks at a time by default (`-c`); `-n` and `-w` are mutually exclusive.
- USB enclosures often hide SMART: try `-d sat`.
- Behind hardware RAID controllers use `-d megaraid,N` or `-d cciss,N` where supported.
- SSD wear: watch `Wear_Leveling_Count` or `Media_Wearout_Indicator` where the drive reports them.

## Verify
- [ ] `smartctl -l selftest` shows a recent completed long test with no errors.
- [ ] smartd sends a test mail (`-M test` directive in smartd.conf, restart) to the right address.

## Checked

2026-10-26. smartmontools main (last commit 2026-10-24): smartctl options -i, -H, -A, -a, -t, -l selftest, -l error and -d sat, megaraid,N, cciss,N; drivedb attribute names for IDs 5, 177, 187, 188, 197, 198, 199 and 233; smartd.conf directives -a, -o, -S, -n, -s REGEXP, -W DIFF,INFO,CRIT, -m and -M test. e2fsprogs master (last commit 2026-09-07): badblocks default block size 1024, default 64 blocks at a time, -n and -w exclusive; e2fsck -c twice runs a non-destructive read-write test. Removed the time estimates, NVMe field names, the 16 TB claim, the RAID tool names and the systemctl line. Interpretation of attribute values as failure predictors is practice, not documented thresholds: read it as guidance.

Method: documentation only; no commands were run.
