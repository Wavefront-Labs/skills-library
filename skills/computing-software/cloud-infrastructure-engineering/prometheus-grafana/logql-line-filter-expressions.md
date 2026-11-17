---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.logql-line-filter-expressions
name: logql-line-filter-expressions
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [line-filter-expressions, logql-line-filters, logql, query-performance, pattern-match-filter]
level: practitioner
status: verified
description: "Write fast LogQL line filters (|=, !=, |~, !~, pattern |> and or-chains), order them for performance and avoid regex where substring filters work."
sources: ["https://grafana.com/docs/loki/latest/query/log_queries/#line-filter-expression", "https://grafana.com/docs/loki/latest/query/bp-query/", "https://grafana.com/docs/loki/latest/query/log_queries/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LogQL line filter expressions

Line filters run on the raw line before parsing and are the cheapest way to cut data.

| Operator | Meaning |
|---|---|
| `\|= "text"` | contains |
| `!= "text"` | does not contain |
| `\|~ "regex"` | matches RE2 regex |
| `!~ "regex"` | does not match |
| `\|> "pattern"` / `!>` | matches a pattern expression (`<_>` wildcards); accepted by Loki 3.7.9 here, but not listed on that version's log-queries page |

```logql
{namespace="prod", app="api"} |= "error" != "healthcheck" |~ "(?i)timeout|deadline"
{app="api"} |= "payment" or "refund"                         # or-chain in one filter (ran on Loki 3.7.9)
{app="nginx"} |> "<_> - - <_> \"POST /api/<_>\" 5<_>"         # pattern filter
```

## Performance rules (query best practices)
1. Narrow the stream selector first (labels), then line filters, then parsers, then label filters.
2. Put the most selective filter first.
3. Prefer `|=` and `!=` over `|~` and `!~`; the Loki query best-practice page says the substring operators evaluate faster than regular expressions, so use regex as a last resort. Line-filter regexes are not anchored (unlike label matchers), and `.` matches newlines.
4. Case-insensitive: `|~ "(?i)error"` (a plain `|~ "TIMEOUT"` matched nothing on lower-case text) costs more; if logs have a consistent case, use exact text.
5. Line filters before `| json`: parsing every line then filtering by label is much slower than filtering text first.

## Gotchas
- Backticks avoid escaping: ``|~ `\d{3}ms` ``.
- `!=` on a missing string keeps everything; check negative filters against sample lines.
- Line filters see the raw line, not structured metadata or labels.

## Verify
- [ ] Query inspector shows reduced bytes processed after reordering filters.

## Checked
Ran Loki 3.7.9 and queried 60 JSON, 60 nginx-style and 60 logfmt lines: `|=`, `!=`, `|~` with `(?i)`, case-sensitivity, unanchored regex (`|~ "pay|refund"` matched inside lines), backtick strings, `|> ` and `!>` pattern filters, `|= "a" or "b"` chains, `ip()` filters, and line filter before `| json | status >= 500`. Docs read (Loki v3.7.9 source): query/bp-query.md (ordering, simple filters over regex, parsers after line filters) and query/log_queries (operator list, regex not anchored). The old best-practices URL in `sources` returned 404 in the docs tree, replaced by `bp-query`.
