---
id: computing-software.firmware-embedded-development.esp-idf.builtin-usb-jtag-debugging
name: builtin-usb-jtag-debugging
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [idf-monitor, esp-usb-jtag, openocd-esp32, idf-py-gdb, usb-serial-jtag, hardware-breakpoints, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Debug ESP32-C3/S3/C6/H2 through the built-in USB Serial/JTAG controller with OpenOCD and GDB: drivers, idf.py openocd/gdb, breakpoints in flash, and sleep/pin pitfalls."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/jtag-debugging/configure-builtin-jtag.rst
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/jtag-debugging/index.rst
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/jtag-debugging/tips-and-quirks.rst
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/usb-serial-jtag-console.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Built-in USB-JTAG debugging

ESP32-C3, S3, C6, H2 (and newer) include a USB Serial/JTAG controller: one USB cable to the
chip's native USB pins (S3: GPIO19/20, C3: GPIO18/19) gives a serial console **and** a JTAG
debugger. No external probe needed.

## Host setup
- Linux: install OpenOCD's udev rules (`60-openocd.rules` from `openocd-esp32`), re-plug.
- Windows: if OpenOCD reports `LIBUSB_ERROR_NOT_FOUND`, install the drivers with the Espressif Installation Manager (EIM): `Open Dashboard`, then `Install Drivers`, or the EIM command line as described in the guide.
- Debugging over the built-in USB needs a chip revision the guide lists as supported (for example 0.3 or newer on ESP32-C3); use an external probe (such as ESP-Prog) on older revisions.

## Run
```bash
idf.py -p /dev/ttyACM0 flash          # flash over the same USB
idf.py openocd                        # uses the default board config for the target unless OPENOCD_COMMANDS or --openocd-commands is set
idf.py gdb                            # in another terminal; or:
idf.py openocd gdbgui monitor        # example of combining targets in one invocation
idf.py gdbgui / idf.py gdbtui
```
Manual:
```bash
openocd -f board/esp32s3-builtin.cfg        # board/esp32c3-builtin.cfg on ESP32-C3
<target>-gdb -x build/gdbinit/symbols build/app.elf   # e.g. xtensa-esp32s3-elf-gdb; idf.py gdb generates the gdbinit files
(gdb) target remote :3333
(gdb) mon reset halt
(gdb) thb app_main
(gdb) c
```

## Debugging specifics
- GDB cannot set software breakpoints in flash, so breakpoints in flash code use the chip's **hardware** breakpoints, a small fixed number per chip (see the breakpoints section of the tips-and-quirks guide). Delete old ones when you run out. Watchpoints are limited too (up to two on ESP32-family chips).
- `CONFIG_ESP_DEBUG_OCDAWARE=y` (default) makes panics break into the debugger instead of
  rebooting when attached.
- FreeRTOS awareness: `idf.py gdb` loads a GDB Python extension for FreeRTOS tasks when the requirements are met (otherwise `python import freertos_gdb`).
- Flash programming through OpenOCD: `mon program_esp build/app.bin 0x10000 verify` from GDB, or `program_esp_bins <build_dir> flasher_args.json verify exit` for a multi-binary project.

## Pitfalls
- **Sleep:** the USB Serial/JTAG controller does not work during sleep. In deep sleep the device disappears from the host; in light sleep it stops responding and may need a cable replug on wake. ESP-IDF adds no check to stop sleep entry while connected. Disable sleep in debug builds or use an external JTAG probe.
- **Pin use:** the USB D-/D+ pins (S3: GPIO19/20, C3: GPIO18/19) are dedicated to this controller while it is used for debugging.
- **Production:** burning eFuses can switch the JTAG interface to GPIOs, and enabling flash encryption or secure boot disables JTAG by default (the bootloader burns an eFuse on first boot). Plan debug access before burning.
- Console: `CONFIG_ESP_CONSOLE_USB_SERIAL_JTAG` (selected in the console option, `CONFIG_ESP_CONSOLE_UART`) routes logs here. Data can occasionally get stuck in host memory until more data is sent.

## Verify
- [ ] Breakpoint at `app_main` hits after `mon reset halt` + continue.
- [ ] Thread list shows all FreeRTOS tasks with backtraces.
- [ ] Debug build has sleep disabled or documented as unsupported while debugging.

## Checked

2026-10-25, against the ESP-IDF documentation source (espressif/esp-idf docs/en, master, v6.1 release period). Confirmed from the JTAG debugging guides and USB Serial/JTAG console guide: D-/D+ pins, EIM driver install and LIBUSB_ERROR_NOT_FOUND, Linux udev rules, board/esp32s3-builtin.cfg and esp32c3-builtin.cfg, idf.py openocd/gdb/gdbtui/gdbgui, program_esp and program_esp_bins, thb app_main and mon reset halt, CONFIG_ESP_DEBUG_OCDAWARE default on, sleep behaviour, JTAG disabled by secure boot or flash encryption. Removed unconfirmed claims: USB id 303a:1001, Zadig/WinUSB steps, mon esp smp, watchdog behaviour, DIS_USB_JTAG and JTAG_SEL_ENABLE eFuse names, TinyUSB conflict, console blocking.
Method: documentation only; no commands were run.
