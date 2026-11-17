---
id: computing-software.qa-testing-engineering.jmeter-k6.k6-json-and-csv-outputs
name: k6-json-and-csv-outputs
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [k6-json-output, k6-csv-output, k6-results-output, raw-metrics, jq-analysis]
level: practitioner
status: verified
description: "Write raw k6 metrics to JSON or CSV outputs (--out json/csv), control size with gzip and system tag filters, and analyse points with jq or pandas."
sources:
  - https://grafana.com/docs/k6/latest/results-output/real-time/json/
  - https://grafana.com/docs/k6/latest/results-output/real-time/csv/
  - https://grafana.com/docs/k6/latest/using-k6/k6-options/reference/#system-tags
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JSON and CSV result outputs

## Run
```bash
k6 run --out json=results.json.gz script.js     # .gz suffix compresses
k6 run --out csv=results.csv script.js
k6 run --out json=raw.json --out csv=raw.csv script.js   # multiple outputs
```
CSV options (documented defaults): `K6_CSV_TIME_FORMAT` (`unix` default; `rfc3339`, `rfc3339_nano`, `unix_nano`, `unix_micro`, `unix_milli`), `K6_CSV_SAVE_INTERVAL` (`1s`), `K6_CSV_FILENAME`. Both files above were written and parsed (gzip NDJSON read back with Python; the `.gz` suffix compresses).

## JSON shape (NDJSON)
```json
{"type":"Metric","data":{"name":"http_req_duration","type":"trend",...},"metric":"http_req_duration"}
{"type":"Point","data":{"time":"2024-...","value":187.4,"tags":{"name":"GET /orders","status":"200","scenario":"api"}},"metric":"http_req_duration"}
```

## Analysis
```bash
# extract name/value pairs per endpoint (feed to sort/awk or pandas for percentiles)
zcat results.json.gz | jq -r 'select(.type=="Point" and .metric=="http_req_duration") | [.data.tags.name, .data.value] | @tsv' > d.tsv
```
```python
import pandas as pd
df = pd.read_csv("results.csv")
d = df[df.metric_name == "http_req_duration"]
print(d.groupby("name")["metric_value"].quantile([0.5, 0.95, 0.99]).unstack())
```

## Keeping files manageable
Every HTTP request emits 9 metric points (`http_reqs`, `http_req_duration`, `_blocked`, `_connecting`, `_tls_handshaking`, `_sending`, `_waiting`, `_receiving`, `http_req_failed`; counted in a run on k6 2.3.0), plus per-iteration and VU metrics. A 1M-request test makes a multi-GB JSON. Reduce:
- `--system-tags=status,method,name,scenario,expected_response` (fewer tags per point)
- `discardResponseBodies` doesn't reduce points; aggregate in a time-series DB for long tests instead (Prometheus/InfluxDB).
- `--summary-export` / `handleSummary` for aggregates only.

## Gotchas
- Raw points include setup/teardown requests. In a run, the setup request had `group: ::setup` and no `scenario` tag (VU-code requests had `scenario: api`), so filter on the `group` tag (`::setup`, `::teardown`) or the absence of `scenario`.
- CSV columns: `metric_name,timestamp,metric_value,check,error,error_code,expected_response,group,method,name,proto,scenario,service,status,subproto,tls_version,url,extra_tags,metadata`.

## Verify
Quantiles computed from raw points match the end-of-test summary within rounding (run: 201 points, k6 `med=50.75ms p(95)=90.71ms p(99)=91.26ms` vs pandas `quantile` 50.758 / 90.717 / 91.266 ms).
