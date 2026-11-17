---
id: computing-software.ux-hci-design.usability-heuristics.status-feedback-response-times
name: status-feedback-response-times
category: computing-software
field: ux-hci-design
product: usability-heuristics
tags: [response-time-limits, feedback-latency, uh-visibility-status]
level: practitioner
status: draft
description: "Choose feedback type by expected delay using Nielsen's 0.1s, 1s and 10s response-time limits."
sources:
  - https://www.nngroup.com/articles/ten-usability-heuristics/
  - https://www.nngroup.com/articles/response-times-3-important-limits/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Feedback by response time
Nielsen's three limits (from Miller 1968 and Card et al. 1991):
- **0.1 s**: feels instantaneous; no feedback needed beyond showing the result.
- **1 s**: user's flow of thought stays uninterrupted; no special indicator needed but they notice the delay.
- **10 s**: limit of keeping attention; show a progress indicator and let users cancel.

## Choose the indicator
- Under about 1 s: nothing, or a subtle state change on the control (pressed state).
- 1-10 s, unknown duration: spinner or skeleton screen.
- Over about 10 s or known length: determinate progress bar, with estimated time or step count, and a cancel path.
- Long background work: let the user leave and notify on completion.

## Gotchas
- A spinner that never resolves is worse than none; add a timeout and an error state.
- Optimistic UI (show success before the server confirms) needs a rollback path.

## Verify
- [ ] Every action over 1 s shows a state change; over 10 s shows determinate progress and cancel.
