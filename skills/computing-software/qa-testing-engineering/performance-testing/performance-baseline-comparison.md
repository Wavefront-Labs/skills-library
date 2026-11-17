---
id: computing-software.qa-testing-engineering.performance-testing.performance-baseline-comparison
name: performance-baseline-comparison
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [performance-baseline, regression-detection, performance-testing, ci-performance-gates, statistical-comparison]
level: practitioner
status: verified
description: "Detect performance regressions by comparing runs to a baseline: controlled conditions, repeated runs, relative thresholds, statistical tests, and storing results per build."
sources:
  - https://grafana.com/docs/k6/latest/results-output/end-of-test/custom-summary/
  - https://bencher.dev/docs/explanation/thresholds/
  - https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Baseline comparison and regression detection

**Goal:** spot when a change makes things slower, with confidence that the difference is real, not noise.

## Establish a baseline
- Same script, workload, data volume, environment size and configuration, test duration.
- Run 3-5 times to measure run-to-run variance; baseline = median of runs per transaction (p50, p95, p99, throughput, error rate, CPU per request).
- Store results with build id, commit, environment, date (JSON summaries from `handleSummary`, JMeter CSV, Locust CSV) in a results store (S3 + table, InfluxDB, Bencher).

## Compare
| Metric | Rule example |
|---|---|
| p95 per transaction | regression if > baseline x 1.10 and > run-to-run noise |
| throughput at fixed rate | must be achieved (no dropped iterations) |
| error rate | absolute limit |
| CPU/memory per request | > 15% increase flags efficiency regression |

## Statistics
- Compare distributions, not single numbers: Mann-Whitney U test (`scipy.stats.mannwhitneyu`) on raw latencies, or bootstrap confidence intervals of the p95 difference. Do not gate on the p-value alone: with ~600 requests per run, two runs of the same config gave p = 0.097 against each other and p = 0.006 against a third, yet their p95 was 23.5 vs 23.6 ms. Add an effect-size floor (the 10% rule above). A real +50 ms slowdown gave p = 3.6e-124 and a bootstrap 95% CI for the p95 difference of [49.5, 51.1] ms, while the unchanged run's CI was [-0.39, 0.38] ms.
- Microbenchmarks: repeated runs and change-point detection (Bencher offers percentage, z-score, t-test, IQR and static threshold tests; DataStax Hunter finds change-points in a series of results).

## CI integration
- Nightly or per-merge performance job on a dedicated, quiet environment; pin instance types.
- Script compares current summary to baseline file and fails with a table of deltas:
A working `compare.py` for Locust CSV prefixes (it takes the median p95 of several baseline runs and also requires the increase to exceed the run-to-run spread):
```python
import argparse, csv, json, statistics, sys
ap = argparse.ArgumentParser()
ap.add_argument("--baseline", nargs="+", required=True)   # one results prefix per baseline run
ap.add_argument("--current", required=True)
ap.add_argument("--max-p95-increase", type=float, default=0.10)
a = ap.parse_args()
def p95(prefix):
    with open(prefix + "_stats.csv", newline="") as f:
        return {r["Name"]: float(r["95%"]) for r in csv.DictReader(f) if r["Name"] != "Aggregated"}
base = [p95(p) for p in a.baseline]
cur = p95(a.current)
bad = 0
for name, c in cur.items():
    b = statistics.median(r[name] for r in base)
    noise = max(r[name] for r in base) - min(r[name] for r in base)
    flag = c > b * (1 + a.max_p95_increase) and c - b > noise
    bad += flag
    print(f"{name:12} baseline p95 {b:6.0f} ms  current {c:6.0f} ms  {'REGRESSION' if flag else 'ok'}")
sys.exit(1 if bad else 0)
```
```bash
python compare.py --baseline results/b1 results/b2 results/b3 --current results/run --max-p95-increase 0.10
```
The script exits 1 on a regression so the CI step fails. For k6 or JMeter, read the equivalent p95 from the `handleSummary` JSON or the JMeter CSV instead.
- Update the baseline deliberately (after accepted changes), with a commit noting why.

## Noise control
- Warm-up period excluded from analysis.
- No other load on shared dependencies; same time window if environment is shared.
- Same generator location and size.

## Gotchas
- Comparing against a single lucky run causes false alarms; use the median of multiple runs.
- Gradual creep: each change 3% slower passes a 10% gate; also compare against a long-term reference baseline.

## Verify
A deliberate slowdown (added 50 ms sleep in a handler) is flagged by the comparison, and an unchanged rerun is not (run here: 24 ms baseline p95 vs 73 ms flagged REGRESSION with exit 1; the unchanged rerun printed ok with exit 0).

## Checked
Locust 2.47.0, SciPy and NumPy in a Windows scratch venv, local HTTP server whose delay I changed.
- Run: three baseline runs, one unchanged rerun and one run with a 50 ms handler delay (5 users, 6 s each); `compare.py` above exited 0 for the unchanged run and 1 for the slowed run; `mannwhitneyu` on raw latencies (raw samples written by a request listener): same-config pair p = 0.097, unchanged vs baseline p = 0.006, slowed vs baseline p = 3.6e-124; one-sided `alternative='less'` p = 1.8e-124 and `'greater'` p = 1.0 for baseline vs slowed; bootstrap CI of the p95 difference (2000 resamples) as quoted.
- Fetched: Bencher thresholds page (test types), DataStax Hunter README (finds change-points), k6 custom-summary page (`handleSummary`), SciPy mannwhitneyu page (URL live).
