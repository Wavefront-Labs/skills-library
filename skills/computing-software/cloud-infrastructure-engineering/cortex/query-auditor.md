---
id: computing-software.cloud-infrastructure-engineering.cortex.query-auditor
name: query-auditor
category: computing-software
field: cloud-infrastructure-engineering
product: cortex
tags: [query-audit, correctness, migration, comparison, tooling]
level: advanced
status: docs-checked
description: "Use the query-audit tool to measure result differences between two Prometheus-API backends during migrations or read-path changes."
sources:
  - https://github.com/cortexproject/cortex/blob/master/docs/operations/query-auditor.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The query auditor ships in the Cortex repository but not in the Docker images, so build it from source. It is mainly for Cortex developers but helps operators during events such as backend migrations.

It runs a set of queries against two backends exposing the Prometheus read API, usually the query-frontend of two Cortex deployments, and compares: label sets must match; each label set must have the same number of samples as its pair; each sample's difference is computed against its pair; then the average difference per query is reported.

Limitation: only queries with `Matrix` response types are supported.

Config has a `control` and a `test` backend, each with `host` and `headers` such as `X-Scope-OrgID`, then a `queries` list with `query`, `start`, `end` and `step_size`:

```yaml
control:
  host: http://localhost:8080/prometheus
  headers:
    "X-Scope-OrgID": 1234
test:
  host: http://localhost:8081/prometheus
queries:
  - query: 'sum(rate(container_cpu_usage_seconds_total[5m]))'
    start: 2019-11-25T00:00:00Z
    end: 2019-11-28T00:00:00Z
    step_size: 15m
```

Use cases are correctness testing while changing the read path and comparing results from different backends. Run it from the repository checkout with `go run ./tools/query-audit/ -f config.yaml`; ideal output reports `0.000000% avg diff` for each query along with series and sample counts.

## Checked

Method: docs-checked 2026-11-09 against the Cortex query auditor page (raw markdown, read in full).
