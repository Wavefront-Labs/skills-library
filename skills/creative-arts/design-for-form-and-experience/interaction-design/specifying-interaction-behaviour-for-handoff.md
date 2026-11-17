---
id: creative-arts.design-for-form-and-experience.interaction-design.specifying-interaction-behaviour-for-handoff
name: specifying-interaction-behaviour-for-handoff
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [interaction-specs, behaviour-specs, interaction-spec, design-handoff, interaction-documentation, state-specification]
level: practitioner
status: draft
description: "Specify interaction behaviour for engineers: triggers, states, transitions, validation rules, timing, error and empty cases in a table, backed by a prototype link."
sources:
  - "Nielsen Norman Group topics (nngroup.com/topics)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Interaction behaviour specs

A prototype shows one path; a behaviour spec captures the complete rules so developers do not guess.

## Contents
1. **Component or screen name, purpose and entry points.**
2. **State table:** state, how the user gets there, what is shown, what is enabled (default, hover, focus, pressed, loading, success, error, disabled, empty).
3. **Events and responses:** per event (click, long-press, swipe, key press), the response and the next state; keyboard equivalents (see `...interaction-design.designing-keyboard-operability-and-focus-order`).
4. **Data rules:** validation (when it runs: on blur or on submit), formats, limits, defaults, sorting, pagination or loading approach.
5. **Timing:** debounce, minimum display time for loaders, auto-dismiss durations, timeouts (see `...interaction-design.defining-microinteraction-rules`).
6. **Edge cases:** long text, zero or one or many items, offline, errors (see `...ux-design.designing-error-and-edge-case-flows`).
7. **Responsive and platform variation.**
8. **Analytics events** to track, if any.
9. **Links:** the prototype, the flow, the tickets, acceptance criteria.

## Format
A short document or a page in the design file, with the state diagram or flow plus tables. Keep it in the same place as the design and update it with changes (see `...design-systems.versioning-deprecating-and-changelogging`).

## Verify
- [ ] Every state and event is in a table.
- [ ] A developer can write acceptance tests from it.
- [ ] It links to the current design version.
