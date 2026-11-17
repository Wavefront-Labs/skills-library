---
id: creative-arts.design-for-form-and-experience.interaction-design.prioritising-content-mobile-first
name: prioritising-content-mobile-first
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [mobile-first, mobile-first-design, content-prioritisation, progressive-enhancement, responsive-design, small-screen-first]
level: practitioner
status: draft
description: "Design mobile-first: rank content and tasks for the smallest screen, then add for larger ones, using min-width queries and progressive enhancement."
sources:
  - "Luke Wroblewski, Mobile First (A Book Apart, 2011)"
  - "Nielsen Norman Group topics (nngroup.com/topics)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Mobile-first prioritisation

Luke Wroblewski's argument for mobile first is that small screens force focus on what matters, that mobile use is growing, and that mobile has capabilities (location, touch, camera) desktop lacks.

## Steps
1. **List user tasks and content,** and rank them (see `...ux-design.writing-a-content-priority-guide`). The small screen forces a choice: what must be here?
2. **Design the small layout first** in one column; large touch targets (see `...interaction-design.sizing-touch-targets`); a primary action reachable by the thumb; short forms (see `...interaction-design.laying-out-forms-and-ordering-fields`).
3. **Use progressive enhancement:** the base experience works everywhere; add features and richer layout for larger screens or capable devices.
4. **Write CSS mobile-first:** base styles for the small screen; `min-width` media queries add layout as space allows.
5. **Move, do not hide:** content that matters on desktop should have a mobile form (collapse, accordion, tabs) rather than removal.
6. **Consider performance:** smaller images, lazy-loaded media, fewer scripts.
7. **Add larger-screen enhancements** (multi-column, side panels, hover affordances) without making them the only route.

## Gotchas
- Cutting features for mobile that mobile users need.
- Assuming mobile means "on the go"; many users are at home on a phone.

## Verify
- [ ] The core task is complete on the smallest layout.
- [ ] Large-screen additions are enhancements, not requirements.
- [ ] The CSS uses min-width queries.
