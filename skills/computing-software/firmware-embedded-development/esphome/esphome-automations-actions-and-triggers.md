---
id: computing-software.firmware-embedded-development.esphome.esphome-automations-actions-and-triggers
name: esphome-automations-actions-and-triggers
category: computing-software
field: firmware-embedded-development
product: esphome
tags: [esphome, automations, actions, triggers, on-press, on-value-range, delay, if-action, then, local-automation]
level: practitioner
status: docs-checked
description: "Build on-device ESPHome automations with triggers and ordered actions, including on_press, on_value_range, delay and if, so devices work without Home Assistant."
sources: ["https://esphome.io/automations/actions/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Esphome automations actions and triggers

ESPHome actions make a device do something. The main argument for ESPHome automations over Home Assistant's: IoT devices should not depend on network connections for simple jobs such as a wall button toggling a dehumidifier.

Anatomy:
- Give the target component an `id` so the automation can refer to it (for example `switch.toggle` with the switch's id).
- Triggers attach to components as `on_...` keys. A binary sensor offers `on_press` (when pressing begins), `on_release`, `on_click`, `on_double_click`. A sensor offers `on_value_range` (value within, above or below a range, such as `above: 65.0` or `below: 50.0`).
- `then:` holds the actions, executed sequentially, one list entry each. A single trigger can also carry several automations.

Example of the pattern: turn a switch on when humidity is at or above 65 percent and off when it falls to 50 percent or below, using two `on_value_range` blocks.

Common actions:
- `delay`: a smart asynchronous delay; other code keeps running. In a lambda, return the delay in milliseconds.
- `if`: evaluates `condition:` and runs `then:` or `else:`, then continues with the next action.

When pure YAML is not enough, use templates (lambdas), which run C++. The `lambda` action executes arbitrary C++ (for example `id(some_binary_sensor).publish_state(false);`), and `id(...)` fetches a component by its ID so you can read `.state` or call its methods.

## Checked

2026-11-04. Prose, option names, defaults and ranges were compared with https://esphome.io/automations/actions/ (fetched this batch). Replaced an unsourced lambda/COVER_OPEN paragraph with what the page shows.

Method: documentation only; no commands were run.
