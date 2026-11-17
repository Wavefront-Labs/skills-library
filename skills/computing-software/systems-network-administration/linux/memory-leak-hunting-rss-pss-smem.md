---
id: computing-software.systems-network-administration.linux.memory-leak-hunting-rss-pss-smem
name: memory-leak-hunting-rss-pss-smem
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, memory, memory-leak, smem, pss, rss, uss, smaps-rollup, pmap, valgrind, heaptrack, lpic-2, sysadmin]
level: practitioner
status: docs-checked
description: "Find which process is leaking memory and prove it: RSS vs PSS vs USS, smem and smaps_rollup sampling over time, pmap for growing mappings, and handing evidence to developers."
sources:
  - https://www.kernel.org/doc/html/latest/filesystems/proc.html
  - https://manpages.debian.org/trixie/smem/smem.8.en.html
  - https://github.com/sysstat/sysstat/blob/master/man/pidstat.1
  - https://github.com/iovisor/bcc/blob/master/man/man8/memleak.8
  - https://valgrind.org/docs/manual/mc-manual.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hunting memory leaks: RSS, PSS, smem

**Goal:** identify the process whose memory grows without bound, show the growth with data,
and narrow it to heap vs mapped files vs threads.

## 1. Pick the right metric
- **RSS**: resident pages, counting shared pages fully in every process — summing over
  processes overstates usage.
- **PSS**: unshared memory (USS) plus the process's proportion of shared memory (smem(8)).
- **USS**: unshared memory only; growth here points at the process itself.
```bash
smem -tk -s pss -r | head -15            # per process, sorted by PSS, with totals (-k human units)
smem -u -tk                              # per user
smem -m -s pss -r | head                 # per mapping/library
grep -E '^(Rss|Pss|Private_Dirty|Swap)' /proc/1234/smaps_rollup    # no smem installed
ps -eo pid,rss,cmd --sort=-rss | head    # fast, RSS only
```

## 2. Prove growth over time
```bash
while sleep 60; do printf '%s ' "$(date +%T)"; awk '/^Pss:|^Swap:/{printf "%s %s ",$1,$2}' /proc/1234/smaps_rollup; echo; done | tee pss.log
pidstat -r -p 1234 60                    # page faults and memory utilisation per interval (sysstat; -r)
```
Steady growth across load-neutral periods (night, weekend) = leak; growth that plateaus =
cache/warm-up. Include `Swap:` — a leaking process may be pushed to swap and look flat in RSS.

## 3. Narrow it down
```bash
pmap -x 1234 > t1; sleep 600; pmap -x 1234 > t2; diff t1 t2    # which mappings grew (extended format)
ls /proc/1234/task | wc -l               # thread count growing → thread leak (each has a stack)
ls /proc/1234/fd | wc -l                 # fd leak often accompanies memory leak
```
Language runtimes have their own heap profilers; use those first for managed code. Native code in test: `valgrind --leak-check=full` (Memcheck manual);
for a running process, bcc `memleak -p PID` (eBPF) prints outstanding allocations with call stacks.

## 4. Contain until fixed
`MemoryMax=2G` + `Restart=on-failure` on the unit, or a scheduled restart — record it as a
known issue, not a fix. systemd.resource-control(5) recommends `MemoryHigh=` as the main control and `MemoryMax=` as the last line of defence.

## Gotchas
- Freed memory is not always returned to the OS, so RSS can stay high after a spike without a leak.
- Kernel-side leaks don't show in any process: check `SUnreclaim` (part of Slab that cannot be reclaimed) in /proc/meminfo.
- tmpfs and shm growth looks like "memory gone" with no process to blame.

## Verify
- [ ] A time series (PSS/USS per interval) shows monotonic growth for the suspect and not for peers.
- [ ] After the fix or restart, the same series is flat under the same load.

## Checked
2026-10-27. Checked against the Linux kernel proc documentation (smaps fields Rss, Pss, Private_Dirty, Swap, SwapPss, the smaps_rollup file, Slab and SUnreclaim), the Debian trixie smem(8) page (USS and PSS definitions; -t, -k, -s, -r, -u, -m), sysstat pidstat(1) (-r), bcc memleak(8), and systemd.resource-control(5) (MemoryHigh and MemoryMax guidance). Confirmed: smaps_rollup contains the same fields as smaps; the smem option set; pidstat -r reporting page faults and memory use; memleak -p PID; valgrind --leak-check=full in the Memcheck manual. Removed: the pmap column sorting and anon-growth claim (the pmap page does not describe -x columns), the JVM, Python, Go, Node and heaptrack tooling lines, the MALLOC_ARENA_MAX tuning claim and the malloc behaviour remark, which were not confirmed from readable sources. The selenic.com link in sources is unreachable from this environment and was replaced by the Debian smem page.

Method: documentation only; no commands were run.
