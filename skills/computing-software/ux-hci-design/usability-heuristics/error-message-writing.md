---
id: computing-software.ux-hci-design.usability-heuristics.error-message-writing
name: error-message-writing
category: computing-software
field: ux-hci-design
product: usability-heuristics
tags: [error-message-writing, error-message-guidelines, uh-error-recovery]
level: practitioner
status: draft
description: "Write errors in plain language that state the problem, cause and a concrete next step, placed next to the problem."
sources:
  - https://www.nngroup.com/articles/ten-usability-heuristics/
  - https://www.nngroup.com/articles/error-message-guidelines/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Error message formula
1. Say what happened in plain words (no codes alone, no blame).
2. Say why, if known.
3. Say how to fix it, or give an action (Retry / Edit).

Bad: "Invalid input". Better: "Enter a date as DD/MM/YYYY, for example 31/01/2026".
- Place the message adjacent to the field; mark with icon and text, not colour alone (WCAG 1.4.1).
- Preserve what the user typed.
- For server failures give a reference id and a safe way to retry.

## Verify
- [ ] Each error message names the field and the fix; fields keep their values.
