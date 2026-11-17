---
id: creative-arts.design-for-form-and-experience.interaction-design.designing-loading-skeletons-and-progress
name: designing-loading-skeletons-and-progress
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [skeleton-screens, progress-indicators, loading-states, spinners, perceived-performance, ui-states, loading-skeleton]
level: practitioner
status: docs-checked
description: "Design loading states: choose skeleton screens, spinners or progress bars by wait time, keep layout stable, show real progress where known and manage perceived speed."
sources:
  - https://www.nngroup.com/articles/response-times-3-important-limits/
  - https://www.nngroup.com/articles/skeleton-screens/
  - https://www.nngroup.com/articles/progress-indicators/
  - https://web.dev/articles/vitals
  - https://www.w3.org/TR/wai-aria-1.2/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Loading skeletons and progress indicators

**Goal:** waiting feels short and predictable, and layout does not jump.

## Choose by duration
- **Under about 0.1 s:** show nothing; it feels instant.
- **0.1-1 s:** no special indicator is normally needed; a subtle state change on the control (pressed, disabled) is enough. NN/g warns a looped animation for under 1 s is distracting.
- **About 2-10 s:** a looped animation such as a spinner (NN/g). Use **skeleton screens** for full-page loads (grey placeholders matching layout); put spinners for button actions inside the button.
- **10 s or more:** a **percent-done progress bar**, with an estimate of when it finishes (or step counts when percentages are hard to compute) and a clear way to cancel or continue elsewhere.

## Skeletons
- Mirror the final layout (blocks for image, lines for text), subtle shimmer or pulse.
- Load in priority order; render real content as it arrives, region by region.
- Do not use for tiny widgets (use a spinner) or for content that may never appear.

## Progress
- Determinate when you can measure; otherwise honest indeterminate with a status message ("Uploading 3 of 8 files"). NN/g notes a bar that races ahead and then hangs frustrates users.
- Optimistic UI for fast, reliable actions (like, send): show the result immediately, roll back with an explanation on failure.
- Maintain **layout stability:** reserve space (aspect ratios, min-heights); web.dev treats a Cumulative Layout Shift of 0.1 or less as good.

## Accessibility
`role="progressbar"` with `aria-valuenow`, `aria-valuemin` and `aria-valuemax`; `aria-busy` on loading regions; a polite live announcement ("Loading results", "12 results loaded").

## Verify
- [ ] Indicator type matches the wait duration; no flash for instant loads.
- [ ] Skeleton matches layout; no layout shift on load.
- [ ] Progress is announced to assistive tech.

## Checked
2026-11-01. Confirmed: duration bands (NN/g Response Times and Progress Indicators), skeleton screens for full-page loads (NN/g Skeleton Screens 101), CLS threshold (web.dev Vitals), ARIA progressbar and live-region attributes (WAI-ARIA 1.2). Removed: the 200-300 ms show-delay and 400-500 ms minimum-display figures, the reduced-motion note, and the Material 3 source (page unreadable).
Method: documentation only; no commands were run.
