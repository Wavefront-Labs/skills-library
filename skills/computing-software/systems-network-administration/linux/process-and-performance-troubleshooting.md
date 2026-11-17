---
id: computing-software.systems-network-administration.linux.process-and-performance-troubleshooting
name: process-and-performance-troubleshooting
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, performance, troubleshooting, use-method, load-average, d-state, uninterruptible-sleep, psi, pressure-stall, pidstat, sysstat, sar, iostat, mpstat, top, htop, ps, strace, perf, perf-top, flame-graph, oom-killer, oom-score-adj, cgroups, systemd-cgtop, steal-time, iowait, zombie, signals, kill, lsof, sysadmin, high-load]
level: advanced
status: draft
description: "Diagnose slow or misbehaving Linux processes: USE method, load average vs D-state, PSI, pidstat/sar history, strace and perf, OOM-killer forensics, cgroup limits and stuck processes."
sources:
  - https://www.brendangregg.com/usemethod.html
  - https://docs.kernel.org/accounting/psi.html
  - https://man7.org/linux/man-pages/man1/pidstat.1.html
  - https://man7.org/linux/man-pages/man1/perf.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Process and performance troubleshooting — from "it's slow" to the guilty resource

**Goal:** go past the first-minute triage (see
`computing-software.systems-network-administration.linux.systemd-service-management`)
to a named bottleneck: which resource, which process, which code path.

## 1. USE method — for every resource ask Utilisation, Saturation, Errors
| Resource | Utilisation | Saturation | Errors |
|---|---|---|---|
| CPU | `mpstat -P ALL 1` | run-queue `r` in `vmstat 1` > cores; PSI `cpu` | — |
| Memory | `free -m` (look at *available*) | `si/so` in `vmstat`; PSI `memory` | OOM kills in `journalctl -k` |
| Disk | `iostat -xz 1` `%util` | `aqu-sz`, `r_await/w_await` | `dmesg` I/O errors |
| Network | `sar -n DEV 1` | `nstat` drops/retransmits, `ss -s` | `ip -s link` errors |

Errors are cheapest to check and most often skipped.

## 2. Load average is not CPU
Linux load counts runnable **and** uninterruptible (D-state) tasks. Load 40 with idle
CPUs means tasks blocked on I/O, NFS, or a hung device:
```bash
ps -eo state,pid,comm,wchan:32 | awk '$1=="D"'   # who is stuck and where in the kernel
cat /proc/<PID>/stack                            # root; kernel stack of a hung task
```
**Pressure Stall Information** (kernel 4.20+) is the better saturation signal:
```bash
cat /proc/pressure/{cpu,memory,io}   # "some avg10=12.3" = 12% of time ≥1 task stalled
```
Sustained `memory full` > a few % means real thrashing even if swap looks quiet.

## 3. Who is it — and historically?
```bash
pidstat -u -r -d -w 1 5      # per-process CPU, memory faults, disk I/O, context switches
systemd-cgtop                # per-service (cgroup) CPU/mem/IO
sar -u -f /var/log/sa/sa$(date -d yesterday +%d)   # what happened last night
```
Enable sysstat collection (`systemctl enable --now sysstat`) *before* you need it —
"slow at 03:00" is unanswerable without history. The sa file path differs on Debian
(`/var/log/sysstat/`).

High `%steal` in `mpstat` on a VM = the hypervisor is starving you; no in-guest fix.

## 4. What is it doing?
- **Syscall view:** `strace -f -tt -T -p <PID> -o /tmp/trace.txt` — long `-T` times on
  `futex`, `read`, `connect` point at locks, slow storage, or a remote dependency.
  `strace -c -p <PID>` gives a summary. strace slows the target a lot; keep it short
  in production.
- **CPU profile:** `perf top -p <PID>` live, or
  `perf record -F 99 -g -p <PID> -- sleep 30; perf report`. Feed to FlameGraph scripts
  for a flame graph. Missing symbols → install debuginfo / use `--call-graph dwarf`;
  JIT runtimes (Java, Node) need perf-map agents.
- **Open files/sockets:** `lsof -p <PID>`, `ss -tanp | grep <PID>`.

## 5. OOM-killer forensics
```bash
journalctl -k | grep -iE 'out of memory|oom-kill|killed process'
```
The kill message names the cgroup: if it says `oom_memcg` / a service slice, the
process hit its **cgroup** `MemoryMax` (or container limit), not host RAM — raise the
limit or fix the leak, adding swap won't help. Protect critical daemons with
`OOMScoreAdjust=-500` in their unit; never `-1000` everything.

## 6. Stuck processes and signals
- `kill -TERM` first, `-KILL` after a timeout. **D-state processes ignore SIGKILL**
  until the I/O returns — fix the storage/NFS, or reboot.
- **Zombies** (`Z`) use no resources but a PID; kill or fix the *parent* that isn't
  reaping (`ps -o ppid= -p <ZPID>`).
- `cat /proc/<PID>/status` shows threads, VmRSS, voluntary/non-voluntary context switches.

**Uncertain:** tool output columns change between sysstat and procps versions; PSI
requires `CONFIG_PSI` and can be disabled by boot flag on some distros (`psi=1`).

## Verify
- [ ] You can name the saturated resource with a number (e.g. io some avg60=35).
- [ ] You identified the process/cgroup responsible with `pidstat` or `systemd-cgtop`.
- [ ] For CPU issues you have a perf profile; for latency, an strace or wchan sample.
- [ ] OOM events were attributed to host vs cgroup limit.
- [ ] sysstat history is enabled for the next incident.
