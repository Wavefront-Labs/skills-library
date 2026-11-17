---
id: computing-software.systems-network-administration.home-assistant.script-start-methods
name: script-start-methods
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [script-turn-on, wait, call-script]
level: practitioner
status: docs-checked
description: "Start a Home Assistant script from an automation by calling it directly (waits, returns a response) or with Turn on script (background, no response)."
sources:
  - https://www.home-assistant.io/docs/script/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: choose between calling a script and using Turn on script.

Call the script itself:

- In YAML, use the script as the action:

```yaml
actions:
  - action: script.wake_up
```

- The automation waits until the script finishes and can receive a response.
- If the script stops because of an error, the caller stops too.

Use the Turn on script action:

- Starts the script in the background; the caller continues at once.
- Returns no response.
- Values are passed through `variables`.
- Errors in those scripts do not affect the caller.
- If you start several scripts, they start in the order listed.

Nothing is passed automatically. The script does not see the variables or trigger data of the caller, so pass what it needs.

To do other steps while a script runs and still wait later, start it with Turn on script and wait until its entity is off again. The first script is also not stopped if the second one fails.

Script modes work like automation modes (single, restart, queued, parallel; see the automation-modes skill).

When to use a script: reusable sequences of actions that several automations call.

## Checked

2026-11-04. Confirmed against the Scripts page. Replaced script.turn_on with the Turn on script action wording used on the page.

Method: documentation only; no commands were run.
