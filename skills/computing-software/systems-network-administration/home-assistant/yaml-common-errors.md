---
id: computing-software.systems-network-administration.home-assistant.yaml-common-errors
name: yaml-common-errors
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [tab-character, booleans, case-sensitive]
level: intro
status: draft
description: "Fix the three classic Home Assistant YAML mistakes: tab characters, unquoted on/off turning into booleans, and wrong-case entity IDs."
sources:
  - https://www.home-assistant.io/docs/configuration/yaml/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: diagnose a configuration that fails to load because of a YAML syntax slip.

Tab character

The error `found character '\t' that cannot start any token` means a tab was typed instead of spaces. Replace the tab with 2 spaces per level.

Booleans

YAML treats `Y`, `true`, `Yes`, `ON` as true and `n`, `FALSE`, `No`, `off` as false. To set an entity state to the text `on`, quote it, otherwise it becomes the boolean true:

```yaml
state: "on"
```

An unquoted value can produce this error:

```txt
not a valid value for dictionary value @ data
```

Case

Home Assistant is case-sensitive. State values can use any case, so `'on'` is not `'On'` or `'ON'`. Entity IDs are always lowercase, so `binary_sensor.Front_Door` does not match the real entity `binary_sensor.front_door`.

To see how a state is actually reported, open Settings > Tools > States and read the value there.

Duplicate keys

If a key appears twice in the same mapping, the last value wins and the earlier one is dropped without a warning.

Validating

How you validate depends on your editor. If you edit files directly in Home Assistant, use the configuration check described in the configuration docs. From a shell, `hass --script check_config` also validates the files (see the check-config-script skill).
