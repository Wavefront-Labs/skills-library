---
id: computing-software.firmware-embedded-development.platformio.device-monitor-options-and-filters
name: device-monitor-options-and-filters
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [monitor-filters, monitor-speed, esp32-exception-decoder, log2file, time-filter, custom-monitor-filter, pio-device-monitor, platformio, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Configure pio device monitor: monitor_speed/port/rts/dtr/eol/echo, built-in filters (esp32_exception_decoder, time, log2file), and writing a custom filter in Python."
sources:
  - https://docs.platformio.org/en/latest/core/userguide/device/cmd_monitor.html
  - https://docs.platformio.org/en/latest/projectconf/sections/env/options/monitor/index.html
  - https://docs.platformio.org/en/latest/projectconf/sections/platformio/options/directory/monitor_dir.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monitor options and filters

## Options in platformio.ini
```ini
[env:esp32dev]
monitor_speed = 115200            ; default is 9600
monitor_port = /dev/ttyUSB0       ; number, device name, URL handler, or a pattern such as /dev/ttyUSB*
monitor_rts = 0                   ; initial RTS line state (0 or 1)
monitor_dtr = 0                   ; initial DTR line state (0 or 1)
monitor_eol = LF                  ; default is CRLF
monitor_echo = yes                ; default is no
monitor_filters =
    default
    time
    esp32_exception_decoder
    log2file
```
`pio device monitor -e esp32dev` picks these up. The built-in `monitor` target starts the monitor
after a successful build (`pio run -t monitor`, or `targets = upload, monitor` in the env).
Command-line equivalents: `-p/--port`, `-b/--baud`, `--rts`, `--dtr`, `--echo`, `--eol`,
`-f/--filter`, `--raw`, `--encoding`, `--parity`.

## Built-in filters
- `default`: remove typical terminal control codes from input.
- `direct`: forward all data unchanged (use when data already contains ANSI colour codes).
- `debug`: print what is sent and received.
- `hexlify`: hexadecimal view of the data.
- `log2file`: log data to a file named `platformio-device-monitor-%date%.log`.
- `nocontrol`: remove all control codes including CR+LF.
- `printable`: show decimal codes for non-ASCII characters and replace most control codes.
- `time`: timestamp with milliseconds for each new line.
- `send_on_enter`: send a text to the device on Enter.
- `esp32_exception_decoder` and `esp8266_exception_decoder`: decode crash exceptions for the
  Espressif platforms.

## Custom filter
A filter is a Python file whose name has the `filter_` prefix. PlatformIO looks in the project's
`monitor` directory (`monitor_dir`, default `<project>/monitor`), then
`<platforms_dir>/<platform>/monitor`, then `<packages_dir>/<package>/monitor`.
```python
# monitor/filter_demo.py
from platformio.public import DeviceMonitorFilterBase

class Demo(DeviceMonitorFilterBase):
    NAME = "demo"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("Demo filter is loaded")

    def rx(self, text):
        return f"Received: {text}\n"

    def tx(self, text):
        print(f"Sent: {text}\n")
        return text
```
Enable with `monitor_filters = demo`. The official filters are examples:
`platformio/device/monitor/filters` in platformio-core and the `monitor` folders of
platform-espressif32 and platform-espressif8266.

## Hotkeys
Ctrl+C quits, Ctrl+T opens the menu, Ctrl+T then Ctrl+H shows help. Toggles after Ctrl+T:
Ctrl+R RTS, Ctrl+D DTR, Ctrl+E local echo, Ctrl+B BREAK. Ctrl+T then `b` changes the baud rate.

## Gotchas
- The `esp32_exception_decoder` needs the matching firmware build in the project; check the
  platform documentation for its requirements.
- Changing the RTS and DTR initial states can matter on boards that reset or enter the
  bootloader from those lines; set them explicitly if opening the monitor disturbs the board.

## Verify
- [ ] A deliberate crash prints a decoded backtrace.
- [ ] `log2file` captures a session for attaching to bug reports.

## Checked
2026-10-26 against platformio-docs (develop, last commit 2026-09-19): `pio device monitor`
reference and the monitor option and `monitor_dir` pages. Confirmed: option defaults (speed 9600,
eol CRLF, echo no), command-line flags, the built-in filter table, custom filter naming, search
locations and `DeviceMonitorFilterBase` API, hotkeys, `monitor` target. Removed as unconfirmed:
the `colorize` filter name, the "build_type = debug improves decoding" and addr2line remarks,
the native USB CDC remark, "DTR reset on open" as fact, and the `self.environment` and older-API
import notes. The docs describe the `log2file` location inconsistently (current directory in one
place, a `logs` folder in another), so check where the file appears on your version.
Method: documentation only; no commands were run.
