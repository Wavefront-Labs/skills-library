---
id: creative-arts.design-for-form-and-experience.ux-design.measuring-usability-with-sus-and-seq
name: measuring-usability-with-sus-and-seq
category: creative-arts
field: design-for-form-and-experience
product: ux-design
tags: [system-usability-scale, sus, single-ease-question, seq, ux-metrics, usability-metrics, questionnaire, ux-research]
level: practitioner
status: draft
description: "Score the System Usability Scale (10 items, 0-100) and the Single Ease Question (7-point) correctly, interpret against benchmarks, and report with confidence intervals."
sources:
  - https://measuringu.com/sus/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SUS and SEQ

**Goal:** collect two cheap standardised measures: **SEQ** after each task, **SUS** after the whole session or release.

## SEQ (Single Ease Question)
"Overall, this task was: Very difficult (1) ... Very easy (7)." Ask right after each task. (SEQ wording and benchmarks are not confirmed here; look them up before quoting a benchmark.)

## SUS items (odd are positive, even negative; 1 strongly disagree to 5 strongly agree)
1 I think I would like to use this system frequently. 2 I found it unnecessarily complex. 3 I thought it was easy to use. 4 I think I would need technical support to use it. 5 The functions were well integrated. 6 Too much inconsistency. 7 Most people would learn it very quickly. 8 Very cumbersome to use. 9 I felt very confident. 10 I needed to learn a lot before I could get going.

## Scoring (the part people get wrong)
- Odd item: score = response - 1. Even item: score = 5 - response.
- Sum the ten, multiply by 2.5: result 0-100. It is **not a percentage**.
- Across 500 studies the mean SUS is 68. Above about 80 is grade A, around 68 is C, below 51 is F.
- Report the mean with a **confidence interval**; small samples give a wide interval.


## Gotchas
- SUS measures perceived usability of one system, so compare versions of the same product or against benchmarks, not across unlike product types without care.
- Ask SUS only of people who have used the product.

## Verify
- [ ] Scoring rule applied per item (odd minus 1, even 5 minus), times 2.5.
- [ ] Mean plus confidence interval reported with n.
- [ ] SEQ gathered per task, not per session.
