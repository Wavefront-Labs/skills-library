---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.logcli-queries-tail-and-batch-export
name: logcli-queries-tail-and-batch-export
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [logcli, loki, logcli-query, tail, log-export, batch-download, loki-cli]
level: practitioner
status: docs-checked
description: "Use logcli to run LogQL, tail live logs, export large ranges in batches and inspect series and labels."
sources: ["https://grafana.com/docs/loki/latest/query/logcli/getting-started/", "https://grafana.com/docs/loki/latest/query/logcli/logcli-tutorial/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: terminal access to Loki for debugging and exports.

```
export LOKI_ADDR=https://loki.example.com
export LOKI_ORG_ID=team-a
export LOKI_BEARER_TOKEN_FILE=<path-to-token-file>

logcli labels
logcli series '{app="api"}'
logcli query '{app="api"} |= "error"' --since=1h --limit=200
logcli query '{app="api"}' --since=24h --batch=5000 --limit=100000 -o raw
logcli query 'sum by (level) (count_over_time({app="api"}[5m]))' --since=6h --step=5m
logcli query '{app="api"}' --tail --delay-for=2
logcli stats '{app="api"}' --since=1h
```
Settings: `--addr` or `LOKI_ADDR`; `--org-id` or `LOKI_ORG_ID` (sets `X-Scope-OrgID`); behind an authenticating proxy use `LOKI_USERNAME` and `LOKI_PASSWORD`, `LOKI_BEARER_TOKEN` or `LOKI_BEARER_TOKEN_FILE`.

`query` flags: `--limit` (default 30; `0` fetches all), `--since` (default 1h), `--from` and `--to`, `--step` (metric queries), `--batch` (default 1000, per request until the limit is reached), `--forward` (oldest first; without it batches download in reverse), `-o`/`--output` with `default`, `raw` or `jsonl`, `--quiet` to suppress query metadata on stderr. `--parallel-duration` (default 1h) and `--parallel-max-workers` (default 1) split a range into parallel jobs; output is then out of order, so add `--part-path-prefix` to write one file per job; with parallel workers `--limit` is ignored. `-f`/`--follow` is an alias of `--tail`.

Other commands: `instant-query`, `labels [<label>]`, `series <matcher>` (with `--analyze-labels`), `stats`, `volume`.

Gotchas
- Without `--limit` and `--batch` a large export stops at 30 entries.
- Server limits such as `max_entries_limit_per_query` (default 5000) and `max_query_length` still apply.
- Use `LOKI_ORG_ID` or `--org-id` for multi-tenant clusters.

## Verify
`logcli labels` returns label names; `logcli query '{app="api"}' --limit 1` returns one entry, proving address, tenant and auth.

## Checked
2026-11-03. Confirmed against the LogCLI getting-started reference (command and flag listing, defaults, environment variables) and the configuration reference for the server limits. Removed: the shell redirect to a file, the "websocket-friendly proxies" note, and the placeholder token path (now `<path-to-token-file>`).
Method: documentation only; no commands were run.
