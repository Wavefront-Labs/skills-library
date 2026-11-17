---
id: creative-arts.design-for-form-and-experience.mood-boarding.measuring-attributes-with-semantic-differential-scales
name: measuring-attributes-with-semantic-differential-scales
category: creative-arts
field: design-for-form-and-experience
product: mood-boarding
tags: [semantic-differential, kansei-engineering, attribute-scales, brand-perception, product-semantics, osgood, perception-testing]
level: practitioner
status: draft
description: "Measure design perception with semantic differential scales: pick bipolar adjective pairs, rate concepts on 5-7 point scales, and analyse profiles to compare against targets."
sources:
  - "Osgood, Suci and Tannenbaum, The Measurement of Meaning (University of Illinois Press, 1957)"
  - "Nagamachi, Kansei Engineering (1995) and Kansei/affective design research"
  - "Hassenzahl, Burmester and Koller, AttrakDiff - questionnaire for pragmatic and hedonic quality (attrakdiff.de)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Semantic differential scales

**Goal:** turn "feels premium" or "friendly" into measurable profiles that compare concepts against a target.

## Build the scale
1. **Derive adjective pairs** from the brand attributes and mood board keywords (`creative-arts.design-for-form-and-experience.mood-boarding.building-a-mood-board-and-style-tiles`). Typical set of 8-15 bipolar pairs: modern-traditional, warm-cool, light-heavy, simple-complex, friendly-formal, precious-ordinary, playful-serious, rugged-delicate.
2. Use true **opposites** (not "friendly" versus "not friendly"); mix pair directions (do not put all positive words on the left).
3. **7-point scale** between the poles (3 = strongly left, 0 or 4 = neutral, up to opposite pole), with only the ends labelled.
4. Add a few evaluative pairs (good-bad, attractive-unattractive) to correlate perception with liking.

## Run
- Show 3-6 concepts (renders, sketches, material samples, packaging mock-ups) in randomised order, consistent presentation (same background, scale, lighting).
- 20-30 respondents of the target group per concept (more if you compare segments); within-subject design is efficient.
- Instruction: "Rate how well each pair describes this design", quick, first impression.
- Online (Qualtrics, Typeform) or in-person with paper sheets.

## Analyse
- Compute **mean profile per concept** and plot a line chart across pairs (the "semantic profile"); overlay the **target profile** from the brief.
- Compare with confidence intervals; look at distance from target per pair; run factor analysis (evaluation, potency, activity) for many scales.
- Use gaps to guide revisions (more "warm", less "heavy"), then re-test the revised concept.

## Gotchas
- Cultural and language differences change adjective meaning; pilot and translate carefully.
- Perception differs by group; do not average across incompatible segments.
- For product or app experiences, AttrakDiff (28 pairs) is a validated option.

## Verify
- [ ] Adjective pairs derive from brand attributes; target profile set before testing.
- [ ] Concepts rated in randomised order with adequate n.
- [ ] Results drive specific revisions and a re-test.
