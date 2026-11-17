---
id: computing-software.systems-network-administration.home-assistant.durations
name: durations
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [duration, for, delay]
level: intro
status: docs-checked
description: "Write durations in Home Assistant YAML: seconds, HH:MM:SS, HH:MM or a days/hours/minutes mapping, and where templates are allowed."
sources:
  - https://www.home-assistant.io/docs/automation/durations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: enter a duration for `for`, `delay` or a wait timeout without a unit mistake.

Durations are used by the For at least option of triggers and conditions, the Delay action, and the timeout of the wait actions.

Accepted YAML formats:

- Seconds as a number: `300` is 5 minutes.
- `HH:MM:SS`: `"00:01:30"` is 1 minute 30 seconds.
- `HH:MM`: `"01:30"` is 1 hour 30 minutes. That is hours and minutes, not minutes and seconds.
- A mapping of `days`, `hours`, `minutes`, `seconds`, `milliseconds`:

```yaml
for:
  minutes: 5
  seconds: 30
```

Device triggers and device conditions accept only the mapping format.

Where `for` goes: most triggers and conditions expect `for` under `options:`; each trigger or condition page shows its own YAML example.

In the UI, enter hours, minutes and seconds. The Delay action and wait timeouts also accept milliseconds.

Templates in durations: the For at least option of the State changed, Numeric state crossed threshold and Template triggers, For at least on the State condition, and the Delay action accept a template. In the UI, choose Template instead of Duration under For at least.

Write `HH:MM` and `HH:MM:SS` values in quotes, as the docs examples do.

## Checked

2026-11-04. Confirmed against the Durations page. Reworded the quoting line: the page quotes the values in examples but does not give a reason.

Method: documentation only; no commands were run.
