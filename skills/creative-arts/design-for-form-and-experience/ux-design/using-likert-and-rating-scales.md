---
id: creative-arts.design-for-form-and-experience.ux-design.using-likert-and-rating-scales
name: using-likert-and-rating-scales
category: creative-arts
field: design-for-form-and-experience
product: ux-design
tags: [likert-scale, rating-scale, survey-design, ordinal-data, questionnaire, ux-research]
level: practitioner
status: docs-checked
description: "Choose and label Likert and rating scales: number of points, word labels, semantic-differential pairs, N/A option, and acquiescence and social-desirability bias."
sources:
  - https://www.nngroup.com/articles/rating-scales/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Likert and rating scales

**Goal:** scales that respondents use consistently and that you can interpret honestly.

## Design choices (NN/g)
- **Points:** Likert items typically use 5 points, though 7 or 9 occur. Semantic differentials typically use 7 (the SEQ example is 7-point).
- **Labels:** Likert options carry word labels; use standard agreement wording rather than inventing options. For semantic differentials only the two poles are typically labelled, with intermediate points numbered or worded "very" or "somewhat". Labelled scales are easier to understand, but intermediate words are hard to choose.
- **Semantic-differential pairs:** use true opposites and test them with users first.
- **"Not applicable":** add it so neutral respondents can be told apart from those who find the question irrelevant.
- **Acquiescence:** respondents tend to agree, and wording can prime them. Alternating positive and negative statements reduces it, but can confuse participants and researchers, who must code the two directions differently.
- **Social desirability:** asking for names or other identifiers increases it, so do not collect them.
- For ease-of-use measurement, prefer standardised questionnaires with psychometric testing (SUS, SUPR-Q) over custom scales.

## Verify
- [ ] Points, labels and direction decided deliberately and applied consistently.
- [ ] No identifiers collected where honesty matters.

## Checked
2026-11-01. Confirmed against NN/g "Rating Scales in UX Research". Removed: midpoint and 7-point reliability claims, ordinal-analysis, top-box, Mann-Whitney and effect-size advice, slider and mobile claims, and the Likert and Sauro and Lewis sources (not read). The page does not cover analysis; look elsewhere before reporting means.
Method: documentation only; no commands were run.
