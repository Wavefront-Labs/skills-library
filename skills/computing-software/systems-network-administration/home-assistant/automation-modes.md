---
id: computing-software.systems-network-administration.home-assistant.automation-modes
name: automation-modes
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [mode, max-exceeded, queued]
level: practitioner
status: docs-checked
description: "Choose the Home Assistant automation mode (single, restart, queued, parallel), set max, and silence warnings with max_exceeded."
sources:
  - https://www.home-assistant.io/docs/automation/modes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: control what happens when an automation starts again while it is still running.

Modes:

- `single` (default): no new run while one is active; a warning is logged.
- `restart`: stops the current run, including a running delay or wait, and starts a new one. It restarts only if the conditions are met.
- `queued`: starts the new run after the previous ones finish, in start order. A run joins the queue only if the conditions are met when it starts.
- `parallel`: starts an independent run immediately.

Limit runs with `max`. It applies to `queued` and `parallel`. In queued mode it counts the running run plus waiting runs; in parallel mode it counts simultaneous runs. Default 10, minimum 2. When the maximum is reached, the new run does not start. For `single` the maximum is effectively 1.

Silence the log warning with `max_exceeded`.

Throttle example: ignore triggers for five minutes after each run.

```yaml
automation:
  - mode: single
    max_exceeded: silent
    triggers:
      - ...
    actions:
      - ...
      # Wait 5 minutes before the automation can run again
      - delay:
          minutes: 5
```

Queue example:

```yaml
automation:
  - mode: queued
    max: 25
    triggers:
      - ...
    actions:
      - ...
```

In the UI, Queue length or Max number of parallel runs sets `max`. A long delay can be replaced by a timer.

## Checked

2026-11-04. Confirmed against the Automation modes page. Nothing removed.

Method: documentation only; no commands were run.
