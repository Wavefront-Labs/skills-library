---
id: computing-software.systems-network-administration.zabbix.preprocessing-throttling-and-change
name: preprocessing-throttling-and-change
category: computing-software
field: systems-network-administration
product: zabbix
tags: [discard-unchanged, heartbeat, simple-change, change-per-second, throttling, change]
level: practitioner
status: docs-checked
description: "Reduce stored data with Discard unchanged (with heartbeat) and compute rates with change steps, including their restart behaviour."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/config/items/preprocessing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Four preprocessing steps depend on the previous value of an item.

Change steps:
- Simple change: current minus previous value.
- Change per second: that difference divided by elapsed seconds. Typical for counters such as interface octets.

Throttling steps:
- Discard unchanged: drop a value equal to the previous one.
- Discard unchanged with heartbeat: drop an unchanged value unless it has been unchanged for the heartbeat period (a positive number of seconds, minimum 1, time suffixes like 30s, 1m, 2h, 1d, user and LLD macros allowed).

Consequences to design for:
- A discarded value is not saved and the server has no knowledge it arrived. No trigger expressions are evaluated, so problems cannot be created or resolved from it, and functions see only the values actually stored.
- Therefore pair throttling with a heartbeat shorter than any nodata() window in your triggers, otherwise nodata() will fire on a perfectly healthy but unchanging metric.
- The previous value is held by the preprocessing manager. After a Zabbix server or proxy restart, or any edit to the item's preprocessing steps, it is reset. The next Simple change or Change per second value is ignored for lack of a baseline, and the next Discard unchanged value is never discarded.

For Numeric (unsigned) items, a float produced by Change per second or a multiplier is still accepted as a correct result.

## Checked

2026-11-03. Confirmed against the Zabbix manual pages (config/items/preprocessing): the figures, defaults, ranges, parameter and key names and behaviours stated above. Removed: nothing needed removing.

Method: documentation only; no commands were run.
