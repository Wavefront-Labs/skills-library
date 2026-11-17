---
id: computing-software.systems-network-administration.home-assistant.trigger-ids
name: trigger-ids
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [trigger-id, multiple-triggers, id]
level: practitioner
status: draft
description: "Combine several triggers in one Home Assistant automation and label each with an id so conditions and actions can tell which one fired."
sources:
  - https://www.home-assistant.io/docs/automation/trigger/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: start one automation from several triggers and branch on which one fired.

List several triggers and any of them starts the automation:

```yaml
automation:
  triggers:
    - trigger: time_pattern
      minutes: 5
    - trigger: sun
      event: sunset
```

A state trigger can watch several entities:

```yaml
automation:
  triggers:
    - trigger: state
      entity_id:
        - sensor.one
        - sensor.two
        - sensor.three
```

Add `id` to a trigger so later steps can identify it:

```yaml
automation:
  triggers:
    - trigger: event
      event_type: "MY_CUSTOM_EVENT"
      id: "custom_event"
    - trigger: mqtt
      topic: "living_room/switch/ac"
      id: "ac_on"
    - trigger: state  # This trigger will be assigned id="2"
      entity_id:
        - device_tracker.paulus
        - device_tracker.anne_therese
      to: "home"
```

A trigger without an `id` gets its position in the list as a string, so the third trigger is `"2"`.

Use the id with the Triggered by condition, or in a template as `trigger.id`. Give separate triggers different ids when the actions should differ, and keep ids short and descriptive so the trace and condition editor stay readable.
