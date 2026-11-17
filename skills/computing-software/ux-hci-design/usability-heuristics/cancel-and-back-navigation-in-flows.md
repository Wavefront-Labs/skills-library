---
id: computing-software.ux-hci-design.usability-heuristics.cancel-and-back-navigation-in-flows
name: cancel-and-back-navigation-in-flows
category: computing-software
field: ux-hci-design
product: usability-heuristics
tags: [wizard-back-navigation, flow-resume]
level: practitioner
status: draft
description: "Keep entered data when users go back, allow editing earlier steps, and let abandoned flows resume."
sources:
  - https://www.nngroup.com/articles/ten-usability-heuristics/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multi-step flow control
- Back must preserve all previously entered values.
- Show a review step with Edit links to each section before final submit.
- Persist drafts (server-side or local) so a refresh or timeout does not wipe the flow.
- Do not trap users: skippable optional steps, clear exit that explains what is saved.

## Verify
- [ ] Go to step 3, back to 1, change a value, forward: later values remain.
