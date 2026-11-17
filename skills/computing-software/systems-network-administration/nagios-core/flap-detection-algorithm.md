---
id: computing-software.systems-network-administration.nagios-core.flap-detection-algorithm
name: flap-detection-algorithm
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, flap-detection, flapping, percent-state-change, 21-checks, state-transitions, flapping-notifications]
level: advanced
status: docs-checked
description: "How Nagios Core detects flapping: last 21 results, weighted percent state change, start/stop thresholds, and what happens to notifications and comments."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/flapping.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flap detection algorithm

1. Keep the last **21** check results per host/service (any result).
2. Count state transitions between consecutive results (at most 20).
3. Convert to a **weighted percent state change**; the newest change weighs 50% more than the oldest. 0% = never changes; near 100% = changes every check.
4. Compare to thresholds:
   - not flapping and value >= high threshold: **start flapping**
   - flapping and value < low threshold: **stop flapping**
   - otherwise unchanged

Example: 7 changes of 20 = 35% unweighted; weighted about 31%.

## Hosts vs services
Services are evaluated on every check (active or passive). Hosts on every host check and also during service checks, but only after at least the average service check interval has passed since the last evaluation.

## Effects
- Start: log message, non-persistent comment, "flapping start" notification, other notifications suppressed.
- Stop: log, comment removed, "flapping stop" notification, normal notification resumes.

This page gives no default threshold values. Config: `computing-software.systems-network-administration.nagios-core.flap-detection-config`.

## Checked

2026-11-04. Confirmed against the Flap Detection page: last 21 results, at most 20 transitions, newest change weighted 50% more than the oldest, 7 of 20 = 35% example with 31% weighted, start and stop comparisons, service and host evaluation rules and the flap handling lists.

Method: documentation only; no commands were run.
