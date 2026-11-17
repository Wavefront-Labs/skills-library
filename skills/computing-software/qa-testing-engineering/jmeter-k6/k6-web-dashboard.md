---
id: computing-software.qa-testing-engineering.jmeter-k6.k6-web-dashboard
name: k6-web-dashboard
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [k6-web-dashboard, k6-html-report, live-dashboard, k6-dashboard-export]
level: practitioner
status: verified
description: "Watch k6 runs live with the built-in web dashboard (K6_WEB_DASHBOARD) and export a standalone HTML report for sharing results, with port, period and CI settings."
sources:
  - https://grafana.com/docs/k6/latest/results-output/web-dashboard/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# k6 web dashboard and HTML report export

Built into k6 (0.49+); no extension needed.

```bash
K6_WEB_DASHBOARD=true k6 run script.js                         # open http://127.0.0.1:5665
K6_WEB_DASHBOARD=true K6_WEB_DASHBOARD_EXPORT=report.html k6 run script.js
```
Options (env):
| Variable | Default | Meaning |
|---|---|---|
| `K6_WEB_DASHBOARD_HOST` | docs say `localhost`; source default is empty | bind address. Run on Windows with k6 2.3.0: unset host listened on `0.0.0.0` and `[::]` (all interfaces), `K6_WEB_DASHBOARD_HOST=127.0.0.1` listened on `127.0.0.1` only. Set it explicitly on shared machines |
| `K6_WEB_DASHBOARD_PORT` | 5665 | port (`-1` disables the server but still allows export: run, no listener on 5665 and `report.html` was written) |
| `K6_WEB_DASHBOARD_PERIOD` | 10s | aggregation period of charts; the HTML export needs more than one period of data |
| `K6_WEB_DASHBOARD_OPEN` | false | open browser automatically |
| `K6_WEB_DASHBOARD_EXPORT` | - | write HTML report at the end |

## What it shows
Overview (VUs, request rate, failed rate, p95/p99 duration), timings breakdown (blocked, connecting, TLS, sending, waiting, receiving), per-scenario panels, and browser Web Vitals for k6 browser tests. The exported HTML is self-contained (one file, 166 kB in a run, no external script or stylesheet URLs) for attaching to tickets or CI artifacts. The k6 docs add that the report only has graphs when the test lasts more than three times the period.

## CI pattern
```yaml
- run: K6_WEB_DASHBOARD=true K6_WEB_DASHBOARD_PORT=-1 K6_WEB_DASHBOARD_EXPORT=k6-report.html k6 run test.js
- uses: actions/upload-artifact@v4
  if: always()
  with: { name: k6-report, path: k6-report.html }
```
The workflow passes `actionlint` 1.7.12 (k6 must be on the runner first, e.g. via the `grafana/setup-k6-action` repo, which exists). `actions/upload-artifact` is at v7.0.2 (Oct 2026), so `@v4` works but is old; use a current major or pin a SHA.

## Gotchas
- A short test writes no report: an 8 s run with the default 10 s period logged `The test run was short, report generation was skipped (not enough data)` and created no file (run; source skips export when at most one snapshot exists). For smoke runs set `K6_WEB_DASHBOARD_PERIOD=1s`, which produced the report. Use tests longer than three periods for useful graphs.
- In CI disable the server with port `-1` (no port bound, export still works).
- Period-aggregated charts smooth spikes; check the raw outputs for short incidents.
- In Docker, publish the port and bind host `0.0.0.0`.

## Verify
`report.html` exists (check the file, because a too-short run silently skips it), opens offline and its totals match the end-of-test summary.
