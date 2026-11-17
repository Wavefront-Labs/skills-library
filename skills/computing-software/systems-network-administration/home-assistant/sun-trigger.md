---
id: computing-software.systems-network-administration.home-assistant.sun-trigger
name: sun-trigger
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [sunset, offset, elevation]
level: practitioner
status: docs-checked
description: "Trigger Home Assistant automations at sunrise or sunset with a time offset, or when sun elevation crosses a value using a numeric_state trigger."
sources:
  - https://www.home-assistant.io/docs/automation/trigger/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: act relative to sunrise, sunset or how dark it is.

Sunset or sunrise with an optional offset. A negative offset means before:

```yaml
automation:
  triggers:
    - trigger: sun
      # Possible values: sunset, sunrise
      event: sunset
      # Optional time offset. This example will trigger 45 minutes before sunset.
      offset: "-00:45:00"
```

Sun elevation. For a darkness-based trigger, watch the `elevation` attribute of `sun.sun` with a numeric state trigger. The value can be positive or negative:

```yaml
automation:
  - alias: "Exterior lighting on when dark outside"
    triggers:
      - trigger: numeric_state
        entity_id: sun.sun
        attribute: elevation
        # Can be a positive or negative number
        below: -4.0
    actions:
      - action: switch.turn_on
        target:
          entity_id: switch.exterior_lighting
```

Choosing between them:

- Fixed relation to sunrise or sunset, optionally shifted: the `sun` trigger with `offset`.
- Based on actual darkness: elevation with `below` (or `above`) a threshold.

Combine with a time condition (for example `after` and `before`) so the automation does not act outside the hours you want. See the automation-yaml skill for a full example that mixes a sun trigger and a time condition.

The offset is a number of seconds or `HH:MM:SS`; the docs example quotes it. For dusk or dawn, the docs suggest the Dusk, Dawn or Sun elevation crossed threshold triggers instead of a sunset offset, because twilight length changes through the year.

## Checked

2026-11-04. Confirmed against the Automation trigger page. Replaced the claim that the offset must be quoted with the page wording (number of seconds or HH:MM:SS, quoted in the example); added the dusk/dawn tip.

Method: documentation only; no commands were run.
