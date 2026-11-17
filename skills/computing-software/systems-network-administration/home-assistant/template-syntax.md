---
id: computing-software.systems-network-administration.home-assistant.template-syntax
name: template-syntax
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [jinja, expressions, filters]
level: intro
status: docs-checked
description: "Read and write Home Assistant template syntax: {{ }} versus {% %}, operators, filters with the pipe, is tests, and the filter-before-math precedence trap."
sources:
  - https://www.home-assistant.io/docs/templating/syntax/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: write correct templates the first time.

Markers:

- `{{ ... }}` calculates and shows the result.
- `{% ... %}` runs logic and adds nothing to the output by itself.

```text
Hello, {{ states('person.frenck') }}.
{% if is_state('sun.sun', 'below_horizon') %}
It is dark outside.
{% endif %}
```

Expressions can read state data: `{{ states.sensor.outdoor.state }}` or `{{ states.sensor.outdoor.attributes.friendly_name }}`.

Operators:

- Math: `+`, `-`, `*`, `/`, integer division `//`, remainder `%`, power `**`.
- Comparison: `==`, `!=`.
- Logic.

Filters transform a value with the pipe and chain left to right:

```text
Upper case: {{ 'hello' | upper }}
Rounded:    {{ 3.14159 | round(2) }}
Chained:    {{ [3, 1, 2] | sort | join(', ') }}
```

Tests ask yes/no questions with `is`, or `is not` for the opposite:

```text
{{ 42 is number }}
{{ 3 is in [1, 2, 3] }}
{{ 42 is not number }}
```

Trap: the pipe binds tighter than math. `{{ 10 / 3 | round(2) }}` runs as 10 divided by (3 rounded), giving 3.3333333333333335, not 3.33. Add parentheses:

```text
{{ (10 / 3) | round(2) }}
```

Whitespace: templates keep every space and newline you write, including those around `{% if %}` and `{% set %}` tags. Trim them when output must be clean, such as a sensor value.

The template functions reference lists all filters with examples.

## Checked

2026-11-04. Confirmed against the Templating syntax page. Nothing removed.

Method: documentation only; no commands were run.
