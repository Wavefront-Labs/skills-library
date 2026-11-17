---
id: computing-software.systems-network-administration.zabbix.recovery-expressions-and-hysteresis
name: recovery-expressions-and-hysteresis
category: computing-software
field: systems-network-administration
product: zabbix
tags: [recovery-expression, hysteresis, flapping, ok-event-generation, recovery]
level: practitioner
status: docs-checked
description: "Prevent trigger flapping with a separate recovery expression so a problem clears only past a lower threshold."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/config/triggers/expression
  - https://www.zabbix.com/documentation/current/en/manual/config/triggers/trigger
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default the problem expression decides both states: TRUE creates a problem and the problem is resolved as soon as the expression is FALSE. For hysteresis, set OK event generation to Recovery expression and add a second expression.

Illustrative example (placeholder item and thresholds, not from the docs):
Problem expression: last(/host/key)>HIGH
Recovery expression: last(/host/key)<=LOW   (LOW lower than HIGH)

Recovery then takes two steps: the problem expression must evaluate FALSE, and the recovery expression must evaluate TRUE. Between LOW and HIGH the trigger stays in Problem, so a value hovering near HIGH does not flap.

Rules (trigger configuration page):
- Recovery expression is optional, defines additional conditions to meet before the problem is resolved, after the problem expression has already evaluated FALSE.
- It is not possible to resolve a problem by the recovery expression alone if the problem expression is still TRUE.
- The Recovery expression field is only available when OK event generation is set to Recovery expression.
- OK event generation options: Expression (OK events use the same expression as problem events), Recovery expression, or None (the trigger never returns to OK on its own, so rely on manual close or correlation).
- Allow manual close lets an operator close problems of this trigger manually when acknowledging them.

Use hysteresis for thresholds that hover near a limit. A sustained-window function in the problem expression, in the style min(/host/key,5m)>VALUE, also helps avoid transient spikes (the expression page shows min over 5m in a trigger example).

## Checked

2026-11-09. Confirmed against the trigger configuration page (OK event generation, Recovery expression, Allow manual close) and the trigger expression page (min over 5m example). Removed: the claimed docs temperature example with numeric thresholds and the {TRIGGER.VALUE}-is-always-1 claim, neither of which appears on the cited pages; replaced the numbers with placeholders.
Method: documentation only; no commands were run.
