---
id: computing-software.systems-network-administration.home-assistant.testing-and-traces
name: testing-and-traces
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [traces, run-actions, simulated-trigger]
level: practitioner
status: draft
description: "Test a Home Assistant automation safely: trigger it from the Actions tool, run with a simulated trigger, and read traces (last 5 kept per automation)."
sources:
  - https://www.home-assistant.io/docs/automation/testing/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: prove an automation works without waiting for the real event.

Test the parts:

- Conditions: check the current state of a condition, or disable it to run without it (`enabled: false` in YAML).
- Actions: test one action or all actions from the editor.

Trigger it manually from the Actions tool:

1. Go to Settings > Tools > Actions.
2. In Action, select Trigger automation.
3. Select Add target and choose the automation.
4. Perform the action.

This runs without trigger data. There is no trigger ID, a Triggered by condition is never met, and templates that read `trigger` find nothing.

Simulated trigger: when the conditions or actions depend on which trigger fired, run with a simulated trigger. You simulate the state change or event the trigger reacts to, and the automation runs from the start with real trigger data. It works for state, numeric state and manual event triggers. For time or MQTT triggers, cause the real thing instead.

Risk: simulating a state change or firing an event starts every automation with a trigger on it, and those control real devices. Review which automations react first.

Traces:

- Home Assistant keeps the last 5 traces of each automation.
- Traces marked Did not trigger are kept separately and never replace real runs.
- Open a trace to follow each step, view changed variables, and download it for sharing.
