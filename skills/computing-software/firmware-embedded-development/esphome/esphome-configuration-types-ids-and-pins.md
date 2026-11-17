---
id: computing-software.firmware-embedded-development.esphome.esphome-configuration-types-ids-and-pins
name: esphome-configuration-types-ids-and-pins
category: computing-software
field: firmware-embedded-development
product: esphome
tags: [esphome, configuration-types, id, pin-schema, gpio, inverted, pullup, strapping-pins, drive-strength]
level: intro
status: docs-checked
description: "Write valid ESPHome IDs and pins: C++ naming rules for IDs, chip-internal GPIO numbers and board aliases, and the full pin schema with mode, inverted and strapping warnings."
sources: ["https://esphome.io/guides/configuration-types/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Esphome configuration types ids and pins

IDs connect components across domains, for example an output referenced by a light. They must be unique in a configuration. Because ESPHome generates C++ and IDs become variable names, they must follow C++ identifier rules: start with a letter, no spaces, no special characters except underscore, and not be a keyword. They are internal and are not Home Assistant entity IDs.

Pins always use the chip-internal GPIO numbers: `16` or `GPIO16`. Many boards define aliases, for example the NodeMCU ESP8266 uses `D0` for GPIO16; aliases are defined per board in the esphome section and not all boards have them.

The advanced pin schema:

```yaml
pin:
  number: GPIO5
  inverted: true
  mode:
    input: true
    pullup: true
```

Options:
- `number` (required), `inverted` (treat reads and writes as inverted, default false).
- `allow_other_uses`: suppress the error raised when the same pin appears elsewhere, for rare shared-pin cases.
- `mode`: a shorthand string (`INPUT`, `OUTPUT`, `OUTPUT_OPEN_DRAIN`, `ANALOG`, `INPUT_PULLUP`, `INPUT_PULLDOWN`, `INPUT_OUTPUT_OPEN_DRAIN`) or a mapping of `input`, `output`, `pullup`, `pulldown`, `open_drain`.
- `drive_strength`: ESP32 with ESP-IDF only; `5mA`, `10mA`, `20mA` (default) or `40mA`.
- `ignore_strapping_warning`: ESP32 strapping pins are read at reset to set boot behaviour, so avoid them for I/O; only suppress the warning if you are certain it is safe.

## Checked

2026-11-04. Prose, option names, defaults and ranges were compared with https://esphome.io/guides/configuration-types/ (fetched this batch). Nothing needed removing.

Method: documentation only; no commands were run.
