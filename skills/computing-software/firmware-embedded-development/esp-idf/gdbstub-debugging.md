---
id: computing-software.firmware-embedded-development.esp-idf.gdbstub-debugging
name: gdbstub-debugging
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-debug, gdbstub, gdb-over-uart, panic-gdbstub, runtime-gdbstub, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Debug ESP-IDF apps without a JTAG probe using the GDB stub over UART: panic-time and runtime gdbstub, connecting with idf.py monitor and inspecting tasks."
sources:
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/fatal-errors.html#gdb-stub
  - https://github.com/espressif/esp-idf/blob/v6.1/components/esp_gdbstub/Kconfig
  - https://github.com/espressif/esp-idf/blob/v6.1/components/esp_system/Kconfig
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/tools/idf-monitor.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GDB stub

The GDB stub lets GDB talk to the chip over the console UART. No probe, no extra pins.

## Panic-time stub
```
CONFIG_ESP_SYSTEM_PANIC_GDBSTUB=y
```
On a crash, instead of rebooting, the chip starts a GDB remote-protocol server on the console UART.
`idf.py monitor` starts GDB automatically when it detects the GDB Stub prompt (`$T0b#e6`-style packet)
on the UART. You can then:
```
(gdb) bt
(gdb) info threads          # FreeRTOS tasks (CONFIG_ESP_GDBSTUB_SUPPORT_TASKS)
(gdb) thread 4
(gdb) p *my_struct
(gdb) x/16xw 0x3ffb0000
```
This is read-only, post-mortem debugging: you cannot set breakpoints, change the PC or continue execution.
To reset, exit GDB and use Ctrl-T Ctrl-R in IDF Monitor or the reset button.

## Runtime stub
```
CONFIG_ESP_SYSTEM_GDBSTUB_RUNTIME=y
```
Run `idf.py monitor`, wait for the device to initialise, then press Ctrl+C to interrupt execution and
enter GDB attached to the device. All UART input is handled by the GDB stub while this option is on.
The print-and-halt, print-and-reboot and silent-reboot panic choices depend on the runtime stub being
off, so a build with the runtime stub uses the panic-time GDB stub as its panic behaviour.

## Trade-offs vs JTAG
- The panic-time stub cannot set breakpoints or continue execution (see above); a JTAG probe is needed for that.
- Console UART is shared with the stub; with the runtime stub, UART input goes to the stub.
- Field-friendly: a customer unit with only a serial cable can still give you a backtrace and
  variable dump. Ship panic gdbstub only in diagnostic builds; production should reboot
  (`CONFIG_ESP_SYSTEM_PANIC_PRINT_REBOOT`, the default) and store a core dump instead.

## Verify
- [ ] Force a panic (`abort()`), GDB attaches via idf.py monitor, `bt` shows the call.
- [ ] Production sdkconfig does not halt on panic.

## Checked

Checked against ESP-IDF v6.1 (docs/en/api-guides/fatal-errors.rst GDB Stub section, components/esp_gdbstub/Kconfig, components/esp_system/Kconfig).
Confirmed: `CONFIG_ESP_SYSTEM_PANIC_GDBSTUB` (choice item, available when esp_gdbstub is in the build), `CONFIG_ESP_SYSTEM_GDBSTUB_RUNTIME` with the Ctrl+C procedure in `idf.py monitor`, `CONFIG_ESP_GDBSTUB_SUPPORT_TASKS` (default y, `info threads`), `CONFIG_ESP_SYSTEM_PANIC_PRINT_REBOOT` as the default choice, automatic GDB start by IDF Monitor, and the read-only no-breakpoint/no-continue limit of the panic stub. Removed unconfirmed claims: breakpoint and stepping support in the runtime stub and the manual `target remote` invocation.

Method: documentation only; no commands were run.
