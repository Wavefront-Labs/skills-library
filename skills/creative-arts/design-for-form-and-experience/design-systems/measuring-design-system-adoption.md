---
id: creative-arts.design-for-form-and-experience.design-systems.measuring-design-system-adoption
name: measuring-design-system-adoption
category: creative-arts
field: design-for-form-and-experience
product: design-systems
tags: [adoption-metrics, design-system-adoption, coverage-metrics, component-usage, design-system-health, roi, design-ops]
level: practitioner
status: draft
description: "Measure design system adoption: component and token coverage in code and Figma, version spread, detached instances, contribution and satisfaction metrics, then report."
sources:
  - "Nathan Curtis (EightShapes), Measuring System Adoption / Design System Metrics (eightshapes.com)"
  - "Figma Help Center - Library analytics (help.figma.com/hc/en-us/articles/4500009496215-Library-analytics)"
  - "Brad Frost, Design System Metrics (bradfrost.com/blog/post/design-system-metrics)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Measuring design system adoption

**Goal:** know whether the system is used, where it is not, and whether it pays off.

## Metrics
- **Design coverage:** share of Figma frames built from library instances; **Library analytics** (Figma) shows insertions, detachments and component usage per team; detached instance rate is a key smell.
- **Code coverage:** share of UI built from system components: static analysis with `react-scanner`, Omlet, or a custom ts-morph / ESLint script counting imports from the package vs local components; CSS token usage vs raw values (stylelint reports, project-wide grep for hex colours).
- **Version spread:** how many apps are on the latest major and how far behind others are (from lockfiles or Renovate data).
- **Contribution:** number of external PRs, request cycle time.
- **Quality and speed:** accessibility defects per release, time to ship a new screen with and without the system (pilot studies), UI bug counts.
- **Satisfaction:** quarterly survey with NPS or SUS (`creative-arts.design-for-form-and-experience.ux-design.measuring-usability-with-sus-and-seq`), support ticket volume and themes.
- **Cost:** estimated hours saved = reuse count x average build time per component (state assumptions).

## Practice
1. Pick 4-6 metrics aligned to goals (consistency, speed, accessibility); instrument automatically and snapshot monthly into a dashboard.
2. Segment by product and team to find laggards and investigate causes (missing components, poor docs).
3. Report trends and decisions, not vanity totals; pair numbers with stories and interviews.

## Verify
- [ ] Coverage measured in both Figma and code with documented method.
- [ ] Trend dashboard updated on a schedule; adopters segmented.
- [ ] Metrics lead to roadmap decisions.
