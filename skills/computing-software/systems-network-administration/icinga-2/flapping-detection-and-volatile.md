---
id: computing-software.systems-network-administration.icinga-2.flapping-detection-and-volatile
name: flapping-detection-and-volatile
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, flapping, enable-flapping, flapping-threshold-high, volatile, flappingstart]
level: practitioner
status: docs-checked
description: "Enable Icinga 2 flapping detection with enable_flapping and thresholds (30 and 25 percent), the weighted 20-state calculation, and volatile."
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/08-advanced-topics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# flapping detection and volatile objects
**Flapping** means a host/service changes state too often, causing a storm of problem and recovery notifications. With detection on, a flapping notification is sent and other notifications are suppressed until things calm down. It can reveal wrong thresholds, troublesome services or network problems.

Attributes: `enable_flapping`, `flapping_threshold_high`, `flapping_threshold_low`, `flapping_ignore_states`. Defaults are 30% high and 25% low: above high the object is flapping until it drops below low. `FlappingStart` and `FlappingEnd` notifications are sent if configured. There is no hard/soft distinction; all state changes count.

Calculation: the last 20 state changes are saved, weighted from 1.15 (most recent) down to 0.8 (20th); the weighted state changes divided by 20 give the percentage. Docs example: weighted sum 7.82 gives 39.1%, above 30%, so flapping; after seven more non-changing results the value falls below 25% and the object recovers.

**Volatile.** The `volatile` option treats every state change as a HARD state change, comparable to `max_check_attempts = 1`. Any NOT-OK result ignores `max_check_attempts`, triggers notifications and re-sends them on each additional NOT-OK result unless acknowledged or in downtime. A typical use is security checks. Default is false; enable only when required.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Partial read of the Icinga 2 Advanced Topics chapter: the Check Flapping, How it works and Volatile Services and Hosts sections were read in full; other sections were not. Confirmed: enable_flapping, flapping_threshold_high and low with 30% and 25% defaults, flapping_ignore_states, FlappingStart and FlappingEnd, no hard or soft distinction, 20 saved state changes weighted 1.15 down to 0.8, the 7.82 and 39.1% example, recovery after seven more non-changing results, and the volatile semantics and default false.
