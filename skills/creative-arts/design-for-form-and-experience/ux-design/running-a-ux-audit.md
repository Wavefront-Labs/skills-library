---
id: creative-arts.design-for-form-and-experience.ux-design.running-a-ux-audit
name: running-a-ux-audit
category: creative-arts
field: design-for-form-and-experience
product: ux-design
tags: [ux-audit, ux-review, usability-audit, analytics-review, ux-research]
level: practitioner
status: docs-checked
description: "Audit a live product: scope the journeys, combine analytics, heuristic review and accessibility checks, and deliver a prioritised issue log with evidence and quick wins."
sources:
  - https://web.dev/articles/vitals
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# UX audit of a live product

**Goal:** a time-boxed, evidence-based review of an existing product that ends in a ranked list of fixes the team can schedule.

## Steps
1. **Frame:** business goals, target users, the key journeys (sign-up, search to purchase, support contact). Agree what is out of scope.
2. **Gather quantitative evidence:** funnel drop-off per journey, top exit pages, search terms with zero results, support ticket themes, Core Web Vitals (web.dev targets: LCP within 2.5 seconds, INP 200 milliseconds or less, CLS 0.1 or less, measured at the 75th percentile of page loads).
3. **Inspect qualitatively:** heuristic evaluation of each journey (`creative-arts.design-for-form-and-experience.ux-design.heuristic-evaluation-with-nielsens-ten`), a quick accessibility pass (keyboard-only run, contrast with a checker, a screen-reader smoke test), content and IA review.
4. **Triangulate:** a finding is strong when two sources agree (analytics shows 60 percent drop at step 3 and the heuristic review flags unclear validation there).
5. **Log issues** in a sheet: ID, journey/screen, observation, evidence link, heuristic or WCAG criterion, severity, effort (S/M/L), recommendation.
6. **Prioritise** on severity against effort; flag quick wins (high severity, small effort) and items that need research before a fix.
7. **Report:** one-page summary, top issues with annotated screenshots, then the full log as appendix. Present it rather than just emailing it.

## Gotchas
- Opinions without evidence get argued away; every row needs a screenshot or metric.
- Auditing every page is a trap. Journeys, not sitemap.
- State the audit date and product version; live products change under you.

## Verify
- [ ] Each journey has analytics evidence and an inspection result.
- [ ] Every issue carries severity, effort and a recommendation.
- [ ] The summary names the top fixes and what to research further.

## Checked
2026-11-01. Confirmed against web.dev, Web Vitals: LCP, INP and CLS targets and the 75th-percentile measure. The audit procedure itself is practitioner convention with no figures; the NN/g and IDF audit pages were not readable or not read. Removed: half-day framing, 3-5 journey count, 0-4 severity scale, top-10 count, the NN/g and IDF sources.
Method: documentation only; no commands were run.
