---
id: computing-software.firmware-embedded-development.hardware-debugging.post-mortem-core-dump-analysis
name: post-mortem-core-dump-analysis
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [core-dump-analysis, coredump, post-mortem-debugging, crashdebug, zephyr-coredump, esp-idf-coredump, memfault, gdb, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Debug field crashes after the fact with MCU core dumps: capturing registers and RAM, Zephyr and ESP-IDF coredump tooling, CrashDebug for raw dumps, and loading them into GDB."
sources:
  - https://docs.zephyrproject.org/latest/services/debugging/coredump.html
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/core_dump.html
  - https://github.com/adamgreen/CrashDebug
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Post-mortem core dump analysis

**Goal:** a device that crashed in the field (no debugger attached) gives you a full GDB session
of the moment of the crash: backtrace, locals, globals, all threads.

## What a core dump contains
- CPU registers at the fault.
- Memory: all RAM, or selected regions (current thread stack, kernel objects, key globals). Each
  region costs storage, so prioritise stacks.
- You need the ELF that matches the running firmware: GDB takes symbols (and, for CrashDebug,
  the read-only flash contents) from it.

## Zephyr
```
CONFIG_DEBUG_COREDUMP=y
CONFIG_DEBUG_COREDUMP_BACKEND_LOGGING=y            # or _FLASH_PARTITION, _LOGGING_UDP
CONFIG_DEBUG_COREDUMP_MEMORY_DUMP_THREADS=y        # or _MIN, or _LINKER_RAM (the default)
```
`_MIN` dumps only the exception thread stack and its thread struct, `_THREADS` dumps all thread
structs and stacks, `_LINKER_RAM` dumps the RAM between `_image_ram_start` and `_image_ram_end`
(data, noinit, BSS at least). The flash-partition backend needs a partition labelled
`coredump-partition` in the devicetree. The logging backend prints `#CD:` lines on the console.
Host side, from the Zephyr tree:
```sh
./scripts/coredump/coredump_serial_log_parser.py coredump.log coredump.bin
./scripts/coredump/coredump_gdbserver.py build/zephyr/zephyr.elf coredump.bin
```
Then start the architecture's GDB on `build/zephyr/zephyr.elf` and run
`target remote localhost:1234`; `info registers` and `bt` work as usual. You can also start the
server from inside GDB with `target remote | ./scripts/coredump/coredump_gdbserver.py --pipe
build/zephyr/zephyr.elf coredump.bin`.

## ESP-IDF
The panic handler saves a core dump with every task's TCB and stack (the crashed task always,
others by priority up to `CONFIG_ESP_COREDUMP_MAX_TASKS_NUM`). `CONFIG_ESP_COREDUMP_TO_FLASH_OR_UART`
selects flash or UART output; flash needs a `coredump` data partition (sub-type `coredump`,
add the `encrypted` flag if flash encryption is on). The file is ELF and carries a SHA256 checksum.
`CONFIG_ESP_COREDUMP_CAPTURE_DRAM` adds .bss, .data and heap (bigger dump).
`idf.py coredump-info` prints registers, call stack, tasks and memory; `idf.py coredump-debug`
opens GDB on the dump (only stack variables are reliable since not all memory is saved). A UART
dump is Base64; save the body to a file and decode with `idf.py coredump-info -c <file>`.
With flash encryption on, read the dump through the device rather than from the encrypted partition.

## Bare metal or custom: CrashDebug
CrashDebug is a GDB remote stub for Cortex-M post-mortem debugging. It needs the matching ELF
(or a `--bin` image plus base address) and a dump holding RAM and r0-r12, sp, lr, pc, xpsr.
Dump sources: a text dump you create from GDB while halted (loop `x/4wx` over each RAM region
shown by `info mem`, then `info all-registers`, with logging to a file); a CrashCatcher hex dump
(starts with the `6343` signature, with surrounding console text removed); or a CrashCatcher
binary dump. Then:
```sh
arm-none-eabi-gdb app.elf -ex "set target-charset ASCII" \
  -ex "target remote | CrashDebug --elf app.elf --dump crash.dmp"
```
Use forward slashes in paths on Windows (GDB strips backslashes in `-ex` arguments).

## Commercial
Memfault's SDK collects coredumps from fielded devices with configurable regions, storing them
in RAM, flash or external storage and rebooting afterwards; see its coredump collection docs.

## Analysis checklist
- `bt` in the faulting thread; `info threads` / `thread apply all bt` for RTOS dumps.
- Fault status registers (CFSR, HFSR, MMFAR, BFAR) to classify (see `cortex-m-hardfault-analysis`).
- Corrupted backtraces often mean stack corruption: look at the raw stack memory.
- Archive the ELF for every released build; without it the dump is useless.

## Verify
- [ ] Trigger a deliberate fault on a test device and get a correct `bt` from the dump on the host.

## Checked
Confirmed against the Zephyr Core Dump page (Kconfig options, #CD: log, script names and argument
order, gdbserver port 1234, flash partition label), the ESP-IDF Core Dump guide (options, partition
requirements, Base64 UART output, idf.py subcommands, checksum) and the CrashDebug README (stub
usage, dump types, command line, Windows slash note). Fixed: the ESP-IDF option name
(`CONFIG_ESP_COREDUMP_ENABLE_TO_FLASH` is not on the current page). Removed as unconfirmed: the
`dump binary memory` recipe, `esp_core_dump_image_get()`, Percepio Detect, "same author" claim for
CrashCatcher, and stacked-exception-frame detail.

Method: docs-checked 2026-11-09 against the Zephyr core dump page, the ESP-IDF core dump guide and the CrashDebug README, all read in full.
