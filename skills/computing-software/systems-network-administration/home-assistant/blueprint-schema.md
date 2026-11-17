---
id: computing-software.systems-network-administration.home-assistant.blueprint-schema
name: blueprint-schema
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [blueprint, input, sections]
level: advanced
status: docs-checked
description: "Write a Home Assistant automation blueprint: the blueprint header, inputs with selectors and defaults, input sections, and the !input tag in the body."
sources:
  - https://www.home-assistant.io/docs/blueprint/schema/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: write a reusable automation as a blueprint.

Minimal header:

```yaml
blueprint:
  name: Example blueprint
  domain: automation
```

Inputs go under `input`, each with a name and optionally a description, default and selector:

```yaml
blueprint:
  name: Example blueprint
  domain: automation
  input:
    my_input:
      name: Example input
```

Sections group inputs with their own `input` key. Sections are new in 2024.6.0, so set `min_version: 2024.6.0` under `homeassistant:` in the blueprint header when you use them:

```yaml
  input:
    my_section:
      name: My Section
      icon: mdi:cog
      description: These options control a specific feature of this blueprint
      input:
        my_input:
          name: Example input
```

Use an input value in the body with `!input`. To use it in a template, copy it into a variable first:

```yaml
variables:
  my_input: !input my_input
```

Motion-activated light, abridged:

```yaml
blueprint:
  name: Motion-activated Light
  domain: automation
  input:
    motion_entity:
      name: Motion Sensor
      selector:
        entity:
          filter:
            device_class: motion
            domain: binary_sensor
    no_motion_wait:
      name: Wait time
      default: 120
      selector:
        number:
          min: 0
          max: 3600
          unit_of_measurement: seconds
mode: restart
max_exceeded: silent
triggers:
  - trigger: state
    entity_id: !input motion_entity
    from: "off"
    to: "on"
```

## Checked

2026-11-04. Confirmed against the Blueprint schema page. Added the min_version 2024.6.0 requirement for input sections.

Method: documentation only; no commands were run.
