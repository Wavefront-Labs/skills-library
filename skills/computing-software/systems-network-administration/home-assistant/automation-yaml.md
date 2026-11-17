---
id: computing-software.systems-network-administration.home-assistant.automation-yaml
name: automation-yaml
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [automation-yaml, alias, automations-yaml]
level: practitioner
status: docs-checked
description: "Write automations directly in YAML: the UI-managed automations.yaml include, labelled blocks, alias, multiple triggers, conditions and actions."
sources:
  - https://www.home-assistant.io/docs/automation/yaml/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: hand-write automations in configuration.yaml alongside the UI-managed file.

Keep the include the UI needs, and add labelled blocks for your own:

```yaml
# The configuration required for the UI to work
automation: !include automations.yaml
# Labeled automation block
automation kitchen:
  - triggers:
      - trigger: ...
```

Complete example:

```yaml
automation my_lights:
  - alias: "Rule 1 Light on in the evening"
    triggers:
      - trigger: sun
        event: sunset
        offset: "-01:00:00"
      - trigger: state
        entity_id:
          - person.paulus
          - person.anne_therese
        to: "home"
    conditions:
      - condition: state
        entity_id:
          - person.paulus
          - person.anne_therese
        match: any
        state: "home"
      - condition: time
        after: "16:00:00"
        before: "23:00:00"
    actions:
      - action: homeassistant.turn_on
        target:
          entity_id: light.living_room
```

Notes:

- Prefix each trigger and condition with `-` to list several.
- A single action does not need the `-`, though it is allowed.
- `alias` gives the automation a name.
- Optional `initial_state: false` starts the automation turned off.

After editing, reload automations to apply the changes: Settings > Tools > YAML, then Automations under YAML configuration reloading. A run of a changed automation stops when you reload.

## Checked

2026-11-04. Confirmed against the Automation YAML page. Changed the reload instruction to Settings > Tools > YAML > Automations, as the page states, instead of the developer tools.

Method: documentation only; no commands were run.
