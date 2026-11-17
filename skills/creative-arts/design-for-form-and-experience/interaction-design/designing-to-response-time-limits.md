---
id: creative-arts.design-for-form-and-experience.interaction-design.designing-to-response-time-limits
name: designing-to-response-time-limits
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [response-time-limits, doherty-threshold, response-time, latency, perceived-performance, laws-of-ux, system-feedback]
level: practitioner
status: docs-checked
description: "Design to human response-time limits: 0.1 s feels instant, 1 s keeps flow, 10 s loses attention; the Doherty threshold of 400 ms; feedback and perceived performance tactics."
sources:
  - https://www.nngroup.com/articles/response-times-3-important-limits/
  - https://lawsofux.com/doherty-threshold/
  - https://web.dev/articles/vitals
  - https://web.dev/articles/rail
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Response-time limits and the Doherty threshold

## The numbers
- **0.1 s (100 ms):** about the limit for the user to feel the system is reacting instantaneously; no special feedback is needed except displaying the result (direct manipulation: typing, dragging, toggles).
- **1 s:** about the limit for the user's flow of thought to stay uninterrupted, though the delay is noticed; between 0.1 and 1 s no special feedback is normally needed.
- **10 s:** about the limit for keeping the user's attention on the task. Beyond it, give a percent-done indicator and a clearly signposted way to interrupt; users will want to do other tasks while waiting.
- **Doherty threshold (400 ms):** Doherty and Thadani (IBM Systems Journal, 1982) set the target for computer response time at 400 milliseconds, replacing 2 seconds; Laws of UX summarises it as providing feedback within 400 ms.
- **Core Web Vitals** (web.dev, measured at the 75th percentile of page loads): LCP within 2.5 seconds, INP of 200 milliseconds or less, CLS of 0.1 or less.

## Design for it
1. Set **latency budgets per interaction** from the limits above and measure real-user data against them.
2. **Acknowledge immediately:** pressed states within one frame (about 16 ms at 60 frames per second, per web.dev RAIL); disable or show a spinner in the control that was clicked.
3. **Optimistic updates** for reliable actions; reconcile on failure.
4. **Skeleton screens and progressive rendering** instead of blank pages (`creative-arts.design-for-form-and-experience.interaction-design.designing-loading-skeletons-and-progress`).
5. **Prefetch and cache** likely next pages; lazy load below-the-fold; compress and size images.
6. **Perceived performance:** show something useful early, use progress with estimates, and give the waiting user something to read or do; avoid fake progress bars.

## Verify
- [ ] Latency budgets exist for key interactions and are measured.
- [ ] Every wait over 1 s has an indicator; over 10 s has progress and cancel.
- [ ] Vitals within thresholds on mid-range devices and slow networks.

## Checked
2026-11-01. Confirmed: the 0.1, 1 and 10 second limits (NN/g Response Times), the 400 ms Doherty threshold and 1982 IBM paper (Laws of UX), the three Core Web Vitals thresholds and 75th percentile (web.dev Vitals), and the 16 ms frame (web.dev RAIL). Removed: the per-interaction budget figures (100 ms, 1 s, 400 ms for search) and the 100-300 ms animation range, which no page states.
Method: documentation only; no commands were run.
