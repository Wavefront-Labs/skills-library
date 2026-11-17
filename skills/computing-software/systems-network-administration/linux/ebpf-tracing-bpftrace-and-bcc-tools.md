---
id: computing-software.systems-network-administration.linux.ebpf-tracing-bpftrace-and-bcc-tools
name: ebpf-tracing-bpftrace-and-bcc-tools
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, ebpf, bpftrace, bcc-tools, execsnoop, opensnoop, tcpconnect, runqlat, biolatency, kprobes, tracepoints, performance-troubleshooting, lpic-2, sysadmin]
level: practitioner
status: docs-checked
description: "Answer production questions safely with eBPF: ready-made BCC tools (execsnoop, opensnoop, tcpconnect, runqlat) and bpftrace one-liners on tracepoints, kprobes and uprobes."
sources:
  - https://github.com/iovisor/bcc/blob/master/README.md
  - https://github.com/bpftrace/bpftrace/blob/master/man/adoc/bpftrace.adoc
  - https://github.com/bpftrace/bpftrace/blob/master/docs/language.md
  - https://github.com/bpftrace/bpftrace/blob/master/docs/tutorial_one_liners.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# eBPF tracing: BCC tools and bpftrace

**Goal:** see short-lived processes, file opens, connections and latency distributions on a
live box with low overhead — things `top` and logs can't show.

## 1. Install
- Install the BCC tools and bpftrace from your distribution's packages; package names and the tool install
  directory (and any `-bpfcc` name suffix) differ per distribution, so locate them with your package manager.
- Tracing needs root or equivalent privileges. Some bpftrace probe types (fentry/fexit) need a kernel with BTF.

## 2. BCC tools (first resort)
```bash
cd /usr/share/bcc/tools
./execsnoop -T                 # every exec(), incl. processes that live 5 ms (cron storms, crash loops)
./opensnoop -x -n nginx        # failed opens only (-x), filter by name: missing files, EACCES
./tcpconnect -t; ./tcpaccept   # outgoing/incoming TCP connections with PID
./tcpretrans                   # retransmits with addresses (network loss)
./runqlat 10 1                 # CPU run-queue latency histogram — CPU saturation
./biolatency -D 10 1           # block I/O latency per disk
./ext4slower 10                # ext4 ops slower than 10 ms (xfsslower, nfsslower too)
./cachestat 1                  # page cache hit ratio
./profile -F 99 -f 30 > out.folded   # CPU stack sampling for flame graphs
./killsnoop; ./oomkill         # who sent signals; OOM kill details
```

## 3. bpftrace one-liners (when no tool fits)
```bash
bpftrace -l 'tracepoint:syscalls:sys_enter_open*'         # list probes
bpftrace -e 'tracepoint:syscalls:sys_enter_openat { printf("%s %s\n", comm, str(args.filename)); }'
bpftrace -e 'tracepoint:raw_syscalls:sys_enter { @[comm] = count(); }'          # syscalls by process
bpftrace -e 'kprobe:vfs_read { @start[tid] = nsecs; } kretprobe:vfs_read /@start[tid]/ { @us = hist((nsecs - @start[tid]) / 1000); delete(@start, tid); }'
bpftrace -e 'tracepoint:sched:sched_process_exit { printf("%s exited\n", comm); }'
bpftrace -e 'uretprobe:/bin/bash:readline { printf("%d %s\n", pid, str(retval)); }'   # commands typed in bash
```
Ctrl-C prints maps (`@`). Syntax: `probe /filter/ { action }`; builtins `pid comm tid nsecs
kstack ustack retval args`.

## Gotchas
- High-frequency probes (every syscall, every packet) cost real CPU — run for seconds, not hours.
- User stacks need symbol information for the traced binary; check each tool's man page for stack options.

## Verify
- [ ] `execsnoop` shows a test `ls` you run in another terminal.
- [ ] A one-liner's histogram/count matches a known workload (e.g. `dd` reads show in `vfs_read`).

## Checked

Checked 2026-10-27 against bpftrace language reference and one-liner tutorial (bpftrace/bpftrace master), BCC man pages (iovisor/bcc master), 2026-10-27. Confirmed: bpftrace -l listing, tracepoint args.field syntax, str(), count(), hist(), nsecs, kstack/ustack, delete(@map, key) form, uprobe/uretprobe attach syntax, BCC option names used (execsnoop -T, opensnoop -x -n, tcpconnect -t, biolatency -D, profile -F -f) and the existence of tcpaccept, tcpretrans, runqlat, ext4slower, cachestat, killsnoop, oomkill. Removed or softened: package names and install paths, kernel-version and capability requirements, BTF path, lockdown and frame-pointer remarks, and a sched_process_exit field that does not exist; delete() call updated to the documented form.

Method: documentation only; no commands were run.
