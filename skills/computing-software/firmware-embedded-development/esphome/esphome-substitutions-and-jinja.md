---
id: computing-software.firmware-embedded-development.esphome.esphome-substitutions-and-jinja
name: esphome-substitutions-and-jinja
category: computing-software
field: firmware-embedded-development
product: esphome
tags: [esphome, substitutions, jinja, literal, include-vars, yaml, templating, secrets]
level: advanced
status: docs-checked
description: "Reduce repetition with ESPHome substitutions: ${} syntax, structured values, Jinja expressions, the !literal tag and substitutions inside !include filenames and variables."
sources: ["https://esphome.io/components/substitutions/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Esphome substitutions and jinja

Substitutions let one generic source file serve many nodes. Define key-value pairs under top-level `substitutions:`, then use `$key` or `${key}` (case-sensitive, bash-like) anywhere; ESPHome replaces them before validating the configuration.

```yaml
substitutions:
  bme280_temperature_offset: "-1.0"
sensor:
  - platform: bme280_i2c
    temperature:
      name: BME280 Temperature
      filters:
        - offset: ${bme280_temperature_offset}
```

Values can be any YAML type: dictionaries (`device: {name: Kitchen AC, port: 12}`), booleans, lists (`unused_pins: [12, 23, 27]`). Two substitution passes are performed, so compound names like `${bar_${foo}_value}` work, but the recommended form is a dictionary lookup `${bar[foo]}`.

Jinja: simple expressions and filters work inside `${ ... }` (ESPHome configures Jinja to use `${...}` rather than `{{ ... }}`). All substitution variables are visible by name; dictionaries use dot or index access (`${ device.name }`, `${ device["name"] }`) and lists can be indexed (`${ unused_pins[2] }`). Expressions can do arithmetic, conditionals (`${native_width * 2 if high_dpi else native_width}`), filters such as `| round | int`, and use Python math functions.

To stop substitution and Jinja processing for a value, prefix it with `!literal`; the text `This is a ${value}` then stays literal.

`!include` also takes substitutions: the filename is expanded before loading (`hardware-${platform}.yaml`), the variables passed to the included file are expanded, and include conditions are expanded so the file only loads when the condition holds.

## Checked

2026-11-04. Prose, option names, defaults and ranges were compared with https://esphome.io/components/substitutions/ (fetched this batch). Removed the remote-packages secrets line (belongs to the packages page, not cited here).

Method: documentation only; no commands were run.
