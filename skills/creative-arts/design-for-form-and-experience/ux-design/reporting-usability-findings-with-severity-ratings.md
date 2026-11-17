---
id: creative-arts.design-for-form-and-experience.ux-design.reporting-usability-findings-with-severity-ratings
name: reporting-usability-findings-with-severity-ratings
category: creative-arts
field: design-for-form-and-experience
product: ux-design
tags: [usability-findings-report, severity-ratings, usability-report, finding-severity, usability-issues, usability-testing]
level: practitioner
status: docs-checked
description: "Report usability findings with severity ratings: write findings with evidence, rate by impact and frequency, recommend fixes and prioritise for the team."
sources:
  - https://www.nngroup.com/articles/how-to-rate-the-severity-of-usability-problems/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Usability findings report with severity ratings

Goal: give the team a short list of problems, with evidence, ranked so the most harmful are fixed first.

## Write each finding
- **Title** as the problem ("Users miss the Save button").
- **Evidence:** how many participants, a quote or clip, a screenshot.
- **Where and task** it appeared.
- **Why it matters** (consequence for the user and the business).
- **Recommendation** (a direction, not a pixel spec).

## Rate severity
Nielsen's scale: 0 = not a usability problem at all, 1 = cosmetic only (fix if extra time is available), 2 = minor (low priority), 3 = major (important to fix, high priority), 4 = usability catastrophe (imperative to fix before release). Combine these factors into one rating: **frequency** (how often it occurs), **impact** (how hard it is to get past), **persistence** (hit once or repeatedly) and **market impact** (effect on the product's popularity). Have several evaluators rate independently, because one evaluator's ratings are unreliable; averaging about three is satisfactory for many practical purposes.

## Prioritise
Combine severity with effort to fix (see `...ux-design.building-a-ux-roadmap-with-impact-effort-prioritisation`). Group by theme.

## Verify
- [ ] Each finding has evidence and a severity.
- [ ] Rating criteria are stated.

## Checked
2026-11-01. Confirmed against NN/g "How to Rate the Severity of Usability Problems": scale 0-4, factors (including market impact, previously omitted), multiple raters. Removed: summary page, highlight-reel, readout and ticket advice, "show what worked well", and the Krug source (not read).
Method: documentation only; no commands were run.
