---
id: computing-software.ux-hci-design.usability-heuristics.real-world-metaphors-and-conventions
name: real-world-metaphors-and-conventions
category: computing-software
field: ux-hci-design
product: usability-heuristics
tags: [interface-metaphors, real-world-conventions]
level: practitioner
status: draft
description: "Apply familiar real-world metaphors and ordering conventions, and avoid metaphors the system cannot honour."
sources:
  - https://www.nngroup.com/articles/ten-usability-heuristics/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Metaphors and natural ordering
- Use metaphors that map cleanly (folder, trash, cart) but drop them where the system behaves differently (a trash that isn't recoverable).
- Present information in natural order: chronological, alphabetical, or by task sequence.
- Follow cultural conventions: date formats, number formats, units, reading direction (RTL layouts need mirrored navigation).
- Icons: pair with text unless universally understood; NN/g research finds many icons ambiguous.

## Gotchas
- Skeuomorphic cues can imply affordances that do not exist.
- Dates like 03/04/2026 are ambiguous across locales; use a month name or locale-aware formatting (`Intl.DateTimeFormat`).

## Verify
- [ ] Label and icon comprehension tested with representative users.
