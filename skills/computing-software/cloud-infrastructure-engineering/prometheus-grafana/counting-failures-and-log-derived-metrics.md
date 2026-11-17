---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.counting-failures-and-log-derived-metrics
name: counting-failures-and-log-derived-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [failure-counting, error-instrumentation, instrumentation, prometheus-best-practices, error-rate-measurement]
level: practitioner
status: docs-checked
description: "Count failures properly: paired total and failure counters, reason labels, initialising series, and turning important log lines into counters instead of LogQL alerts."
sources: ["https://prometheus.io/docs/practices/instrumentation/", "https://prometheus.io/docs/practices/naming/", "https://grafana.com/docs/loki/latest/alert/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Counting failures and log-derived metrics

## Paired counters
The Prometheus instrumentation page: every time there is a failure, increment a counter; and when reporting failures, "you should generally have some other metric representing the total number of attempts. This makes the failure ratio easy to calculate." Failures may also bubble up to a more general error counter depending on how the code is structured.
```promql
sum(rate(db_queries_failed_total[5m])) / sum(rate(db_queries_total[5m]))
```
For online-serving systems, the page suggests counting queries when they end, so the count lines up with the error and latency stats (be consistent either way).

## Reason labels
Use labels, not procedurally generated metric names (the page's example: one `http_responses_total` with a `code` label rather than `http_responses_500_total`). Keep label cardinality low: the page suggests below 10 for most metrics, and investigating alternatives if it could exceed 100. The naming page adds not to use labels for unbounded values such as user IDs or email addresses, so an arbitrary exception message would be a bad label value; a small fixed set of reasons is fine.

## Export zero, do not leave series missing
Series that only appear when something happens are hard to handle, so export a default such as 0 for any series you know may exist. Most client libraries (Go, Java, Python) automatically export 0 for metrics with no labels; for metrics with labels you have to create the label combinations yourself (see your client library docs for how).

## Logging-derived metrics
- Prometheus advice: for every line of logging code, also have a counter that is incremented, so you can see how often an interesting message has been happening and for how long. Closely related messages in one function (branches of an if/switch) can share one counter. It is also useful to export total info/error/warning lines logged by the application and compare them as part of releases.
- If you cannot change the code, Loki's ruler can evaluate Prometheus-compatible recording rules written in LogQL and remote-write the result as a metric, for example the page's `sum(rate({container="nginx"}[1m]))` recorded as `nginx:requests:rate1m`. Compatible remote-write backends listed: Prometheus (>= v2.25.0), Grafana Mimir and Thanos Receiver. Configure under `ruler.remote_write` (`enabled: true`, `clients: <name>: url: ...`).
- The Loki page positions log-based rules for black-box monitoring of components you cannot instrument, for event alerting (for example `count_over_time({namespace="prod"} |~ "..." [5m]) > 0`), and for alerting on high-cardinality sources, since values extracted at query time avoid a cardinality explosion in the metrics store.

## Alerting on a ratio
The Loki alerting page's example alerts on an error ratio with a threshold and a `for` duration:
```yaml
- alert: HighPercentageError
  expr: sum(rate({app="foo", env="production"} |= "error" [5m])) by (job) / sum(rate({app="foo", env="production"}[5m])) by (job) > 0.05
  for: 10m
  labels:
    severity: page
```

## Verify
- [ ] Every failure counter has a matching total-attempts metric, so a ratio query returns a value.
- [ ] Known label combinations of the failure counter exist at 0 right after a restart.

## Checked
Date: 2026-11-07. Read in full: the Prometheus instrumentation practices page (logging, failures, labels, "avoid missing metrics" sections), the Prometheus metric and label naming page (labels section, cardinality caution) and the Loki alerting and recording rules page (use cases, alerting rule and recording rule examples, remote-write section; the ruler sharding and storage sections were skimmed only). Trims: removed the `result="success|error"` single-counter alternative, the Python label-initialisation and Java `catch` snippets (not on these pages), "`> 0` alerts never fire after a restart", Alloy `loki.process` `stage.metrics`, the OTel `count` connector, "native counters are cheaper and survive log sampling", the "rate(...) > 0 pages on a single error" advice and `increase(...) > N` for rare events.
Method: documentation only; no commands were run.
