---
id: computing-software.qa-testing-engineering.performance-testing.locust-headless-ci
name: locust-headless-ci
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [locust-headless, locust, ci-integration, csv-stats, performance-gates]
level: practitioner
status: verified
description: "Run Locust headless in CI: -u, -r and -t flags, --csv stats and HTML report, exit codes on failure ratio or percentiles, config files and stop timeouts."
sources:
  - https://docs.locust.io/en/stable/quickstart.html#direct-command-line-usage-headless
  - https://docs.locust.io/en/stable/configuration.html
  - https://docs.locust.io/en/stable/running-without-web-ui.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Headless runs and CSV stats in CI (Locust)

## Command
```bash
locust -f locustfile.py --headless \
  -u 300 -r 10 -t 20m \
  --host https://staging.example.test \
  --csv results/run --csv-full-history \
  --html results/report.html \
  --stop-timeout 30 \
  --only-summary
```
- `-u` users, `-r` spawn rate/s, `-t` run time; `--stop-timeout` lets tasks finish.
- CSV files: `run_stats.csv` (per endpoint aggregates: counts, failures, median/average/min/max, content size, RPS, and percentile columns 50%, 66%, 75%, 80%, 90%, 95%, 98%, 99%, 99.9%, 99.99%, 100%), `run_failures.csv` (Method, Name, Error, Occurrences, First Seen, Last Seen), `run_exceptions.csv`, `run_stats_history.csv` (time series with an `Aggregated` row per interval; `--csv-full-history` adds per-endpoint rows). Folders in the `--csv` prefix are created automatically; `--html` wrote a ~0.9 MB report in the run here.

## Config file
```ini
# locust.conf (or --config ci.conf; also pyproject.toml [tool.locust])
locustfile = locustfile.py
headless = true
users = 300
spawn-rate = 10
run-time = 20m
host = https://staging.example.test
csv = results/run
html = results/report.html
```
Env vars work too: `LOCUST_USERS=300`.

## Fail the build
```python
from locust import events

@events.quitting.add_listener
def _(environment, **kw):
    total = environment.stats.total
    if total.fail_ratio > 0.01:
        environment.process_exit_code = 1
    elif total.get_response_time_percentile(0.95) > 800:
        environment.process_exit_code = 1
    elif total.avg_response_time > 400:
        environment.process_exit_code = 1
```
Default exit code is 1 if any request failed (configurable via `--exit-code-on-error`; `--exit-code-on-error 0` gave exit code 0 on a run where every request failed). A `quitting` listener runs on the master or standalone process where `environment.stats.total` is complete.

## CI job (GitHub Actions)
```yaml
- run: pip install locust && locust --config ci.conf
- uses: actions/upload-artifact@v7
  if: always()
  with: { name: locust-results, path: results/ }
```

## Gotchas
- CI runners are small; heavy loads need dedicated generators or distributed workers; check runner CPU (Locust logs a warning above 90% CPU).
- Percentiles in Locust stats are bucketed approximations (rounded response times); fine for gates, not microsecond analysis.
- Running against shared staging during others' tests produces noise; schedule.

## Verify
The job fails when the failure ratio or p95 gate is exceeded, and CSV + HTML artifacts are kept for each run.

## Checked
Locust 2.47.0, Windows scratch venv, local HTTP server; GitHub API.
- Run: `locust --config ci.conf --csv-full-history --stop-timeout 5 --only-summary` with the conf keys from the skill (locustfile, headless, users, spawn-rate, run-time, host, csv in a subfolder, html): produced `report.html`, `run_stats.csv`, `run_stats_history.csv`, `run_failures.csv`, `run_exceptions.csv`; CSV headers read with Python; exit codes 0 (clean run), 1 (failures), 0 with `--exit-code-on-error 0`; the three-branch `quitting` gate pattern ran (gate set exit code 1 on a 300 ms endpoint with a 200 ms p95 limit); console table is headed "approximated" as the gotcha says; `--only-summary` in `--help`.
- Fetched: docs.locust.io configuration and running-without-web-ui pages (CSV flags, exit code section; the old retrieving-stats URL is a 404 and was dropped); GitHub tags API for actions/upload-artifact (latest v7.0.2, v7 major tag exists).
- The workflow YAML was checked part by part: both commands ran as shown above and the action version came from the tags API.
