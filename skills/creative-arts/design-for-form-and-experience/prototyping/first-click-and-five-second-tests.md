---
id: creative-arts.design-for-form-and-experience.prototyping.first-click-and-five-second-tests
name: first-click-and-five-second-tests
category: creative-arts
field: design-for-form-and-experience
product: prototyping
tags: [first-click-testing, five-second-test, first-impression-test, click-test, unmoderated-testing, navigation-testing, maze]
level: practitioner
status: draft
description: "Run first-click tests (does the first click lead to success) and five-second tests (what do people remember), with setup, question design, sample size and analysis."
sources:
  - "Bailey, Wolfson, Nall and Koyani, Performance-Based Usability Testing: Metrics That Have the Greatest Impact for Improving a System's Usability (HCII 2009)"
  - "Nielsen Norman Group - First Click and Five-Second Tests (nngroup.com/articles/first-click-testing)"
  - "Lyssna / UsabilityHub - Five Second Test and Click Test guides (lyssna.com/guides)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# First-click and five-second tests

## First-click test
**Finding (Bailey, Wolfson et al.):** users whose first click is correct complete the task about 87 percent of the time versus 46 percent when wrong.
1. **Choose a screenshot or prototype** (static is enough) and **write 3-6 task prompts** as goals, not UI labels: "You want to check an order you placed last week. Where would you click first?"
2. **Define correct areas** (one or several) in the tool (Optimal Workshop Chalkmark, Maze, Lyssna, UserTesting).
3. **Collect** click location, time to click, confidence rating, and an optional "why".
4. **Sample:** 30-50 per task for stable percentages; intervals around the success rate.
5. **Analyse** success percentage, click heatmaps, time; look at where wrong clicks cluster (label confusion), and fix navigation or labelling; retest.
6. Randomise task order; pretest wording; do not hint terms present on the page.

## Five-second test
**Purpose:** measure what a page communicates before people read: purpose, brand, hierarchy, key message.
1. Show a design for **5 seconds** (UsabilityHub/Lyssna, Maze, or in person), then hide it.
2. Ask 2-4 **recall questions:** "What is this page for?", "What do you remember?", "Who is it for?", optionally "What was the main action?" and a sentiment rating.
3. **Sample:** 20-50 responses; code answers into categories (correct purpose vs wrong, mentioned element) and report percentages with example quotes.
4. Test **one design per participant** (between subjects) to avoid carryover; variations compared with proportions tests.

## Gotchas
- Five-second tests evaluate impression, not usability; first-click tests do not test full flows.
- Use real users or a screened panel matching your audience; remote panels vary in quality (add attention checks).
- Static images cannot capture hover and scrolling; call out limits.

## Verify
- [ ] Tasks are goal-based, with predefined correct click areas.
- [ ] Sufficient responses per test; both result and rationale analysed.
- [ ] Fixes retested with the same design variant measure.
