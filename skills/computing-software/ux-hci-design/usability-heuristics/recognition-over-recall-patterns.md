---
id: computing-software.ux-hci-design.usability-heuristics.recognition-over-recall-patterns
name: recognition-over-recall-patterns
category: computing-software
field: ux-hci-design
product: usability-heuristics
tags: [recognition-over-recall, memory-load, uh-recognition-recall]
level: practitioner
status: draft
description: "Show options, recent items and context so users recognise rather than remember."
sources:
  - https://www.nngroup.com/articles/ten-usability-heuristics/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reduce memory load
- Show menus/commands rather than requiring typed commands; offer autocomplete and recent searches.
- Keep relevant info visible when it is needed in the next step (don't make users remember a code from a previous page).
- Provide examples and format hints at fields; placeholder text disappears, so keep persistent labels.
- Show recently used items and favourites.

## Gotchas
- Placeholder-only labels force recall and fail WCAG 3.3.2 in practice.
- Too many visible options trade recall for overload; chunk and prioritise.

## Verify
- [ ] No task step requires remembering data from an earlier screen.
