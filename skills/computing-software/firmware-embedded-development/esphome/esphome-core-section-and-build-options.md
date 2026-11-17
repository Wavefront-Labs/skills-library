---
id: computing-software.firmware-embedded-development.esphome.esphome-core-section-and-build-options
name: esphome-core-section-and-build-options
category: computing-software
field: firmware-embedded-development
product: esphome
tags: [esphome, esphome-core, node-name, friendly-name, name-add-mac-suffix, build-flags, platformio-options, min-version, project]
level: practitioner
status: docs-checked
description: "Configure the ESPHome core section: node name rules, friendly name, MAC suffix, build path, PlatformIO options, includes, libraries, project info and loop interval."
sources: ["https://esphome.io/components/esphome/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Esphome core section and build options

The `esphome:` block holds core information ESPHome needs to build firmware, most importantly the node `name`.

Required and identity options:
- `name`: unique in your ESPHome network; lowercase letters, digits and hyphens only; at most 24 characters by default, or 31 if `name_add_mac_suffix` is `false`.
- `friendly_name`: sent to the frontend and used by Home Assistant as the integration and device name and as a prefix for entity names. Optional but recommended.
- `area`: a string or an `id`/`name` mapping telling Home Assistant which area the device belongs to; `areas` and `devices` define extra areas and sub-devices.
- `name_add_mac_suffix` (default false): appends the last 3 MAC bytes as `<name>-aabbcc`.
- `project` (`name`, `version`, optional `on_update`): creator project metadata; the version is stored in flash and compared on the next firmware's first run.
- `min_version`: refuse to compile on older ESPHome.

Build customisation: `build_path` (default is the `.esphome/build/<NODE>` folder, or the `ESPHOME_BUILD_PATH` variable), `platformio_options` (passed into the platformio.ini env section), `build_flags`, `environment_variables`, `includes` and `includes_c` (C/C++ files relative to the YAML file; the latter wrapped in `extern "C"`), `libraries`, `compile_process_limit`.

Runtime tuning: `loop_interval` (default 16ms; larger values save power but add latency and some components may misbehave) and `suspend_loop` (default false; no effect if any component such as `api` or `wifi` keeps its loop active).

Triggers: `on_boot` (default priority 600; 800 hardware init, 250 WiFi, 200 MQTT and native API, -100 everything initialized), `on_shutdown` (reverse ordering, so higher priority runs later) and `on_loop`.

## Checked

2026-11-04. Prose, option names, defaults and ranges were compared with https://esphome.io/components/esphome/ (fetched this batch). Nothing needed removing.

Method: documentation only; no commands were run.
