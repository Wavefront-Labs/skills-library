---
id: computing-software.firmware-embedded-development.esp-idf.panic-backtrace-decoding
name: panic-backtrace-decoding
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [idf-monitor, esp-panic-backtrace, guru-meditation, addr2line, panic-handler, esp-reset-reason, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Read ESP-IDF Guru Meditation panics: decode backtraces with idf.py monitor or addr2line, interpret common exception causes, and configure panic behaviour for dev and field."
sources:
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/fatal-errors.html
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/tools/idf-monitor.html
  - https://github.com/espressif/esp-idf/blob/v6.1/components/esp_system/include/esp_system.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Panic backtrace decoding

## What a panic looks like (Xtensa)
```
Guru Meditation Error: Core  0 panic'ed (LoadProhibited). Exception was unhandled.
Core  0 register dump:
PC      : 0x400d2f1a  PS      : 0x00060630  A0      : 0x800d1234  A1      : 0x3ffb5e60
...
EXCVADDR: 0x00000008
Backtrace: 0x400d2f17:0x3ffb5e60 0x400d1231:0x3ffb5e90 0x40088a2d:0x3ffb5eb0
```
`idf.py monitor` decodes each address with the build's ELF and prints `file:line` under it.
That requires the **same ELF** as the flashed binary (monitor warns on mismatch).

Without IDF Monitor (for example a field crash from an archived ELF), look the PC values up in the matching ELF with the
toolchain's `addr2line` for your chip (a binutils tool; see its manual for options). The backtrace line holds PC:SP pairs.
RISC-V chips print registers and a stack dump; IDF Monitor builds the backtrace from that dump (it ends with
"Backtrace stopped: frame did not save the PC"). To make the device itself print a backtrace for another monitor
program, enable `CONFIG_ESP_SYSTEM_USE_EH_FRAME` (menu "Backtracing method"): it increases the binary by 20% to 100%, includes
debug information, and the docs strongly advise against it in mass production. `CONFIG_ESP_SYSTEM_USE_FRAME_POINTER` is the alternative: about +5-6%
binary size and about 1% slower, without debug information, so usable in production builds.

## Reading the cause
| Message | Usual meaning |
|---|---|
| `LoadProhibited` / `StoreProhibited`, EXCVADDR near 0 | NULL pointer (+ field offset) dereference |
| EXCVADDR random/odd | use-after-free, corrupted pointer, uninitialised struct |
| `InstrFetchProhibited`, PC = 0 or not `0x4xxxxxxx` | call through a function pointer that does not point to valid code |
| `IllegalInstruction` | a FreeRTOS task function returned instead of calling `vTaskDelete`, a failed instruction read from SPI flash (flash pins reconfigured or disturbed), or in C++ a non-void function that ends without returning a value |
| `IntegerDivideByZero` | as named |
| `Stack canary watchpoint triggered (task)` | that task's stack overflowed (needs `CONFIG_FREERTOS_WATCHPOINT_END_OF_STACK`): increase its stack |
| `abort() was called at PC ...` | `ESP_ERROR_CHECK` failed (file/line printed above) or `assert` |
| Interrupt watchdog (Interrupt WDT) | an ISR or critical section ran too long, or a deadlock with interrupts off |
| Task watchdog timeout | only fatal if `CONFIG_ESP_TASK_WDT_PANIC` is set; a task did not yield |
| `Cache error` | see iram-attr-and-cache-disabled-code |
| `Brownout detector was triggered` | the supply voltage fell below the detector's level; a power problem, not a software bug |

If a fatal error happens inside an ISR, the backtrace shows the interrupt frames too; read the top line as the error location
and the following lines as the call chain.

## Panic behaviour
```
CONFIG_ESP_SYSTEM_PANIC_PRINT_REBOOT=y    # default: print, then reboot (field)
CONFIG_ESP_SYSTEM_PANIC_PRINT_HALT=y      # bench: stop so you can attach a debugger
CONFIG_ESP_SYSTEM_PANIC_GDBSTUB=y         # GDB over serial; idf.py monitor launches gdb
```
Pair with core dumps for full post-mortem (see core-dump-to-flash).

## In the field
On boot, `esp_reset_reason()` returns `ESP_RST_PANIC`, `ESP_RST_INT_WDT`, `ESP_RST_TASK_WDT`,
`ESP_RST_BROWNOUT`, etc. (values of `esp_reset_reason_t`). Report it with the firmware version. Keep the ELF of every released
build (CI artifact), or backtraces from the field are undecodable.

## Verify
- [ ] Deliberate NULL write produces a decoded `file:line` in `idf.py monitor`.
- [ ] Release ELFs archived and the manual `addr2line` lookup tested on one.
- [ ] Reset reason reported in telemetry.

## Checked

Checked against ESP-IDF v6.1 (docs/en/api-guides/fatal-errors.rst, components/esp_system/include/esp_system.h) and the IDF Monitor guide.
Confirmed: register dump and `Backtrace:` PC:SP format, IDF Monitor decoding and RISC-V stack-dump backtrace, `CONFIG_ESP_SYSTEM_USE_EH_FRAME` (20% to 100% size increase, not advised for mass production) and `CONFIG_ESP_SYSTEM_USE_FRAME_POINTER` (+5-6% size, about 1% slower), the three panic-behaviour options with PRINT_REBOOT as default, `CONFIG_ESP_SYSTEM_PANIC_GDBSTUB`, causes of IllegalInstruction, InstrFetchProhibited, Load/StoreProhibited (EXCVADDR), IntegerDivideByZero, stack canary watchpoint, `abort() was called at PC`, brownout message, Task WDT panic option, `esp_reset_reason_t` values ESP_RST_PANIC, ESP_RST_INT_WDT, ESP_RST_TASK_WDT, ESP_RST_BROWNOUT. Removed unconfirmed claims: explicit addr2line flags and toolchain prefixes, the `|<-CORRUPTED` marker, the exact "Interrupt wdt timeout on CPU0" and "Cache disabled but cached memory region accessed" strings, flash access with cache disabled as an IllegalInstruction cause, and stack smash as an InstrFetch cause.

Method: documentation only; no commands were run.
