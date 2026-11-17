---
id: creative-arts.design-for-form-and-experience.ux-design.sampling-and-analysing-a-ux-survey
name: sampling-and-analysing-a-ux-survey
category: creative-arts
field: design-for-form-and-experience
product: ux-design
tags: [survey-sampling, survey-analysis, response-bias, sample-size, margin-of-error, survey-design, ux-research]
level: practitioner
status: draft
description: "Recruit a defensible survey sample, estimate size and margin of error, spot response and non-response bias, and analyse open and closed answers into findings."
sources:
  - "Sauro and Lewis, Quantifying the User Experience, 2nd ed. (2016)"
  - "Pew Research Center - Methods: sampling and weighting (pewresearch.org/our-methods)"
  - "Nielsen Norman Group - Survey Design topic (nngroup.com/topic/survey)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sampling and analysing a UX survey

## Sampling
1. **Define the population** (active paying users in the last 90 days), then the **sampling frame** (the list you can reach). Mismatch between them is the first bias source.
2. **Random sample** from the frame when you need to generalise. Convenience samples (pop-up on the site, social post) are fine for exploring but report them as such.
3. **Size:** for a proportion at 95 percent confidence, n is about 1.96 squared times p(1-p) divided by e squared; with p = 0.5 and 5 percent margin that is about 385, 10 percent margin about 96. Correct for small populations with n adjusted = n / (1 + (n-1)/N).
4. **Expect response rates** of 5-30 percent for in-product or email invites; invite 5-10 times your target n.

## Bias to check
- **Non-response bias:** compare responders with the invited list on known attributes (plan, tenure, region); weight or caveat if they differ.
- **Self-selection:** people with strong opinions respond; do not read satisfaction as population-wide.
- **Survivorship:** exit surveys miss users who left silently.
- **Satisficing:** flag very fast completions and straight-lining; drop with a rule fixed beforehand.

## Analysis
- Clean first (duplicates, speeders, impossible values) and document exclusions.
- Closed items: percentages with 95 percent intervals; segment cuts only where each cell has about 30+ responses.
- Open text: code a sample of 50-100 responses into themes (affinity or tags), apply to all, count themes, and quote representative verbatims.
- Report: question, n, result, interval, caveats. Link findings to decisions.

## Verify
- [ ] Population, frame and sampling method are stated.
- [ ] Margin of error and response rate are reported.
- [ ] Exclusion rules and bias checks are documented.
