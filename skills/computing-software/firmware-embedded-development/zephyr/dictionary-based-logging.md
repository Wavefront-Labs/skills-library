---
id: computing-software.firmware-embedded-development.zephyr.dictionary-based-logging
name: dictionary-based-logging
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [dictionary-logging, log-dictionary-support, log-parser, binary-logging, log-database, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Shrink Zephyr log flash and bandwidth with dictionary-based logging: binary output, the generated log_dictionary.json database, host-side parsing, and backend support."
sources:
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/doc/services/logging/index.rst
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/logging/backends/Kconfig.uart
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/logging/Kconfig.template.log_format_config
  - https://docs.zephyrproject.org/latest/services/logging/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dictionary-based logging

Dictionary-based logging outputs messages in a binary format: arguments in their native storage formats
and, for statically defined strings (format strings and string arguments), references into the ELF file
instead of the strings. A dictionary created at build time maps the references back to the strings, and an
offline parser rebuilds the text. The binary form can be more compact in some cases, but needs the offline
parser and is less convenient than text logs.

## Enable
```
CONFIG_LOG=y
CONFIG_LOG_MODE_DEFERRED=y
CONFIG_LOG_BACKEND_UART=y
CONFIG_LOG_BACKEND_UART_OUTPUT_DICTIONARY=y
CONFIG_LOG_BACKEND_UART_OUTPUT_DICTIONARY_BIN=y    # default; or _HEX for hexadecimal text (UART backend only)
# CONFIG_LOG_DICTIONARY_SUPPORT is selected by the backend option
```
The RTT backend can also output dictionary logs (`CONFIG_LOG_BACKEND_RTT_OUTPUT_DICTIONARY`, with
`CONFIG_USE_SEGGER_RTT`; `_HEX` variant available). The in-tree `logging-dictionary` sample shows the setup.

## Build output
`build/zephyr/log_dictionary.json`: maps string addresses to format strings, source ids and
types. Keep it **with each firmware build** (CI artefact); logs from a device can only be decoded
with the database from the exact same build.

## Decode on the host
```bash
# live from serial (binary output only; hex is not supported by the live parser)
python $ZEPHYR_BASE/scripts/logging/dictionary/live_log_parser.py \
    build/zephyr/log_dictionary.json serial /dev/ttyACM0 115200

# live from J-Link RTT, or tail a file
python $ZEPHYR_BASE/scripts/logging/dictionary/live_log_parser.py build/zephyr/log_dictionary.json jlink-rtt <device_name>
python $ZEPHYR_BASE/scripts/logging/dictionary/live_log_parser.py build/zephyr/log_dictionary.json file <filepath>

# offline, from a captured file; add --hex when the capture holds hexadecimal characters
python $ZEPHYR_BASE/scripts/logging/dictionary/log_parser.py \
    build/zephyr/log_dictionary.json capture.bin
```

## Restrictions
- Only statically defined strings are encoded as ELF references; the database only works with the build
  that produced it.
- `long double` is not supported by Python's `struct` module, so such arguments decode to wrong values.
- Binary output cannot be read in a plain terminal; use the hex variant when capturing by hand.
- Logging does not support width specifiers on strings (`%8s`, `%.*s`).

## Verify
- [ ] `log_dictionary.json` archived with every release image.
- [ ] Host parser decodes a sample capture from the device correctly.
- [ ] Image size compared before/after (`west build -t rom_report`) if size is the goal.

## Checked

Checked 2026-10-26 against the Zephyr logging guide (doc/services/logging/index.rst on main) and Kconfig files: dictionary
design description, `CONFIG_LOG_DICTIONARY_SUPPORT` selected by backends, UART `_BIN`/`_HEX` choice (BIN default, HEX
UART-only per Kconfig help) and RTT options, `log_dictionary.json` build-only validity, parser positional arguments for
serial, jlink-rtt and file inputs, `--hex` for the offline parser, live parser binary-only, `long double` limitation.
Removed flash-saving, formatting-cost and interleaving claims, the file-system backend claim, and the invented
`--port`/`--baudrate` flags, none of which the documentation supports.

Method: documentation only; no commands were run.
