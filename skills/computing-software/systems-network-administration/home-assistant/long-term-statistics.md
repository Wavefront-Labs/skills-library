---
id: computing-software.systems-network-administration.home-assistant.long-term-statistics
name: long-term-statistics
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [statistics, state-class, recorder]
level: practitioner
status: docs-checked
description: "Understand which Home Assistant sensors get short-term and long-term statistics, how long state history is kept, and why a sensor may be missing them."
sources:
  - https://www.home-assistant.io/docs/configuration/long-term-statistics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: work out why a sensor has (or lacks) long-term history and how long data is kept.

Defaults: Home Assistant stores every state change and keeps it for 10 days. For many sensors it also stores two kinds of statistics automatically:

- Short-term statistics, every 5 minutes. Kept as long as the state history (10 days by default).
- Long-term statistics, every hour.

Retention of state history is changed with the `purge_keep_days` option of the recorder integration.

A sensor gets statistics only when all of these are true:

1. It has a state class. The integration providing the sensor usually sets it.
2. Its state is a number.
3. It is recorded. If you exclude the entity from the recorder, no statistics are kept.

Only sensor entities get statistics this way; lights and switches do not.

Check a sensor:

1. Go to Settings > Tools > States.
2. Find the sensor and look at the `state_class` attribute.
3. If you created the sensor yourself (for example a template sensor) and it has no state class, set one so statistics are produced.

Do not confuse this with the Statistics helper integration, which creates a new sensor such as the average of another sensor over the last hour. Statistics can be inspected and repaired in the Statistics tab of the developer tools.

## Checked

2026-11-04. Confirmed against the Long-term statistics page. Nothing removed.

Method: documentation only; no commands were run.
