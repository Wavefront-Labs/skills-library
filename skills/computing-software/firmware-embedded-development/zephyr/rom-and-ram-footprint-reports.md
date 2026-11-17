---
id: computing-software.firmware-embedded-development.zephyr.rom-and-ram-footprint-reports
name: rom-and-ram-footprint-reports
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [rom-report, ram-report, footprint-analysis, puncover, size-report, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Measure and shrink Zephyr flash and RAM use with west build -t rom_report/ram_report, footprint diffs, puncover, and the Kconfig options that matter most."
sources:
  - https://docs.zephyrproject.org/latest/develop/optimizations/footprint.html
  - https://docs.zephyrproject.org/latest/develop/optimizations/tools.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ROM and RAM footprint reports

## Reports
```bash
west build -b nrf52840dk/nrf52840 app
west build -t rom_report          # tree of flash usage by path/symbol
west build -t ram_report          # static RAM (.data/.bss/noinit)
west build -t footprint           # runs ram_report and rom_report; each also writes ram.json / rom.json in the build dir
west build -t rom_plot            # also ram_plot: sunburst chart in a browser
west build -t puncover            # local web server (localhost:5000 by default; pip install puncover)
west build -t dashboard           # HTML dashboard at build/dashboard/index.html (reports, Kconfig trace, init levels, devicetree)
```
`puncover` stack estimates need `-DCONFIG_STACK_USAGE=y -DCONFIG_CALLGRAPH_INFO=y`. Under sysbuild use
the image-prefixed targets (see the sysbuild page).
The build summary at link time already prints region usage:
```
Memory region   Used Size  Region Size  %age Used
        FLASH:     142 KB       1 MB     13.87%
          RAM:      38 KB     256 KB     14.84%
```

Reports group symbols by file-system location in the source tree. Two containers collect
symbols that cannot be placed: `Hidden` (no matching mapped file, or the name could not be
determined) and `No paths` (name known, location unknown; repeated functions are summed). Expand
big nodes to find the culprits.

## Comparing builds
```bash
python $ZEPHYR_BASE/scripts/footprint/size_report -k build/zephyr/zephyr.elf -z $ZEPHYR_BASE -o out rom
```
Save the JSON per commit in CI and diff; `scripts/footprint/fpdiff.py` compares two JSON reports.
Twister has footprint options: `--enable-size-report`, `--create-rom-ram-report` and
`--footprint-report [all|ROM|RAM]` (writes `twister_footprint.json`), and baseline comparison with
`-m/--last-metrics` or `--compare-report <twister.json>`, `--show-footprint`, and
`-H/--footprint-threshold` (percent, default 5.0). `--footprint-from-buildlog` takes sizes from
`build.log` and does not work correctly with sysbuild.

## Usual big wins
| Item | Kconfig |
|---|---|
| Logging strings | `CONFIG_LOG=n` in release, or `CONFIG_LOG_DICTIONARY_SUPPORT=y` |
| Asserts | `CONFIG_ASSERT=n`; `CONFIG_ASSERT_VERBOSE=n` drops file/line strings |
| printk/console | `CONFIG_PRINTK=n`, `CONFIG_CONSOLE=n`, `CONFIG_UART_CONSOLE=n` |
| Optimisation | `CONFIG_SIZE_OPTIMIZATIONS=y` (the default level, except with `CONFIG_DEBUG`, coverage or LLVM) vs `DEBUG_OPTIMIZATIONS` |
| Shell | `CONFIG_SHELL=n` or trim `CONFIG_SHELL_CMDS*` |
| Stacks (RAM) | `CONFIG_MAIN_STACK_SIZE`, `CONFIG_SYSTEM_WORKQUEUE_STACK_SIZE`, `CONFIG_ISR_STACK_SIZE`, `CONFIG_IDLE_STACK_SIZE`; measure with thread analyzer first |
| Heap (RAM) | `CONFIG_HEAP_MEM_POOL_SIZE`, `CONFIG_COMMON_LIBC_MALLOC_ARENA_SIZE` |
| Networking/BT buffers | `CONFIG_NET_BUF_*_COUNT`, `CONFIG_BT_BUF_*` |
| Libc | `CONFIG_PICOLIBC` vs `CONFIG_MINIMAL_LIBC`; `CONFIG_CBPRINTF_NANO=y` |

## Gotchas
- The reports describe the linked image; heap usage and stack high-water marks need runtime
  tools (`CONFIG_THREAD_ANALYZER`, `sys_heap_runtime_stats_get`).
- Start stack tuning with the documented defaults: ISR 2048, main 1024, idle 320, system
  workqueue 1024 bytes (the footprint page).
- Compare builds with identical toolchain versions; a compiler upgrade can shift sizes.

## Verify
- [ ] Footprint JSON stored per CI build with a size budget check.
- [ ] Release config reviewed against the big-wins table.

## Checked

2026-10-26. Zephyr docs main branch (latest release v4.4.2). Confirmed the ram_report, rom_report, ram_plot, rom_plot, puncover, dashboard targets and the Hidden and No paths containers (optimizations/tools page), footprint target and ram.json/rom.json output plus size_report arguments (cmake/reports/CMakeLists.txt), the default stack sizes (footprint page), the twister footprint options and defaults (twisterlib/environment.py), the optimisation-level default (Kconfig.zephyr), and that scripts/footprint/fpdiff.py exists. Corrected the footprint target description, the twister option list and the (hidden) container name; removed the unconfirmed .noinit stack remark.
Method: documentation only; no commands were run.
