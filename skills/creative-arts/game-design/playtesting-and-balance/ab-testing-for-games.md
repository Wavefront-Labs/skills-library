---
id: creative-arts.game-design.playtesting-and-balance.ab-testing-for-games
name: ab-testing-for-games
category: creative-arts
field: game-design
product: playtesting-and-balance
tags: [game-design, playtesting-and-balance, ab-testing, split-test, experiment, live-ops, statistics, sample-size]
level: practitioner
status: draft
description: "Run a clean A/B test on a live or beta game: one hypothesis, random assignment, a metric fixed in advance, a sample size set before launch, and no peeking."
sources:
  - https://www.gdcvault.com
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# A/B testing for games

**Goal:** learn whether a change causes a measurable difference, instead of guessing from before/after numbers.

## Procedure
1. **State a falsifiable hypothesis** with one primary metric ("showing the tutorial skip button raises tutorial completion") and guardrail metrics that must not get worse (retention, crash rate, revenue).
2. **Assign at random per player**, not per session or per day, and keep each player in their group for the whole test. Log the assigned variant on every event.
3. **Fix sample size and duration before starting** using a power calculation: you need the baseline rate, the smallest difference worth detecting, a significance level and a power target. Run at least whole weeks so weekday effects balance.
4. **Check the split** (sample ratio mismatch): if a 50/50 assignment lands at 52/48 on large numbers, something is wrong with assignment or logging; do not trust the result.
5. **Do not peek and stop early** on a good-looking day; repeated looks inflate false positives unless you use a sequential method designed for it.
6. **Analyse the pre-registered metric** with an appropriate test (two-proportion test for rates; for skewed money or playtime, use methods robust to outliers) and report the confidence interval, not only the p-value.
7. **Decide and document:** ship, drop, or iterate; keep the test record.

## Gotchas
- Small studios often lack traffic; use larger effects, longer runs, or qualitative tests instead.
- Many metrics give false winners; name one primary metric.
- Novelty effects fade; check whether the lift survives the second week.
- In multiplayer, variants can interact (matchmaking across groups); isolate or randomise by cluster.

## Verify
- [ ] Hypothesis, metric, sample size and end date written before launch.
- [ ] Split ratio checked and guardrails reviewed.
- [ ] Decision recorded with interval and caveats.
