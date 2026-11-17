---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.rule-evaluation-latency-and-missed-iterations
name: rule-evaluation-latency-and-missed-iterations
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, rule-evaluation-latency, rule-group-timing, precompute-expensive-queries, recording-rule-performance, missed-iterations, recording-rules, alerting-rules, concurrent-rule-evaluation]
level: advanced
status: docs-checked
description: "Detect and fix slow Prometheus rule groups and missed evaluations: the missed-iteration and failure metrics, splitting groups, group interval, concurrent evaluation."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/recording_rules/", "https://prometheus.io/docs/prometheus/latest/feature_flags/", "https://github.com/prometheus/prometheus/blob/main/documentation/prometheus-mixin/alerts.libsonnet", "https://prometheus.io/docs/prometheus/latest/command-line/prometheus/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rule evaluation latency

Rules within a group run sequentially at a regular interval, with the same evaluation time. If a group has not finished before its next evaluation is due, that evaluation is skipped, and later ones keep being skipped until the first completes or times out. Recording rules then have a gap in their series, and alerting rules are evaluated less often.

## Metrics
The Prometheus mixin alerts use these two:
```promql
# Missed iterations: the mixin alert PrometheusMissingRuleEvaluations (for 15m)
increase(prometheus_rule_group_iterations_missed_total[5m]) > 0
# Per-rule failures: the mixin alert PrometheusRuleFailures (for 15m)
increase(prometheus_rule_evaluation_failures_total[5m]) > 0
```
The recording rules docs say `rule_group_iterations_missed_total` is incremented for each missed iteration of a rule group.

## Fixes
1. Precompute expensive expressions with recording rules: the docs say querying the precomputed result is often much faster, especially for dashboards that repeat the same expression on refresh.
2. Split the group: rule groups execute concurrently with each other by default, while rules within a group are sequential because a rule can use the output of a preceding one. Keep dependent rules in the same group, in order.
3. Set a longer group `interval` for slow, non-urgent rules (`interval` defaults to `global.evaluation_interval`).
4. Concurrent evaluation within a group: `--enable-feature=concurrent-rule-eval` evaluates rules without a detectable dependency on other rules in the group concurrently. This can improve evaluation latency at the cost of more concurrent query load. The number is bounded by `--rules.max-concurrent-evals` (default 4); the command-line reference says `--query.max-concurrency` (default 20) may need adjusting when it is set.
5. `query_offset` on a group (default `global.rule_query_offset`) offsets the evaluation timestamp into the past so the underlying metrics have been received and stored; it is for metric availability delays, not for slow evaluation.

## Gotchas
- `limit` on a group (default 0, no limit) caps the series a recording rule or alerts an alerting rule can produce. When exceeded, all series from the rule are discarded, an alerting rule's alerts are cleared, and the event is recorded as an evaluation error with no stale markers written. This shows up as evaluation failures, not latency.
- An alert is firing once it has been returned for the `for` duration (default 0s).
- `promtool check rules <file>` checks rule file syntax without a server; it exits 0 when valid and 1 on errors.

## Checked
Date: 2026-11-07.
Read in full: Defining recording rules (group fields, sequential evaluation, `limit`, `query_offset`, skipped evaluations and gaps), the Feature flags page (Concurrent evaluation section), and the Prometheus command-line page flag table. The mixin `alerts.libsonnet` page was read around the `PrometheusRuleFailures` and `PrometheusMissingRuleEvaluations` alerts and otherwise searched for rule metric names.
Removed because no cited page confirms them: `prometheus_rule_group_last_duration_seconds` and `prometheus_rule_group_interval_seconds` (and the 0.8 ratio alert), the `/rules` page and query-log `ruleGroup` field, the "2.52+" version claim, "rules share the engine", the `rate(x[1d])` advice, `for` stretching on missed iterations, and the invented Verify checklist.
Method: documentation only; no commands were run.
