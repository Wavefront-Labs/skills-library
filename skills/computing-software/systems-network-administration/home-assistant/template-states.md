---
id: computing-software.systems-network-administration.home-assistant.template-states
name: template-states
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [states, state-attr, is-state]
level: practitioner
status: docs-checked
description: "Read entity states and attributes in Home Assistant templates with states(), state_attr(), is_state() and has_value(), and avoid the text-not-number trap."
sources:
  - https://www.home-assistant.io/docs/templating/states/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: get entity data into a template safely.

First look at the entity in Settings > Tools > States, and keep it open while you write.

Read a state:

```text
The kitchen light is {{ states('light.kitchen') }}.
```

Every state is text. `states('sensor.outdoor_temperature')` returns `'22.5'`, not a number, and text comparison misbehaves (`'6' < '10'` is False). Convert with a default:

```text
{{ states('sensor.outdoor_temperature') | float(0) + 5 }}
```

States have a 255 character limit.

Attributes:

```text
{{ state_attr('light.kitchen', 'brightness') }}
{{ state_attr('light.kitchen', 'brightness') | int(0) }}
```

Checks:

```text
{{ is_state('light.kitchen', 'on') }}
{{ is_state_attr('media_player.living_room', 'source', 'Spotify') }}
{% if has_value('sensor.outdoor_temperature') %}
It is {{ states('sensor.outdoor_temperature') }} outside.
{% endif %}
```

Lists: `states.light` gives every entity in the light domain.

```text
There are {{ states.light | count }} lights in total.
```

If an entity does not exist, its state object is none; reading a further attribute can fail.

Update rate: templates re-render when a used entity changes. A template that walks all states renders at most once per minute; one that walks a domain such as `states.light` at most once per second.

Inside automations the `trigger` variable is available, and in template entities the `this` variable.

## Checked

2026-11-04. Confirmed against the Templating states page. Nothing removed.

Method: documentation only; no commands were run.
