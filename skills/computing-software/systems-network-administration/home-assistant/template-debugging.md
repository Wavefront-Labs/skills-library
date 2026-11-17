---
id: computing-software.systems-network-administration.home-assistant.template-debugging
name: template-debugging
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [template-editor, tojson, typeof]
level: practitioner
status: docs-checked
description: "Debug Home Assistant templates in Settings > Tools > Template: isolate values, check types with typeof, dump attributes with tojson, and mock trigger or this."
sources:
  - https://www.home-assistant.io/docs/templating/debugging/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: find why a template returns the wrong thing.

Open Settings > Tools > Template. The editor shows the result while you type.

Method:

1. Paste the template into the editor.
2. If it uses `trigger` or `this`, define them at the top with `{% set %}` using values you expect (the editor has no real trigger).
3. Narrow it down by testing one expression at a time.
4. Remove the `{% set %}` lines when you paste it back into the automation, script or template entity.

Check a value and its type:

```text
{{ states('sensor.outdoor_temperature') }}
{{ states('sensor.outdoor_temperature') | float(0) }}
{{ states('sensor.outdoor_temperature') | float(0) | round(1) }}
{{ states('sensor.outdoor_temperature') | typeof }}
```

Dump an attribute in readable form:

```text
{{ state_attr('media_player.living_room', 'source_list') | tojson }}
```

List all attributes:

```text
{% for key, value in states.media_player.living_room.attributes.items() %}
{{ key }}: {{ value }}
{% endfor %}
```

Common mistakes:

- A template shown as literal text means the field does not support templating, or the template sits inside a `{% raw %}` block.
- There is no `print()`. Write `{{ expression }}` to show a value.
- `this` or `trigger` appearing as an error or empty result in the editor means you must define them with `{% set %}`.

## Checked

2026-11-04. Confirmed against the Templating debugging page. Nothing removed.

Method: documentation only; no commands were run.
