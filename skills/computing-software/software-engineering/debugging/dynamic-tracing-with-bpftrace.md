---
id: computing-software.software-engineering.debugging.dynamic-tracing-with-bpftrace
name: dynamic-tracing-with-bpftrace
category: computing-software
field: software-engineering
product: debugging
tags: [debugging, observing-execution, bpftrace, ebpf-tracing, bcc-tools, uprobes, kprobes, tracepoints, production-tracing, linux]
level: advanced
status: docs-checked
description: "Trace live Linux systems with eBPF: bcc ready-made tools (execsnoop, opensnoop, biolatency) and bpftrace kprobe, tracepoint and uprobe programs."
sources: ["https://github.com/bpftrace/bpftrace/blob/master/man/adoc/bpftrace.adoc", "https://github.com/iovisor/bcc", "https://www.brendangregg.com/ebpf.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic tracing with bpftrace and bcc

**Goal:** answer precise questions about a running production system (who opens this
file, what's slow, which function returns errors) with low overhead and no restarts.

## Ready-made bcc tools (try these first)
From the bcc README tool list:
| Tool | Shows |
|---|---|
| `execsnoop` | new processes via exec() syscalls |
| `opensnoop` | open() syscalls |
| `tcpconnect` / `tcpaccept` | TCP active (connect()) / passive (accept()) connections |
| `tcpretrans` | TCP retransmits and TLPs |
| `biolatency` | block device I/O latency as a histogram |
| `biosnoop` | block device I/O with PID and latency |
| `runqlat` | run queue (scheduler) latency as a histogram |
| `offcputime` | off-CPU time summarised by kernel stack trace |
| `gethostlatency` | latency of getaddrinfo/gethostbyname[2] calls |

## bpftrace
A program is one or more probes: a provider followed by colon-separated options, for example
`kprobe:do_nanosleep` or `tracepoint:syscalls:sys_enter_openat`, then an optional filter and an action block.
Examples from the bpftrace manual:
```bash
bpftrace -e 'kprobe:do_nanosleep { printf("%d sleeping\n", pid); }'
bpftrace -e 'kprobe:do_nanosleep { printf("%d sleeping\n", pid); }' -c 'sleep 5'
bpftrace -l 'kprobe:*'                    # list probes; wildcards work
bpftrace -l 'k:*socket*,tracepoint:syscalls:*tcp*'
bpftrace -v -e 'tracepoint:syscalls:sys_enter_nanosleep { printf("%s is sleeping.\n", comm); }'
```
- `-l` lists matching probes (given a program, the probes in it); `-v` is verbose; `-c` runs a command;
  `-p`/pid attaches to or filters by a process.
- User-space probes take a binary or library path and function, e.g. `u:lib.so:"fn(char const*)"`,
  and can read arguments such as `str(arg0)`.
- Dynamic tracing (kprobes, uprobes) instruments software text and is not a stable API; target functions
  may be documented only in source. Static tracing points (tracepoints) are fixed and may be a stable
  API. Prefer tracepoints when one exists.
- Dynamic tracing needs only a symbol table that bpftrace can read.

## Safety
Keep sessions short and test on staging first; the manual's `-d verifier` option prints the BPF verifier log
when a program is rejected. Look up your kernel and privilege requirements in the bpftrace and bcc install docs.

## Verify
- [ ] Question answered with an aggregated measurement, not a single anecdotal event.
- [ ] Overhead acceptable (watch CPU while tracing).

## Checked
2026-11-09. Confirmed against the bcc README tool list and the bpftrace manual (probe syntax, `-e`, `-c`, `-l`,
`-v`, `-d verifier`, kprobe example, uprobe syntax, dynamic versus static tracing). Removed as not stated in
these pages: package names, root/CAP_BPF/CAP_PERFMON and kernel-version requirements, the histogram,
latency, uretprobe `retval` and `args.filename` one-liners, the Go/JVM/Node uprobe advice and the claim that
in-kernel aggregation is the main overhead control. Gregg's book is not cited.
Method: documentation only; no commands were run.
