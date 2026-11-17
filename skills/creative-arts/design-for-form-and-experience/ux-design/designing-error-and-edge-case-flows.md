---
id: creative-arts.design-for-form-and-experience.ux-design.designing-error-and-edge-case-flows
name: designing-error-and-edge-case-flows
category: creative-arts
field: design-for-form-and-experience
product: ux-design
tags: [edge-case-flows, error-flows, unhappy-path, alternate-flows, edge-cases-ux]
level: practitioner
status: draft
description: "Design error and edge-case flows: systematically list failure, empty, interrupted and permission cases, design recovery paths and make them testable."
sources:
  - "Nielsen Norman Group topics (nngroup.com/topics)"
  - "Don Norman, The Design of Everyday Things (revised 2013)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Error and edge-case flows

The happy path is a small part of the real design. Edge cases are rare but expensive when unhandled.

## Find the cases
For each step in a flow (see `...ux-design.drawing-user-flow-diagrams`), ask:
- **Input:** invalid, missing, too long, special characters, wrong format.
- **System:** network lost, slow response, server error, timeout, third-party failure.
- **State:** first use (empty), no results, too much data, maximum limit, expired session.
- **Permission:** not signed in, wrong role, denied camera or location.
- **User action:** cancel, back, double-click, refresh mid-task, open in two tabs.
- **Context:** small screen, slow device, assistive technology, other languages and long text.
- **Human error:** slips and mistakes (see `...ux-design.bridging-the-gulfs-of-execution-and-evaluation` and `...interaction-design.preventing-error-with-constraints-and-forcing-functions`).

## Design each
1. Prefer prevention (constraints, defaults), then clear recovery.
2. Say what happened, why and what to do next in plain words (see `...ux-design.writing-helpful-error-messages`).
3. Preserve the user's work and give an obvious way out (retry, undo, contact).
4. Add the screens and states to the flow and wireframes.

## Make them testable
Create a table: case, trigger, expected behaviour, owner. Use it for QA and in usability test tasks.

## Verify
- [ ] Every step has at least input, system and cancel cases considered.
- [ ] No dead ends: each error state offers a next action.
- [ ] Edge cases are in the QA test plan.
