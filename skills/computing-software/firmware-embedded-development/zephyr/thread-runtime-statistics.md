---
id: computing-software.firmware-embedded-development.zephyr.thread-runtime-statistics
name: thread-runtime-statistics
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [thread-runtime-stats, k-thread-runtime-stats-get, thread-analyzer, cpu-load, config-sched-thread-usage, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Measure per-thread CPU usage and stack use in Zephyr with CONFIG_THREAD_RUNTIME_STATS, k_thread_runtime_stats_get, the thread analyzer, and the kernel shell commands."
sources:
  - https://docs.zephyrproject.org/latest/services/debugging/thread-analyzer.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/kernel/Kconfig
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/debug/thread_analyzer/Kconfig
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/kernel/thread.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Thread runtime statistics

## Enable
```
CONFIG_THREAD_RUNTIME_STATS=y
CONFIG_SCHED_THREAD_USAGE_ALL=y      # sum of all non-idle thread cycles (default y when usage stats are on)
CONFIG_THREAD_NAME=y
CONFIG_THREAD_STACK_INFO=y
CONFIG_INIT_STACKS=y                 # fill stacks with 0xaa before first use for high-water measurement
```
Optional: `CONFIG_SCHED_THREAD_USAGE_ANALYSIS=y` for extra scheduling timing (total and longest
scheduled time), and `CONFIG_THREAD_RUNTIME_STATS_USE_TIMING_FUNCTIONS=y` to gather the statistics
with the timing functions, which may use a different timer than OS timekeeping.

## Programmatic
```c
k_thread_runtime_stats_t s, all;
k_thread_runtime_stats_get(tid, &s);
k_thread_runtime_stats_all_get(&all);
uint32_t pct = (uint32_t)(s.execution_cycles * 100 / all.execution_cycles);
/* all.execution_cycles is non-idle plus idle cycles; all.idle_cycles is the idle share */
```
For load over a window, take two snapshots and diff; the counters are cumulative since boot.
`k_thread_runtime_stats_enable(tid)` / `_disable` turn per-thread accounting on and off at runtime
(`CONFIG_SCHED_THREAD_USAGE_AUTO_ENABLE`, default y, enables gathering automatically).

## Thread analyzer
```
CONFIG_THREAD_ANALYZER=y
CONFIG_THREAD_ANALYZER_USE_PRINTK=y   # or _USE_LOG
CONFIG_THREAD_ANALYZER_AUTO=y         # periodic dump
CONFIG_THREAD_ANALYZER_AUTO_INTERVAL=30   # seconds; default 60
```
`CONFIG_THREAD_ANALYZER` selects `CONFIG_INIT_STACKS`, `CONFIG_THREAD_STACK_INFO` and
`CONFIG_THREAD_RUNTIME_STATS`. It reports stack and CPU usage per thread; call `thread_analyzer_print()`
manually when not using `_AUTO`.

## Shell
```
uart:~$ kernel thread list     # thread list
uart:~$ kernel stacks          # thread stack usage
```
Needs `CONFIG_KERNEL_SHELL=y` plus the stack info options above.

## Reading the numbers
- Stack "used" is a high-water mark from the fill pattern (`CONFIG_INIT_STACKS`); leave margin.
- The system workqueue stack is sized with `CONFIG_SYSTEM_WORKQUEUE_STACK_SIZE` (default 1024); the
  logging and shell threads have their own stack-size options.
- Statistics are cycle counts; the cycle source (timing functions or system timer) sets the
  resolution.

## Verify
- [ ] All threads named, so reports are readable.
- [ ] Stack sizes adjusted from measured high-water marks under worst-case load.
- [ ] CPU load metric computed from idle cycles over a window.

## Checked

Checked 2026-10-26 against the Zephyr documentation and sources on the main branch (repository head 2026-10-25; latest release v4.4.2).
- `CONFIG_THREAD_RUNTIME_STATS`, `_USE_TIMING_FUNCTIONS`, `CONFIG_SCHED_THREAD_USAGE_ALL` / `_ANALYSIS` / `_AUTO_ENABLE`,
  `CONFIG_INIT_STACKS` (0xaa), `CONFIG_THREAD_NAME`, `CONFIG_THREAD_STACK_INFO`, `CONFIG_SYSTEM_WORKQUEUE_STACK_SIZE`
  (`kernel/Kconfig`); thread analyzer selects and `AUTO_INTERVAL` default 60 (`subsys/debug/thread_analyzer/Kconfig`);
  `execution_cycles` / `idle_cycles` (`kernel/thread.h`); `kernel thread list` and `kernel stacks` (shell module files
  `thread/list.c`, `thread/stacks.c`).
- Wrong in the draft: `THREAD_RUNTIME_STATS` was said to select `SCHED_THREAD_USAGE` (not shown in the Kconfig).
- Removed: the `(older: kernel threads)` note, unsourced percentage margin, overhead paragraph, and the logging/shell
  stack option names that were not confirmed.

Method: documentation only; no commands were run.
