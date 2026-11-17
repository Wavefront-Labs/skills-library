---
id: computing-software.systems-network-administration.linux.ftrace-and-trace-cmd
name: ftrace-and-trace-cmd
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, ftrace, trace-cmd, tracefs, function-graph, tracepoints, kernelshark, kernel-tracing, latency-tracing, lpic-2, sysadmin]
level: practitioner
status: docs-checked
description: "Use the kernel's built-in tracer: tracefs, function and function_graph tracers, event tracepoints, filters, and trace-cmd record/report — available even where eBPF tools aren't."
sources:
  - https://docs.kernel.org/trace/ftrace.html
  - https://docs.kernel.org/trace/events.html
  - https://man7.org/linux/man-pages/man1/trace-cmd.1.html
  - https://docs.kernel.org/trace/ftrace.html
  - https://docs.kernel.org/trace/events.html
  - https://github.com/rostedt/trace-cmd/blob/master/Documentation/trace-cmd/trace-cmd-record.1.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ftrace and trace-cmd

**Goal:** see what the kernel is doing (which functions, which scheduler/IRQ/block events,
how long) on systems with no compiler, no BCC, maybe no extra packages at all.

## 1. Raw tracefs
```bash
cd /sys/kernel/tracing 2>/dev/null || cd /sys/kernel/debug/tracing
cat available_tracers                 # tracers compiled into this kernel
echo 0 > tracing_on; echo > trace
echo function_graph > current_tracer
echo 'vfs_*' > set_ftrace_filter      # limit to matching functions (wildcards)
echo 1234 > set_ftrace_pid            # only this PID
echo 1 > tracing_on; sleep 2; echo 0 > tracing_on
head -50 trace
echo nop > current_tracer; echo > set_ftrace_filter; echo > set_ftrace_pid; echo 1 > tracing_on   # clean up!
```
Events (tracepoints, cheaper and stable):
```bash
ls events/                                        # sched, block, irq, syscalls, net, ext4 …
echo 1 > events/sched/sched_switch/enable
echo 'prev_comm ~ "java*"' > events/sched/sched_switch/filter
cat trace_pipe                                    # streaming, consumes entries
echo 0 > events/enable
```

## 2. trace-cmd (friendlier front end)
```bash
dnf/apt install trace-cmd
trace-cmd record -p function_graph -g do_sys_openat2 -P 1234 sleep 5   # graph one function (-g) for a PID (-P)
trace-cmd record -e sched_switch -e sched_wakeup -e block -a sleep 10  # events
trace-cmd report | less                                 # reads trace.dat
trace-cmd report --cpu 3 | grep -c sched_switch
trace-cmd stat; trace-cmd reset                         # current state; restore defaults
trace-cmd list -e | grep tcp                            # find events
```

## 3. Useful recipes
- Who is waking a CPU / why latency: `trace-cmd record -e sched_wakeup -e sched_switch -e irq`.
- Function latency of a slow syscall: function_graph shows per-call duration with `+`/`!`
  markers for durations above 10 µs / 100 µs.
- `/proc/sys/kernel/ftrace_dump_on_oops=1` dumps the trace buffer into the console on a crash.

## Gotchas
- `function` tracer on everything is very expensive — always filter (`set_ftrace_filter`, `-l`, `-g`).
- Buffers are per-CPU and ring-wrapped; raise `buffer_size_kb` for longer captures.
- Forgetting to reset leaves tracing overhead active; `trace-cmd reset` at the end.

## Verify
- [ ] `cat current_tracer` is `nop`, `tracing_on` is 1 and no events are enabled after cleanup.
- [ ] The report contains the target PID/function and plausible durations.

## Checked

Checked against the Linux kernel documentation tree (torvalds/linux master, latest commit 2026-10-25) (trace/ftrace, trace/events, sysctl/kernel) and the trace-cmd man sources (`trace-cmd-record`, `-report`, `-list`, `-stat`, `-reset`) on 2026-10-26. Confirmed: tracefs at `/sys/kernel/tracing` (debugfs path for compatibility), `available_tracers`, `current_tracer`, `tracing_on`, `set_ftrace_filter`, `set_ftrace_pid`, `buffer_size_kb`, `trace_pipe` as a consuming reader, event filter glob syntax `~`, function_graph `+` (10 us) and `!` (100 us) markers, `kernel.ftrace_dump_on_oops`, trace-cmd `-p`, `-e`, `-a`, `-l`, `-g`, `-P`, `report --cpu`. Fixed: the cleanup line now restores `tracing_on` to 1 so the verify step holds. Removed: the lockdown claim and kernelshark.

Method: documentation only; no commands were run.
