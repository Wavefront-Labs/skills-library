---
id: computing-software.systems-network-administration.home-assistant.helpers-overview
name: helpers-overview
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [helpers, input-boolean, utility-meter]
level: intro
status: docs-checked
description: "Choose the right Home Assistant helper: stored-value helpers like toggle, number and dropdown versus calculated helpers like derivative, integral and utility meter."
sources:
  - https://www.home-assistant.io/docs/configuration/helpers/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick the helper type that fits the job.

Helpers that store a value (set by you or an automation):

- Toggle: on/off, for example to pause an automation or flag that a guest is staying.
- Number: a value set by slider or box, such as a target temperature.
- Dropdown: one option from a list you define, such as a home mode.
- Text: a short piece of text.
- Date and/or time: a date, a time or both, for example the time your alarm goes off.
- Button: pressed to start automations; remembers when it was last pressed.
- Counter (counts up, down or resets), Timer (counts down a time you set) and Schedule (on during time blocks you set for each weekday).

Helpers that calculate a value from other entities and update when they change:

- Combine the state of several sensors: minimum, maximum, average or sum.
- Derivative sensor: how fast a value changes, such as temperature rise.
- Integral sensor: a total over time, such as energy from power.
- Utility Meter: use of energy, gas or water per day, week, month or another period.
- History Stats: how long or how often an entity was in a state, such as heating on today.
- Threshold sensor: above or below a limit you set.
- Template helpers compute from a template.

Where to create one: Settings > Devices & services > Helpers, then Create helper. Helpers appear like other entities, so you can use them in automations, scripts and dashboards. A helper created in the UI is not stored in YAML; a helper set up in YAML cannot have its own settings changed in the UI.

## Checked

2026-11-04. Confirmed against the Helpers page. Removed the backticked domain ids and min_max, which are not on the page; removed the advice to prefer a built-in helper over a template; set the create path to Settings > Devices & services > Helpers.

Method: documentation only; no commands were run.
