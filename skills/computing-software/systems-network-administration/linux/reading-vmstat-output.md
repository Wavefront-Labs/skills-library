---
id: computing-software.systems-network-administration.linux.reading-vmstat-output
name: reading-vmstat-output
category: computing-software
field: systems-network-administration
product: linux
tags: [vmstat, linux-performance, run-queue, swap, iowait]
level: practitioner
status: docs-checked
description: "Read vmstat for CPU, run queue, memory, swap and I/O pressure on Linux, interpret each column, and know what the first line means."
sources: ["https://man7.org/linux/man-pages/man8/vmstat.8.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading vmstat

**Goal:** a 30-second check of saturation across CPU, memory and I/O.

## Run
```bash
vmstat 1 10        # one-second samples, ten of them
vmstat -w -S M 1   # wide output, megabytes
vmstat -s          # table of event counters and memory statistics
vmstat -d          # per-disk statistics
```
The FIRST report gives averages since the last reboot; later reports cover the sampling period (the delay). Ignore the first for current behaviour, or omit it with `-y`. The process and memory columns are instantaneous in every report.

## Columns
- `procs r`: runnable processes (running or waiting for run time). Sustained `r` above the CPU count is a common sign of CPU saturation. `b`: processes blocked waiting for I/O to complete.
- `memory swpd free buff cache`: swap used, idle memory, memory used as buffers, memory used as cache. The unit follows `-S` (k, K, m or M). Because cache and buffers count as used, judge pressure by `si/so`, not by `free`.
- `swap si so`: memory swapped in from disk and out to disk, per second. Sustained nonzero values suggest memory pressure.
- `io bi bo`: KiB per second received from and sent to block devices. `-S` does not change these fields.
- `system in cs`: interrupts (including the clock) and context switches per second.
- `cpu us sy id wa st`: percentages of total CPU time for non-kernel code (user, including nice), kernel code (system), idle, waiting for I/O, and time stolen from a virtual machine. High `sy` points to kernel load; high `wa` means time spent waiting for I/O; high `st` means the VM is losing CPU time to its host.

## Quick diagnoses
- r high, id near 0, us high: CPU bound; profile the app.
- b high and wa high with bi/bo high: disk bound; look at per-disk figures with `vmstat -d` or iostat.
- si/so sustained: memory shortage; find the largest memory users or fix the leak.
- st high: resize or move the VM.

## Verify
Change one thing (add memory, move a job) and re-run vmstat to see the specific column move.

## Checked

Confirmed against the vmstat(8) manual page on man7.org, read in full: the options used (`-w`, `-S`, `-s`, `-d`, `-y`), first-report semantics, and every column description. Removed the claims that `b` means uninterruptible sleep, that high `cs` implies lock contention, the page-cache explanation and the `ps` sort example, and changed the bi/bo unit to KiB per second as the page states. The diagnosis list is practitioner rule of thumb, not manual text.

Method: docs-checked 2026-11-09 against https://man7.org/linux/man-pages/man8/vmstat.8.html
