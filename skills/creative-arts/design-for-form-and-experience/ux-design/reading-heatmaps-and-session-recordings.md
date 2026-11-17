---
id: creative-arts.design-for-form-and-experience.ux-design.reading-heatmaps-and-session-recordings
name: reading-heatmaps-and-session-recordings
category: creative-arts
field: design-for-form-and-experience
product: ux-design
tags: [heatmaps, session-recordings, session-replay, behavioural-analytics, hotjar, microsoft-clarity, product-analytics]
level: practitioner
status: draft
description: "Use heatmaps and session recordings responsibly: pick the right map type, sample enough sessions, read rage and dead clicks, and treat findings as hypotheses to test."
sources:
  - "Nielsen Norman Group - Heatmaps and eyetracking visualisations (nngroup.com/articles/heatmaps-visualizations)"
  - "Microsoft Clarity documentation - heatmaps, rage clicks, dead clicks (learn.microsoft.com/clarity)"
  - "Hotjar Help - Heatmaps and Recordings (help.hotjar.com)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Heatmaps and session recordings

**Goal:** see what users actually do on a page, to generate and prioritise hypotheses, not to prove them.

## Map types
- **Click/tap map:** where people click, including non-clickable things (a sign of expected affordance).
- **Scroll map:** how far down people get; the fold of attention drop is where content stops being seen.
- **Move/attention map:** mouse movement (a rough proxy for gaze, weak on mobile).
Segment by device; desktop and mobile layouts need separate maps.

## Setup
- Install the tool snippet with consent handling and **mask inputs and sensitive elements** (payment, passwords, personal data) before recording.
- Aim for **1,000+ pageviews per device** per map; for recordings, watch 20-30 sessions per question, filtered to the segment and event (e.g. sessions that hit the checkout error).

## Reading signals
- **Rage clicks** (repeated fast clicks) and **dead clicks** (clicks with no response) flag broken or misleading elements.
- **U-turns and quick-backs** show wrong expectations; **excessive scrolling** shows hunting for content.
- Compare to the funnel: look where drop-off is, not at random pages.

## Gotchas
- Dynamic content (carousels, modals) smears heatmaps; use state-specific captures.
- Heat shows where, not why; log a hypothesis, then test it (`creative-arts.design-for-form-and-experience.ux-design.designing-an-ab-test`) or ask users.
- Recordings are personal data under GDPR and similar rules; retention limits and access control apply.

## Verify
- [ ] Sensitive fields masked; consent respected.
- [ ] Segmented by device with adequate sample.
- [ ] Each observation written as a hypothesis with a follow-up.
