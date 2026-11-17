---
id: computing-software.systems-network-administration.linux.block-io-tracing-blktrace-biosnoop
name: block-io-tracing-blktrace-biosnoop
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, blktrace, blkparse, btt, biosnoop, biotop, iostat, disk-latency, io-troubleshooting, lpic-2, sysadmin]
level: practitioner
status: docs-checked
description: "Trace individual block I/Os when iostat isn't enough: biosnoop/biotop for per-process latency, blktrace/blkparse/btt for queue vs device time, and reading the results."
sources:
  - https://man7.org/linux/man-pages/man8/blktrace.8.html
  - https://man7.org/linux/man-pages/man1/blkparse.1.html
  - https://github.com/iovisor/bcc/blob/master/tools/biosnoop_example.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Block I/O tracing: biosnoop and blktrace

**Goal:** prove whether slow I/O is the device, the queue/scheduler, or one process's access
pattern, per request rather than per-second averages.

## 1. Start with averages
Use `iostat -xz 1` (sysstat) to see per-device wait and utilisation first; if latency is high, trace.
Check the `iostat` man page for the column names on your sysstat version.

## 2. Per-process view (eBPF, bcc)
```bash
biosnoop -Q > bio.txt
```
biosnoop prints one line per I/O with columns `TIME(s) COMM PID DISK T SECTOR BYTES LAT(ms)`; `-Q` adds a `QUE(ms)`
column showing time queued in the OS, so queue time and device latency can be told apart. Install path and tool names
(`biotop`, `biolatency`) vary by distro package; see the bcc tools directory and each tool's `_example.txt`.

## 3. blktrace (kernel block layer events)
```bash
blktrace -d /dev/sdb -o trace -w 30          # -w: run for 30 seconds; per-CPU files trace.blktrace.N
blkparse -i trace -d trace.bin > trace.txt   # human-readable output plus a merged binary stream
blktrace -d /dev/sdb -o - | blkparse -i -    # live: -o - writes to stdout
```
blktrace reads events from debugfs; `-r debugfs_path` names the mount point if it is not the default.
Event letters in blkparse output: `Q` queued, `G` get request, `M` back merge, `F` front merge, `I` inserted into the
I/O scheduler, `D` issued to the driver, `C` completed. Comparing the time between `Q`, `D` and `C` events for the same
sector separates time in the OS from time in the device.

## Gotchas
- Trace for seconds, and write output to a different disk than the one traced; traces grow fast.
- On dm/LVM/multipath, trace the underlying device as well as the dm device.

## Verify
- [ ] The slow requests' process/sector match the workload you suspected (e.g. backup reading).
- [ ] The Q-to-D versus D-to-C split supports the conclusion you send to the storage team.

## Checked
2026-10-28. Confirmed in the blktrace(8) and blkparse(1) man pages and the bcc biosnoop example: `-d`, `-o`, `-o -`, `-w`,
`-r`, `blkparse -i -`, the event letters Q/G/M/F/I/D/C, biosnoop columns and `-Q`. Removed as unconfirmed: iostat column
names, the btt latency labels (Q2C/D2C/Q2D) and `btt -s`, `io.max`, `nr_requests`, the debugfs mount command, the
one-session-per-device claim, flush/FUA reading, bcc paths and the biotop/biolatency flags.
Method: documentation only; no commands were run.
