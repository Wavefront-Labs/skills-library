---
id: computing-software.firmware-embedded-development.zephyr.pm-state-statistics
name: pm-state-statistics
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [pm-stats, config-pm-stats, stats-shell, sleep-residency, power-profiling, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Measure how often and how long a Zephyr system sleeps in each power state with CONFIG_PM_STATS and the stats shell, and use it to find what keeps the device awake."
sources:
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/pm/pm_stats.c
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/pm/Kconfig
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/stats/Kconfig
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/stats/stats_shell.c
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PM state statistics

```
CONFIG_PM=y
CONFIG_STATS=y           # CONFIG_PM_STATS depends on it (does not select it)
CONFIG_PM_STATS=y
CONFIG_STATS_NAMES=y     # readable counter names (implied by CONFIG_STATS_SHELL)
CONFIG_STATS_SHELL=y     # depends on STATS && SHELL
CONFIG_SHELL=y
```

## Reading
```
uart:~$ stats list
Stats Group pm_cpu_000_state_2_stats (hdr addr: ...)
    state_count (offset: 0, addr: ...): 1452
    state_last_cycles (offset: 4, addr: ...): 3276
    state_total_cycles (offset: 8, addr: ...): 98123456
```
The shell exposes one command, `stats list`, which prints every registered group with its counters
(there is no `stats show`). One group, `pm_cpu_<CPU>_state_<N>_stats`, is registered for every CPU
and every `enum pm_state` value (`PM_STATE_COUNT`), used or not. Counters per group: number of entries,
cycles in the last residency, and total cycles (32-bit, so they wrap). Values are `k_cycle_get_32()` deltas;
convert with `sys_clock_hw_cycles_per_sec()` and compare total sleep cycles with uptime for a sleep ratio.

Programmatic access: the stats are `STATS_SECT` groups; read via `stats_group_find()` /
`stats_walk()` for telemetry.

## Interpreting
| Observation | Likely cause |
|---|---|
| Deep state count 0 | state not in `cpu-power-states`, locked (`pm_policy_state_lock_get()` without a matching `pm_policy_state_lock_put()`), or timeouts too frequent |
| Many short residencies | a periodic timer/thread wakes too often (logging thread, sensor polling at high rate, `k_sleep` loops) |
| Low total sleep ratio | a thread is busy; check thread runtime stats |
| Shallow state preferred | next timeout always shorter than deep state's min-residency |

## Finding wakers
- Thread runtime stats: which threads consume CPU.
- Tracing (`CONFIG_TRACING`, for example with SystemView) to see the timeline of wakes.
- Disable features one by one (logging, shell itself: the UART console prevents deep sleep on
  many SoCs because RX must stay on).
- Kernel timeouts: periodic `k_timer`s and `k_work_delayable` with short periods.

## Caveat
The shell UART used to read stats usually keeps the device out of deep sleep while active. Read
stats after a measurement period, or export them over another channel and compare with a power
analyser trace.

## Verify
- [ ] Sleep ratio and deep-state counts recorded for the target use case.
- [ ] Power analyser average current agrees with the residency picture.

## Checked

Checked 2026-10-26 against Zephyr main on GitHub: `CONFIG_PM_STATS` depends on `CONFIG_STATS` (the skill said it
selects it, now fixed); `CONFIG_STATS_SHELL` depends on STATS and SHELL and implies STATS_NAMES; the shell has only a
`stats list` subcommand (the invented `stats show` was removed); group naming `pm_cpu_%03d_state_%1d_stats`, the three
counters and their use of `k_cycle_get_32()` are from `subsys/pm/pm_stats.c`; `stats_group_find()`/`stats_walk()`,
`sys_clock_hw_cycles_per_sec()`, `CONFIG_THREAD_RUNTIME_STATS` and the policy lock/put functions exist. Removed
`CONFIG_PM_DEBUG`, which is not a Kconfig symbol in `subsys/pm/Kconfig`.

Method: documentation only; no commands were run.
