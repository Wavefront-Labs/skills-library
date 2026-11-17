---
id: computing-software.systems-network-administration.home-assistant.automation-parts
name: automation-parts
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [trigger, condition, action]
level: intro
status: docs-checked
description: "Understand the three parts of a Home Assistant automation, how trigger, condition and action fit together, and that automations are entities."
sources:
  - https://www.home-assistant.io/docs/automation/basics/
  - https://www.home-assistant.io/docs/automation/yaml/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: structure an automation correctly before building it.

An automation has three parts:

```text
(trigger part)    When Paulus enters home
(condition part)  and it is after sunset
(action part)     turn on the lights in the living room
```

- Trigger: what starts the automation.
- Condition: an optional check; the action part runs only if the conditions are met.
- Action: what the automation does.

In YAML the keys are plural lists:

```yaml
automation:
  - alias: "Example"
    triggers:
      - trigger: sun
        event: sunset
    conditions:
      - condition: time
        after: "16:00:00"
    actions:
      - action: light.turn_on
        target:
          entity_id: light.living_room
```

Build in the editor in this order: add a trigger, add a condition, add an action.

Automations are also entities. They have states and attributes, and actions for automations exist (such as triggering one or turning it on and off). 
Several triggers can be listed, and the automation starts when any of them fires. With several conditions, the And block needs all of them verified and the Or block at least one.

## Checked

2026-11-04. Confirmed against the Automation basics page and the Automation YAML page. Removed the unsupported line that triggers react at a specific moment; reworded the conditions bullet and the And/Or note to the page wording.

Method: documentation only; no commands were run.
