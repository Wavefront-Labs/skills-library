---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheus-query-log-and-active-queries
name: prometheus-query-log-and-active-queries
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, query-log, query-log-analysis, active-query-tracker, slow-queries, jq, grafana-dashboards]
level: practitioner
status: gated
description: "Turn on the Prometheus query log, find the slowest and most expensive queries with jq, and use queries.active to identify the query that crashed the server."
sources: ["https://prometheus.io/docs/guides/query-log/", "https://prometheus.io/docs/prometheus/latest/command-line/prometheus/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Query log and active query tracker

## 1. Enable the query log
```yaml
global:
  query_log_file: /prometheus/query.log      # reloading the configuration reopens the file
```
A relative path was created in the process working directory, not the data dir (run: `query_log_file: ql.log` appeared next to prometheus.yml, with `--storage.tsdb.path=data`). Each line is JSON (3.15.1): `params.query`, `params.start/end/step` (step in seconds, 0 for an instant query), `stats.timings.evalTotalTime`, `stats.timings.execQueueTime`, `stats.samples.totalQueryableSamples` (also `samplesRead`, `peakSamples`; seen with `promql-per-step-stats` enabled, not tested without it), `httpRequest.clientIP` (plus `method`, `path`) for API queries, and `ruleGroup` (`file`, `name`) for rule evaluations.
Prometheus does not rotate the file; the docs say a config reload reopens it, so rotate with logrotate and reload (not rotation-by-copy), or toggle the setting on only while investigating (gated: unconfirmed, source is paywalled or blocked: rotation itself was not run).

## 2. Analyse
```bash
# (jq was not available here; these Python equivalents were run against a real query log)
python3 - <<'EOF'
import json, collections
rows = [json.loads(l) for l in open('query.log')]
# 20 slowest queries
print(*sorted(((r['stats']['timings']['evalTotalTime'], r['params']['query']) for r in rows), reverse=True)[:20], sep='\n')
# Most samples touched
print(*sorted(((r['stats']['samples'].get('totalQueryableSamples', 0), r['params']['query']) for r in rows), reverse=True)[:10], sep='\n')
# Which client sends the most queries (rule evaluations have no httpRequest)
print(collections.Counter(r.get('httpRequest', {}).get('clientIP', 'rule') for r in rows).most_common())
# Queries queued (concurrency saturation)
print([r['params']['query'] for r in rows if r['stats']['timings']['execQueueTime'] > 1])
EOF
```
In the test log a 1-day 1 ms subquery took 0.97 s and touched 17,548 samples, ahead of 2-hour (0.085 s, 34,742 samples) and trivial queries, and rule evaluations showed as `rule` (9) versus `127.0.0.1` (3).
Typical offenders: dashboards with 30-day ranges and 15 s step, `rate(x[1d])` over high-cardinality metrics,
regex matchers on `__name__`, unbounded `topk` over everything.

## 3. Active query tracker (post-crash forensics)
Prometheus writes in-flight queries to `<data-dir>/queries.active`, a memory-mapped file of 1 + max-concurrency x 1000 bytes (run: 20,001 bytes at the default concurrency 20; source `promql/query_logger.go`). After a crash the next start logs, at INFO level, `These queries didn't finish in prometheus' last run:` followed by the unfinished queries (message text confirmed in the 3.15.1 source; a crash with an in-flight query was not reproduced here because the test queries finished in under a second).
That's the query that blew memory; find its dashboard via clientIP/Grafana query inspector.

## Fixes
- Add a recording rule and point the panel at it.
- Raise the panel's min interval / max data points; shorten default dashboard ranges.
- Cap damage with `--query.max-samples` and `--query.timeout` (see query-limits skill).

## Verify
- [ ] query.log is written and is rotated (reload reopens it).
- [ ] Top-10 slow queries each have an owner and a fix or rule.
- [ ] `prometheus_engine_query_duration_seconds{quantile="0.9"}` drops after fixes.

## Checked
Prometheus 3.15.1 (windows-amd64) run locally with `global.query_log_file`, rule evaluations at 5 s and API queries: log line fields read from the JSON, relative-path location, the four analyses re-written in Python and run (jq absent), `queries.active` size (20,001 bytes). Sources: configuration.md at tag v3.15.1 (reload reopens the file); `promql/query_logger.go` and `cmd/prometheus/main.go` at v3.15.1 (entry size, message text). Not run: jq, log rotation, crash recovery message.
