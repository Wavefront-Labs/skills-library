---
id: computing-software.ux-hci-design.interaction-design.loading-states-skeleton-screens
name: loading-states-skeleton-screens
category: computing-software
field: ux-hci-design
product: interaction-design
tags: [skeleton-screens, loading-indicators]
level: practitioner
status: draft
description: "Choose skeletons, spinners or progress bars by load duration and keep layout stable."
sources:
  - https://www.nngroup.com/articles/skeleton-screens/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Loading states
- Skeleton screens suit full-page or content-heavy loads of about 2-10 s and reduce perceived wait; spinners for short, small, indeterminate waits; progress bars when duration is known or over 10 s.
- Reserve space (set dimensions) to avoid layout shift (Cumulative Layout Shift).
- Load most important content first; lazy load below the fold.
- Provide `aria-busy="true"` on updating regions and announce completion.

## Verify
- [ ] Throttle network to slow 3G: states look sensible, no layout jumps.
