---
id: creative-arts.design-for-form-and-experience.interaction-design.defining-microinteraction-rules
name: defining-microinteraction-rules
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [microinteraction-rules, interaction-rules, state-logic, micro-interactions, edge-conditions, saffer-microinteractions]
level: practitioner
status: draft
description: "Define microinteraction rules: what happens after the trigger, with the allowed actions, limits, defaults, sequence and failure cases written as a testable specification."
sources:
  - "Dan Saffer, Microinteractions: Designing with Details (O'Reilly, 2013)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Microinteraction rules

Rules are the invisible logic that determines what happens once the trigger fires: the steps allowed, their order, the limits and what the system does in each case. Saffer notes they should be simple, with few choices and a clear end.

## Define
1. **Goal:** one small task the microinteraction accomplishes (set an alarm, like a post).
2. **Sequence:** the steps from trigger to end; fewer is better.
3. **Allowed inputs and limits:** valid ranges, maximum length, step sizes, what is disabled.
4. **Defaults:** the most likely value pre-selected; remember the last choice if that matches behaviour.
5. **Constraints and edge cases:** what if the network fails, input is out of range, or two events arrive at once (see `...ux-design.designing-error-and-edge-case-flows`).
6. **What the user cannot do:** removing impossible options is better than error messages.
7. **End conditions:** when the interaction is finished and the system returns to rest; what is saved.

## Write it down
Use a state table: state, event, condition, action, next state. Add timing rules (debounce, timeout, delay before an auto-dismiss).

## Verify
- [ ] Every state has a defined exit.
- [ ] Conflicting or simultaneous events are specified.
- [ ] A developer can build it from the table without asking.
