---
id: computing-software.systems-network-administration.home-assistant.splitting-configuration
name: splitting-configuration
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [include, default-config, split]
level: practitioner
status: docs-checked
description: "Split a growing configuration.yaml into files with !include, keeping the default_config and UI-managed automation, script and scene entries intact."
sources:
  - https://www.home-assistant.io/docs/configuration/splitting_configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: move parts of configuration.yaml into separate files without breaking the UI editors.

A fresh configuration.yaml contains entries you must not remove:

```yaml
# Loads a standard set of integrations. Keep this entry.
default_config:
# These files store automations, scripts, and scenes created in the UI.
automation: !include automations.yaml
script: !include scripts.yaml
scene: !include scenes.yaml
```

If there is a `homeassistant:` key, any `!include` under it (for `customize:` or `packages:`) stays nested inside it.

Rules for the included file:

- It must be valid YAML for the place it is included.
- Do not repeat the parent key and do not indent it to match the parent.

Example. In configuration.yaml:

```yaml
customize: !include customize.yaml
```

customize.yaml holds only the entries:

```yaml
light.living_room:
  friendly_name: "Living Room"
  icon: mdi:ceiling-light
switch.patio:
  friendly_name: "Patio Switch"
```

The same pattern works for any integration:

```yaml
switch: !include switch.yaml
sensor: !include sensor.yaml
```

Included files may themselves use `!include`. Use 2 spaces per level; wrong indentation is a common reason a file fails to load. Name files after their purpose.

## Checked

2026-11-04. Confirmed against the Splitting configuration page. Nothing removed.

Method: documentation only; no commands were run.
