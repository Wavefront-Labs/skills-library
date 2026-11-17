---
id: computing-software.qa-testing-engineering.jmeter-k6.k6-influxdb-grafana-output
name: k6-influxdb-grafana-output
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [k6-influxdb, xk6-output-influxdb, grafana-dashboard-k6, time-series-results]
level: practitioner
status: gated
description: "Stream k6 metrics to InfluxDB (v1 built-in output or v2 via xk6-output-influxdb) and visualise in Grafana dashboards, with tag cardinality and push interval tuning."
sources:
  - https://grafana.com/docs/k6/latest/results-output/real-time/influxdb/
  - https://github.com/grafana/xk6-output-influxdb
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# InfluxDB output and Grafana dashboards

## InfluxDB 1.x (built in)
```bash
docker run -d -p 8086:8086 -e INFLUXDB_DB=k6 influxdb:1.8   # (gated: unconfirmed, source is paywalled or blocked; Docker is not available here)
k6 run --out influxdb=http://localhost:8086/k6 script.js
```
Run without Docker: the native InfluxDB 1.8.10 Windows binary with `CREATE DATABASE k6`, then `k6 run --out influxdb=http://127.0.0.1:18086/k6` on k6 2.3.0 (the built-in `influxdb` output still exists in v2). `SHOW MEASUREMENTS` listed `http_req_duration`, `http_reqs`, `iterations`, `vus` and 11 more; `SELECT count(value) FROM http_reqs` matched the run.
Env tuning (documented defaults): `K6_INFLUXDB_PUSH_INTERVAL` (default `1s`), `K6_INFLUXDB_CONCURRENT_WRITES` (default `4`; the example value 10 is a choice), `K6_INFLUXDB_TAGS_AS_FIELDS` (default `vu:int,iter:int,url`: those are already stored as non-indexed fields, so the variable is only needed to move other tags). Run: with defaults the `http_req_duration` tag keys were `expected_response, method, name, proto, scenario, status, testid` and its fields `url, value`.

## InfluxDB 2.x (extension)
```bash
xk6 build --with github.com/grafana/xk6-output-influxdb
K6_INFLUXDB_ORGANIZATION=perf K6_INFLUXDB_BUCKET=k6 K6_INFLUXDB_TOKEN=$TOKEN \
  ./k6 run -o xk6-influxdb=http://localhost:8086 script.js
```
The command and variable names match the extension README; running against an InfluxDB 2 server (gated: unconfirmed, source is paywalled or blocked; no InfluxDB 2 server was run here). Stock k6 2.3.0 rejects `-o xk6-influxdb` (`invalid output type`), so the custom build is required.

## Grafana
Add InfluxDB data source; import a community k6 dashboard ("k6 Load Testing Results", ID 2587 on grafana.com, InfluxDB data source; others: 4411, 10660, 14801) and adapt queries. Key panels: VUs, RPS, p95/p99 `http_req_duration` by `name`, `http_req_failed` rate, checks, iteration duration. Put server metrics (CPU, DB, GC) on the same time axis.

## Cardinality
Each unique tag combination is a series. Custom tags and `name`/`url` values containing ids explode series counts and slow Influx; `vu`, `iter` and `url` are already fields by default (see above). Use `name` tags for grouping, `--system-tags` to drop unneeded tags, and `TAGS_AS_FIELDS` for any other high-cardinality tag.

## Prometheus alternative
`--out experimental-prometheus-rw` (remote write) is the newer path, with native histograms; prefer it if you run Prometheus/Mimir already.

## Gotchas
- Influx write timeouts under heavy load drop metrics: watch k6 log lines "Couldn't write stats" (run: with nothing listening, k6 logged `level=error msg="Couldn't write stats" error="Post ...: connectex: ... actively refused"`); raise push interval or concurrency.
- Dashboard percentiles over aggregated points are approximate; the k6 summary is authoritative for the whole run.

## Verify
Grafana RPS and request counts match the k6 summary totals for the run window.
