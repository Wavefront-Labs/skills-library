---
id: computing-software.data-engineering.data-quality.dq-thresholds-and-acceptance-levels
name: dq-thresholds-and-acceptance-levels
category: computing-software
field: data-engineering
product: data-quality
tags: [data-quality, dq-thresholds, acceptance-criteria, sla, data-quality-rules]
level: advanced
status: draft
description: "Set data quality thresholds and acceptance levels per rule and dataset: fit-for-purpose targets, warn vs fail bands, statistical baselines and agreeing them with owners."
sources:
  - https://www.dama.org/cpages/body-of-knowledge
  - https://www.iso.org/standard/35736.html
  - https://docs.getdbt.com/reference/resource-configs/severity
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DQ thresholds and acceptance levels

**Goal:** each quality rule has an agreed "good enough" level, so failures mean something and perfect is not demanded where it does not matter.

## Fit for purpose
The same column can need 100% completeness for billing and 95% for marketing analytics. Thresholds belong to a **use**, agreed with the data owner and main consumers, recorded with the rule.

## Bands
| Band | Meaning | Action |
|---|---|---|
| Pass | at or above target (e.g. completeness >= 99.5%) | none |
| Warn | between target and tolerance (98-99.5%) | ticket, notify owner, data still published |
| Fail | below tolerance (< 98%) | block publish / circuit-break, page if critical |

## Setting the numbers
- Start from a **baseline**: measure the metric daily for 2-4 weeks. Set warn near the observed normal range (e.g. mean minus 3 sd, or p1), fail at the level where consumers are harmed.
- Hard rules (primary key uniqueness, referential integrity for financial facts) are 100%: zero tolerance.
- Ratio rules over small denominators fluctuate: require a minimum row count before evaluating.
- Re-baseline after source changes; review thresholds quarterly.

## Express in tools
```yaml
# dbt: absolute counts
data_tests:
  - not_null:
      config: {warn_if: ">50", error_if: ">500"}
```
```yaml
# Soda: ratios
checks for orders:
  - missing_percent(customer_id):
      warn: when > 0.5%
      fail: when > 2%
```
Great Expectations: `mostly=0.995` on expectations.

## Document
Rule, dimension, threshold bands, rationale, owner, consumers affected, date agreed. A catalog or contract file is the natural place.

## Gotchas
- Thresholds set by engineers alone tend to be either noisy or toothless.
- Over-tight thresholds get disabled; under-tight ones never fire. Review alert history.

## Verify
For each critical dataset, a threshold table exists with owner sign-off, and last month's warn/fail events match real issues.
