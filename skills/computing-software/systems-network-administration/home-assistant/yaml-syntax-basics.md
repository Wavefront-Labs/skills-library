---
id: computing-software.systems-network-administration.home-assistant.yaml-syntax-basics
name: yaml-syntax-basics
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [yaml, indentation, mapping]
level: intro
status: draft
description: "Write valid Home Assistant YAML: key-value mappings, dash lists, 2-space indentation, comments, and the integration versus platform distinction."
sources:
  - https://www.home-assistant.io/docs/configuration/yaml/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: write YAML entries in configuration.yaml that Home Assistant accepts first time.

Core rules from the docs:

- Mappings are `key: value`. Collections are items that start with `-`. Both can nest.
- Indent with 2 spaces per level. Tabs are not allowed.
- Duplicate keys do not error: the last value for a key is used, so a repeated key silently overrides the first.
- `#` starts a comment that is ignored.
- An integration provides the logic (for example `notify`); a platform connects to a specific service (for example `pushbullet`).

Integration with a platform:

```yaml
notify:
  platform: pushbullet
  api_key: "o.1234abcd"
  name: pushbullet
```

A collection nested inside a mapping, with a comment:

```yaml
input_select:
  threat:
    name: "Threat level"
    # A collection is used for options
    options:
      - 0
      - 1
      - 2
      - 3
    initial: 0
```

A list of mappings, creating two MQTT sensors:

```yaml
sensor:
  - platform: mqtt
    state_topic: "sensor/topic"
  - platform: mqtt
    state_topic: "sensor2/topic"
```

In `input_select` above, `threat` has no value on its own line because everything nested below it is its value.

Most features are set up in the UI; only a few integrations still need entries in configuration.yaml.
