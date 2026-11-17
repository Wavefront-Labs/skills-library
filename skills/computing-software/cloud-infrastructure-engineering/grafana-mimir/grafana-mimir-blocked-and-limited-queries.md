---
id: computing-software.cloud-infrastructure-engineering.grafana-mimir.grafana-mimir-blocked-and-limited-queries
name: grafana-mimir-blocked-and-limited-queries
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-mimir
tags: [blocked-queries, limited-queries, query-protection, per-tenant, promql]
level: advanced
status: docs-checked
description: "Explains per-tenant blocked_queries rules in Mimir: pattern, regex, optional filters, query formatting, remote read and troubleshooting."
sources: ["https://grafana.com/docs/mimir/latest/configure/configure-blocked-queries/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Blocked and limited queries

Per-tenant `blocked_queries` overrides reject queries that match a rule. The order of rules is preserved, so the first matching rule is used.

## Block rule fields

- `pattern` (required): a full PromQL query or a regular expression. A rule without a pattern is a configuration error.
- `regex`: set `true` to treat the pattern as a regular expression; an invalid regex is a configuration error. Match everything with `pattern: ".*"` and `regex: true`.
- Optional filters narrow which matching queries are blocked, and all configured filters must be satisfied: `time_range_longer_than` (time range end - start; not applied to instant queries), `step_size_shorter_than` (not applied to instant queries or queries without a step), and `unaligned_range_queries: true` (range queries whose time range is not a multiple of the step; not applied to instant queries, aligned range queries or remote read).
- `reason`: appears in the blocked-query log line.

```yaml
overrides:
  "tenant-id":
    blocked_queries:
      - pattern: 'sum(rate(node_cpu_seconds_total{env="prod"}[1m]))'
      - pattern: ".*"
        regex: true
        time_range_longer_than: 7d
        reason: "queries longer than 7 days are not allowed"
```

Blocking applies to instant queries, range queries and remote read. For a remote read request each set of matchers is evaluated as a vector selector; if any set is blocked the whole request is rejected. To target those, use a regex pattern with the braces escaped, such as `'\{.*foo.*\}'`.

## Regex patterns and query formatting

Mimir parses queries into PromQL expressions before blocking. Without `regex`, the pattern is parsed and compared to the formatted query. With `regex: true`, the pattern is used as-is against the formatted query, so check it against the output of `mimirtool promql format <query>` (the formatter may reorder operators, remove empty selector braces and strip newlines, extra whitespace and comments).

## Viewing and troubleshooting

- Blocked queries are logged at info level with `msg="query blocked"`, including query text, duration, step, rule index and reason.
- The metric `cortex_query_frontend_rejected_queries_total` counts them per tenant (`user` label) with `reason="blocked"`; the same metric uses `reason="limited"` for rate-limited queries.
- An invalid rule at startup makes Mimir log `msg="module failed"` (`module=runtime-config`) and exit; an invalid rule introduced at runtime logs `msg="failed to load config"` and Mimir keeps the previous valid configuration. The `err` field names the tenant and rule index.

## Checked

2026-11-04. Confirmed against the Mimir page "Configure queries to block": rule fields, the three filters and their exclusions, first-match order, remote read behaviour, formatting, log messages and metric. Removed: `limited_queries`, `expires_at`, `id`, `created_by`, `created_at`, `note` and the claim that `reason` is returned in the HTTP response (none appear on the page).
Method: documentation only; no commands were run.
