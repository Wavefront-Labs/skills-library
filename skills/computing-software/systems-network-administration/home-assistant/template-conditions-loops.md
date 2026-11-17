---
id: computing-software.systems-network-administration.home-assistant.template-conditions-loops
name: template-conditions-loops
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [if, for-loop, set]
level: practitioner
status: docs-checked
description: "Use if/elif/else, inline if, for loops with filtering, and set in Home Assistant templates, including how to close each block."
sources:
  - https://www.home-assistant.io/docs/templating/loops-and-conditions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: add logic to templates.

if / elif / else lives in `{% %}` markers and must be closed with `{% endif %}`. `else` is optional. Home Assistant checks `elif` branches in order and runs the first that matches.

```text
{% set temp = states('sensor.outdoor_temperature') | float(0) %}
{% if temp < 0 %}
Freezing
{% elif temp < 15 %}
Cool
{% else %}
Warm
{% endif %}
```

Inline if for choosing between two values:

```text
{% set temp = 22 %}
It is {{ 'warm' if temp > 20 else 'cool' }}.
```

for loops must be closed with `{% endfor %}`:

```text
{% for light in states.light %}
{{ light.name }}: {{ light.state }}
{% endfor %}
```

Filter inside the loop header:

```text
{% for light in states.light if light.state == 'on' %}
- {{ light.name }}
{% endfor %}
```

`set` stores a value in a variable. A common gotcha is that a variable set inside a loop does not carry out of the loop. The docs cover how to work around that, plus breaking out of loops early and the `do` statement.

Pair these with state reads from the template-states skill.

## Checked

2026-11-04. Confirmed against the Templating loops and conditions page. Removed the whitespace remark, which is not on the page.

Method: documentation only; no commands were run.
