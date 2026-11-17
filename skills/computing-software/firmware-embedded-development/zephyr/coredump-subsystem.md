---
id: computing-software.firmware-embedded-development.zephyr.coredump-subsystem
name: coredump-subsystem
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr-logging, zephyr-coredump, debug-coredump, coredump-backend-flash, coredump-gdbserver, post-mortem, fatal-error-handler, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Capture Zephyr core dumps on fatal errors to logs or a flash partition, retrieve them from the field, and inspect them with GDB via the coredump GDB server."
sources:
  - https://docs.zephyrproject.org/latest/services/debugging/coredump.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/debug/coredump.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/debug/coredump/Kconfig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Zephyr coredump subsystem

**Goal:** after a crash in the field, get registers, stacks and selected memory back to a
developer's GDB session, without a debugger attached at crash time.

## Enable
```
CONFIG_DEBUG_COREDUMP=y
CONFIG_DEBUG_COREDUMP_BACKEND_FLASH_PARTITION=y     # or _BACKEND_LOGGING, _BACKEND_LOGGING_UDP, _BACKEND_NULL
CONFIG_DEBUG_COREDUMP_MEMORY_DUMP_MIN=y             # exception thread's stack only; or _THREADS / _LINKER_RAM (default)
```
The flash backend needs a partition in devicetree (node label `coredump_partition`, `label =
"coredump-partition"`):
```dts
&flash0 { partitions { coredump_partition: partition@f8000 {
    label = "coredump-partition"; reg = <0x000f8000 DT_SIZE_K(32)>; }; }; };
```
Memory choices: `_MIN` dumps the exception thread's stack and thread struct plus the bare minimum
to walk the stack; `_THREADS` dumps the stacks and thread structs of all threads; `_LINKER_RAM`
(the default) dumps the region between `_image_ram_start` and `_image_ram_end` (data, noinit and
BSS at least). Size the partition for the choice you make. Extra memory can be added through
coredump devices even with `_MIN`.

## Retrieving
- Logging backend: the dump appears as `#CD:BEGIN#` ... `#CD:END#` hex lines in the console; save
  the log.
- UDP backend (`_BACKEND_LOGGING_UDP`): `scripts/coredump/coredump_udp_receiver.py` on the
  collector host rebuilds the same raw binary format.
- Flash backend: after reboot, the app checks for a stored dump
  (`coredump_query(COREDUMP_QUERY_HAS_STORED_DUMP, NULL)`), then reads it with
  `coredump_cmd(COREDUMP_CMD_COPY_STORED_DUMP, ...)` and uploads it (MCUmgr, cloud), then
  `COREDUMP_CMD_ERASE_STORED_DUMP`. A shell command (`CONFIG_DEBUG_COREDUMP_SHELL=y`) can
  print it too.

## Analysing
```
./scripts/coredump/coredump_serial_log_parser.py crash.log crash.bin   # from log
./scripts/coredump/coredump_gdbserver.py build/zephyr/zephyr.elf crash.bin
<SDK gdb for the target arch> build/zephyr/zephyr.elf -ex "target remote localhost:1234"
(gdb) bt
(gdb) info registers
(gdb) p some_global
```
**Keep the exact `zephyr.elf` for every released build** (by build ID or version); without it
the dump is just numbers.

## Gotchas
- The dump is written from the fatal error handler, so a backend that depends on the faulting
  subsystem may fail; consider which backend suits the failure modes you expect.
- Sensitive data in RAM dumps: decide what leaves the device (privacy/security).

## Verify
- [ ] Forced fault (e.g. `k_oops()` from a shell command) produces a dump that yields a correct
      backtrace in GDB.
- [ ] Dump survives reboot and is uploaded/erased by the app.

## Checked

Checked 2026-10-25 against the Zephyr source (main, post-4.4; latest release v4.4.2): doc/services/debugging/coredump.rst, include/zephyr/debug/coredump.h and subsys/debug/coredump/Kconfig.
Confirmed: `DEBUG_COREDUMP`, the four backends, the three memory-dump choices and the LINKER_RAM default; the flash partition node (`coredump_partition`, label "coredump-partition"); `#CD:` log framing; `coredump_serial_log_parser.py`, `coredump_udp_receiver.py`, `coredump_gdbserver.py` usage and port 1234; `coredump_query`/`coredump_cmd` with `COREDUMP_QUERY_HAS_STORED_DUMP`, `COREDUMP_CMD_COPY_STORED_DUMP`, `COREDUMP_CMD_ERASE_STORED_DUMP`; `DEBUG_COREDUMP_SHELL` exists.

Method: documentation only; no commands were run.
