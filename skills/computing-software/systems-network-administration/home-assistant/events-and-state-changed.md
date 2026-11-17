---
id: computing-software.systems-network-administration.home-assistant.events-and-state-changed
name: events-and-state-changed
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [events, state-changed, call-service]
level: practitioner
status: docs-checked
description: "Use Home Assistant core events: the data in state_changed, call_service and automation_triggered, and how to watch them in the Events developer tool."
sources:
  - https://www.home-assistant.io/docs/configuration/events/
  - https://www.home-assistant.io/docs/tools/dev-tools/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick the right event type and read its data.

`state_changed`: fired whenever the state or attributes of an entity change. Data:

- `entity_id`: for example `light.kitchen`.
- `old_state`: previous state object, `null` if the state is set for the first time.
- `new_state`: new state object, `null` if the state was removed.

`call_service`: fired when an action is performed. Data:

- `domain`: for example `light`.
- `service`: for example `turn_on`.
- `service_data`: parameters, for example `{"brightness": 120}`.

`automation_triggered`: fired when an automation runs. Data: `name`, `entity_id`, and optional `source`.

Other core events listed include `homeassistant_start`, `homeassistant_started`, `homeassistant_stop`, `entity_registry_updated`, `device_registry_updated`, `service_registered`, `script_started`, `automation_reloaded`.

Find the event a device sends:

1. Go to Settings > Tools > Events.
2. Under Listen to events, enter the event type in Event to subscribe to, or `*` to listen to everything.
3. Only the latest 100 events are kept, so use Filter events.
4. Trigger the device and read the data. Listening changes nothing.

Then use an event trigger with that `event_type` in an automation.

## Checked

2026-11-04. Confirmed against the Events page. Nothing removed.

Method: documentation only; no commands were run.
