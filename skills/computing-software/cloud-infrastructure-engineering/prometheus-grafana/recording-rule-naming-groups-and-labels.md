---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.recording-rule-naming-groups-and-labels
name: recording-rule-naming-groups-and-labels
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, recording-rules, recording-rule-naming, level-metric-operation, rule-groups, rule-group-interval, group-ordering, rule-labels, recording-rule-labels]
level: practitioner
status: docs-checked
description: "Structure recording rules: level:metric:operations names, group interval/limit/query_offset, ordering of dependent rules, and when to add static labels to recorded series."
sources: ["https://prometheus.io/docs/practices/rules/", "https://prometheus.io/docs/prometheus/latest/configuration/recording_rules/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Recording rule naming, groups and labels

## Naming: `level:metric:operations`
- **level**: the aggregation level and labels of the rule output (`job`, `instance`, `cluster`, `instance_path`).
- **metric**: the source metric name, unchanged except for stripping `_total` off counters when taking `rate()`/`irate()`.
- **operations**: the operations applied, newest first (`rate5m`, `sum`, `ratio_rate5m`).
- A ratio by division separates the metrics with `_per_` and uses the operation `ratio`
  (`instance_path:request_failures_per_requests:ratio_rate5m`).
- Aggregate numerator and denominator separately, then divide; never average a ratio or an average.
- Always use a `without` clause listing the labels you aggregate away, so `job` and the rest survive. The labels
  removed in `without` must also disappear from the level in the output name.
```yaml
- record: instance_path:requests:rate5m                # rate(requests_total{job="myjob"}[5m])
- record: path:requests:rate5m                         # sum without (instance)(instance_path:requests:rate5m{job="myjob"})
- record: job:request_failures_per_requests:ratio_rate5m
```
Recording rule names must be valid metric names.

## Groups
```yaml
groups:
  - name: http.rules
    interval: 30s           # default = global evaluation_interval
    limit: 10000            # cap on series a recording rule may produce; 0 = no limit
    query_offset: 30s       # evaluate in the past to tolerate ingestion delay; default global.rule_query_offset
    rules:
      - record: instance_path:requests:rate5m
        expr: rate(requests_total{job="myjob"}[5m])
      - record: path:requests:rate5m                     # uses the rule above: same group, AFTER it
        expr: sum without (instance)(instance_path:requests:rate5m{job="myjob"})
```
- Rules within a group run sequentially, with the same evaluation time.
- If a group exceeds its `limit`, all series from that rule are discarded and the evaluation is recorded as an error.
- If a group is still evaluating when its next evaluation is due, that evaluation is skipped, leaving a gap, and
  `rule_group_iterations_missed_total` increases.
- `query_offset` matters most when Prometheus is a remote-write target, where data can arrive late.
- Check files with `promtool check rules FILE`; reload with SIGHUP.

## Labels on recorded series
```yaml
      - record: job:http_requests:rate5m
        expr: sum by (job) (rate(http_requests_total[5m]))
        labels:
          slo: checkout-availability     # static label to select in dashboards/alerts
```
- Rule `labels` add or overwrite labels before the result is stored; a label defined on the rule overrides the key
  from the group or expression.

## Verify
- [ ] Every rule name follows `level:metric:operations` (lint in CI).
- [ ] Dependent rules live in the same group after their inputs.

## Checked
2026-10-31. Confirmed against the Prometheus "Recording rules" naming practice page (level:metric:operations, `_total`
stripping, newest-first operations, `_per_` and `ratio`, aggregate numerator and denominator separately, `without`
clause) and "Defining recording rules" (group fields `interval`, `limit`, `query_offset` and their defaults, sequential
evaluation, limit behaviour, skipped evaluations and `rule_group_iterations_missed_total`, `promtool check rules`,
SIGHUP reload, label override). Removed unconfirmed claims: version gate for `query_offset`, cross-group ordering and
concurrency, interval-multiple guidance, external-label behaviour, advice on templated labels, and the claim that colons
are banned in instrumented names.
Method: documentation only; no commands were run.
