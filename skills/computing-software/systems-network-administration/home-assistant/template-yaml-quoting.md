---
id: computing-software.systems-network-administration.home-assistant.template-yaml-quoting
name: template-yaml-quoting
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [quoting, value-template, multiline]
level: practitioner
status: draft
description: "Quote Home Assistant templates correctly in YAML: single-line templates need quotes, multi-line templates use a block scalar, and mixing quote types."
sources:
  - https://www.home-assistant.io/docs/templating/yaml/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: stop YAML from breaking on templates.

Single-line templates must be quoted. Without quotes, YAML reads `{{` as the start of a flow mapping and fails, and the error message can be confusing.

```yaml
value_template: "{{ states('sensor.temp') | float > 20 }}"
value_template: "{{ is_state('light.kitchen', 'on') }}"
```

When the template contains double quotes, wrap it in single quotes:

```yaml
value_template: '{{ states["sensor.temp"] }}'
```

Multi-line templates use a block scalar with `|`, which keeps line breaks:

```yaml
message: |
  Temperature: {{ states('sensor.temp') }}°C
  Humidity: {{ states('sensor.humidity') }}%
```

A multi-line template with logic:

```yaml
message: |
  {% if states('sensor.outdoor_temp') | float(0) < 0 %}
  Freezing
  {% else %}
  Fine
  {% endif %}
```

Symptoms and fixes:

- Unquoted single-line template: YAML complains about `{{`. Add quotes.
- Quote clash: use single quotes outside and double quotes inside, or the reverse.

Check the file with the configuration check, and test the template in Settings > Tools > Template (see the template-debugging skill).
