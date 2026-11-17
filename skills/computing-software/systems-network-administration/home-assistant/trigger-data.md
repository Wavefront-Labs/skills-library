---
id: computing-software.systems-network-administration.home-assistant.trigger-data
name: trigger-data
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [trigger-data, trigger-idx, from-state]
level: practitioner
status: draft
description: "Read the trigger variable in Home Assistant templates: trigger.id, trigger.idx, trigger.from_state and to_state, and where to inspect real trigger data."
sources:
  - https://www.home-assistant.io/docs/automation/trigger-data/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: use data about what started an automation inside conditions and actions.

Properties on every trigger:

- `trigger.platform`: the trigger type, such as `state`.
- `trigger.alias`: the trigger alias, or `None`.
- `trigger.id`: the trigger `id`; if you set none, it equals `trigger.idx`.
- `trigger.idx`: position in the trigger list as a string. The first is `"0"`, so compare with a string: `trigger.idx == "0"`.

Most triggers also have `trigger.description`.

State triggers add:

- `trigger.entity_id`: the entity monitored.
- `trigger.from_state`: previous state object, `None` if the entity was just created.
- `trigger.to_state`: new state object, `None` if the entity was removed.
- `trigger.for`: timedelta of how long the entity has been in the new state, or `None`.
- `trigger.attribute`: the monitored attribute, or `None` if the state is monitored.

Example use:

```yaml
message: "{{ trigger.to_state.name }} changed to {{ trigger.to_state.state }}"
```

To branch on the trigger, prefer the Triggered by condition with the trigger id rather than testing in a template.

See real data:

1. In the automation editor, select the Triggered message on the trigger row to open Triggering event detail.
2. Or open the run's trace, select the trigger, and read Changed variables under Step details.

Running only the actions manually gives no trigger data, so templates that read `trigger` have nothing to use.
