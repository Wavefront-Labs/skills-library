---
id: computing-software.cloud-infrastructure-engineering.saltstack.states-ordering
name: states-ordering
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, states, ordering, order, state-auto-order, requisites]
level: practitioner
status: docs-checked
description: "Control Salt state execution order: state_auto_order, requisites overriding file order, the numeric order option and order: last."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/ref/states/ordering.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# State ordering

- Auto ordering: states run in the same order on every system. Master option `state_auto_order` defaults to `True`; `False` switches to lexicographic (classic) ordering.
- Requisites (`require`, `watch`, `prereq`) override file order. An `sls` requisite chains across SLS files, so a state can wait on a whole included state.
- `order`: a numeric value sets position; the page says a state with order 1 is installed in tandem with any other state set to order 1; states without `order` run after all states that have one.
- `order: last` sends a state to the end. Numeric values only cover the beginning of the sequence.
- Requisites take priority over `order`, so do not combine `order` with requisites it depends on or that depend on it.

## Checked

2026-11-04: read the Salt ordering page in full. Confirmed state_auto_order and its default, requisites overriding file order, sls requisites, the order option, unordered states running last and order: last. Reworded the equal-numbers claim to match the page.

Method: documentation only; no commands were run.

