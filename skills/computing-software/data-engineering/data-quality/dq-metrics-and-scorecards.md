---
id: computing-software.data-engineering.data-quality.dq-metrics-and-scorecards
name: dq-metrics-and-scorecards
category: computing-software
field: data-engineering
product: data-quality
tags: [data-quality, scorecard, dq-dimensions, data-quality-metrics, dq-score, trust-score, table-tiering, criticality, stakeholder-reporting, dqdi, dq-governance]
level: practitioner
status: draft
description: "Build a defensible data-quality scorecard (dimensions, weighting, trend) that drives prioritization instead of vanity metrics."   # quoted: YAML would cut an unquoted value at " #" or choke on ": "
sources:
  - https://dama.org/content/body-knowledge
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# A data-quality scorecard that actually drives prioritization

**Goal:** turn test pass/fail noise into a number leadership can act on, without it becoming a vanity metric nobody trusts or uses to decide anything.

## 1. Tier tables by criticality before scoring anything
A scorecard that averages quality across every table in the warehouse equally is useless — a flaky test on an unused staging table and a broken test on the revenue mart shouldn't move the same amount. Tier tables (e.g. Tier 1: exec dashboards/financial reporting, Tier 2: team-level operational tables, Tier 3: everything else) and report/weight the score per tier, or at minimum weight each table's contribution by a measured usage signal (query count, number of downstream dependents from lineage) rather than counting every table once. The single biggest cause of a scorecard nobody trusts is a Tier-3 table's failure tanking the headline number while a Tier-1 break barely registers.

## 2. Pick dimensions that map to the checks you can actually run
Standard DQ dimensions (accuracy, completeness, consistency, timeliness, validity, uniqueness — DAMA's framework is the common reference) are a useful checklist, but a scorecard dimension with no corresponding automated check is decoration. Map each dimension to the specific test types from computing-software.data-engineering.data-quality.data-tests-and-freshness-slas that measure it (timeliness → freshness tests; uniqueness → `unique`/grain tests; validity → `accepted_values`/range tests) before publishing a dimension score — a dimension you can't currently measure should say "not yet measured," not a fabricated or default-good number.

## 2b. Avoid the single-number trap
A single "DQ score: 94%" headline invites exactly one follow-up question leadership shouldn't need to ask: "94% of what, weighted how?" Report the composite number alongside its tier breakdown and trend, and make the weighting formula available/documented, not opaque — a score that can't be explained in one sentence to the person reading it will be ignored or (worse) gamed by whoever owns the inputs once they realize it drives a KPI.

## 3. Trend over absolute, outliers over averages
A quality score's absolute value is less useful than its **trend** (is Tier-1 quality improving or degrading month over month) and its **outliers** (which specific tables are dragging the score down this week) — leadership acts on "these 3 tables need fixing" far more readily than on "our score is 91.2%." Build the dashboard to surface the worst-N tables prominently, with the aggregate score as context, not the headline.

## 4. Gaming resistance
Any metric that affects a team's visible performance will eventually be gamed — a team can inflate its score by deleting flaky tests rather than fixing the underlying issue, or by narrowing a test's scope. Counter this by tracking **test count and coverage** alongside pass rate (a rising pass rate with a falling test count is a red flag, not an improvement) and by having DQ scoring reviewed by someone other than the table's own owning team, at least periodically.

## Verify
- [ ] Every scored dimension maps to at least one real, currently-running automated check — no dimension is a guess.
- [ ] Tier-1/critical tables are weighted or reported separately from the aggregate, not blended into one average.
- [ ] The scorecard's calculation (weights, formula) is written down somewhere the consuming stakeholders can see, not only in the dashboard tool's internal config.
- [ ] Test count/coverage is tracked alongside pass rate, and a falling test count with a rising score triggers a review.
