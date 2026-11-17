---
id: computing-software.firmware-embedded-development.esp-idf.openocd-external-jtag
name: openocd-external-jtag
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-debug, esp-openocd, jtag-debugging, esp-prog, gdb-esp32, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Debug ESP32 with OpenOCD and an external JTAG probe (ESP-Prog, J-Link): wiring, openocd-esp32 board configs, GDB sessions, flash breakpoints and FreeRTOS thread awareness."
sources:
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/jtag-debugging/index.html
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/jtag-debugging/tips-and-quirks.html
  - https://github.com/espressif/openocd-esp32
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenOCD with external JTAG

Needed on the original ESP32 and S2 (no built-in USB-JTAG), or when the USB pins are used by
the application.

## Wiring (ESP32)
| JTAG | ESP32 GPIO |
|---|---|
| TDI | 12 |
| TCK | 13 |
| TMS | 14 |
| TDO | 15 |
| GND | GND |
GPIO12 (MTDI) is a strapping pin: at power-up a low level selects 3.3 V and a high level 1.8 V for the
SPI flash supply, and a connected JTAG probe overrides the pull resistor that does the bootstrapping. OpenOCD's
board files (for example `board/esp32-wrover-kit-3.3v.cfg`) provide the `ESP32_FLASH_VOLTAGE` parameter, which sets
the idle state of the TDO line to reduce the risk of a bad boot; set it to match your module's flash supply (most
WROOM modules use 3.3 V flash; WROVER before WROVER-B use 1.8 V, WROVER-B and -E use 3.3 V). These pins are lost to
the application while debugging.

## Run
Use Espressif's OpenOCD build (repository openocd-esp32; the ESP-IDF JTAG guide describes installing the pre-built binary
distribution), not stock OpenOCD.
```bash
openocd -f board/esp32-wrover-kit-3.3v.cfg          # ESP-WROVER-KIT (FT2232H); other probes and boards need other config files
idf.py openocd                                       # idf.py can start OpenOCD ...
idf.py gdb                                           # ... and GDB (in a second terminal)
```
Which `-f` files to use for your probe and board is covered in the guide's "Configuring OpenOCD for a specific target" section.
GDB:
```bash
xtensa-esp32-elf-gdb -x gdbinit build/app.elf
# gdbinit
target extended-remote :3333
mon reset halt
maintenance flush register-cache
thb app_main
c
```

## FreeRTOS awareness
OpenOCD has explicit support for ESP-IDF FreeRTOS, so GDB sees tasks as threads: `info threads`, `thread 3`, `bt`.
Set the OpenOCD variable `ESP_RTOS` to `none` (before the ESP config file is included) to disable this when debugging
FreeRTOS itself.

## Breakpoints
- ESP32 has 2 hardware breakpoints (`SOC_CPU_BREAKPOINTS_NUM`) and 2 watchpoints; hardware breakpoints work in flash or IRAM.
  OpenOCD also provides software breakpoints (flash up to 32, IRAM up to 32 on Xtensa), but GDB cannot set software breakpoints
  in flash, so OpenOCD emulates those as hardware ones. Setting a software breakpoint in flash modifies flash, and
  `-c 'set ESP_FLASH_SIZE 0'` on the OpenOCD command line disables flash breakpoints.
- `watch var` uses a hardware watchpoint (`set remote hardware-watchpoint-limit 2`); `CONFIG_FREERTOS_WATCHPOINT_END_OF_STACK` uses
  the last watchpoint, so do not combine it with your own.

## Flashing through JTAG
```bash
openocd -f board/esp32-wrover-kit-3.3v.cfg -c "program_esp build/app.bin 0x10000 verify exit"
```

## Issues
- If the application reconfigures a JTAG pin (for example MTDO as an input), GDB reports errors such as "DSR indicates target still busy"; JTAG pins cannot be reused while debugging.
- `CONFIG_ESP_DEBUG_OCDAWARE` (default on): on a panic with OpenOCD attached, ESP-IDF breaks into the debugger.

## Verify
- [ ] Breakpoint at `app_main` hit after `mon reset halt`.
- [ ] `info threads` lists all tasks.

## Checked

Checked against ESP-IDF v6.1 JTAG debugging guide (docs/en/api-guides/jtag-debugging: index.rst, esp32.inc, tips-and-quirks.rst, using-debugger.rst), tools/idf_py_actions/debug_ext.py and soc_caps.h for ESP32.
Confirmed: JTAG pin table (MTDI/GPIO12 TDI, MTCK/GPIO13 TCK, MTMS/GPIO14 TMS, MTDO/GPIO15 TDO); MTDI strapping behaviour and `ESP32_FLASH_VOLTAGE`; flash supply per module; `openocd -f board/esp32-wrover-kit-3.3v.cfg`; `program_esp filename.bin 0x10000 verify exit`; `idf.py openocd` and `idf.py gdb`; GDB startup commands `mon reset halt`, `maintenance flush register-cache`, `thb app_main`, `c`; 2 hardware breakpoints and 2 watchpoints on ESP32; software breakpoint limits and emulation; `ESP_RTOS`, `ESP_FLASH_SIZE`; `CONFIG_ESP_DEBUG_OCDAWARE`. The GDB `target extended-remote :3333` line uses OpenOCD's documented port 3333 with standard GDB syntax (the ESP-IDF guide does not show that exact command). Removed unconfirmed claims: the `espefuse set_flash_voltage` workaround, the J-Link command with `adapter speed 5000`, `adapter speed 1000` for examination errors, Wi-Fi reconnect expectations, watchdog behaviour on resume, and the `-rtos FreeRTOS` flag detail.

Method: documentation only; no commands were run.
