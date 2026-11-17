---
id: computing-software.qa-testing-engineering.performance-testing.throughput-latency-knee-point
name: throughput-latency-knee-point
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [knee-point, throughput-curve, saturation-point, usl-scalability]
level: practitioner
status: verified
description: "Read throughput vs latency curves from stepped load tests to find the knee (saturation) point, fit Universal Scalability Law models, and turn it into a capacity statement."
sources:
  - https://www.brendangregg.com/usemethod.html
  - http://www.perfdynamics.com/Manifesto/USLscalability.html
  - https://grafana.com/docs/k6/latest/testing-guides/test-types/breakpoint-testing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Throughput vs latency curves and the knee point

## The shape
As offered load rises:
1. **Linear region:** throughput rises with load; latency flat.
2. **Knee:** a resource approaches saturation; queueing starts; latency bends upward while throughput gains shrink.
3. **Saturation / retrograde:** throughput plateaus or falls (contention, thrashing, retries) and latency climbs steeply; errors appear.

Operating target: comfortably below the knee (a rule of thumb, not from a standard: often 60-75% of the knee throughput), because queueing delay grows nonlinearly with utilisation (M/M/1: R = S / (1 - U); computed: U = 0.5 gives 2x the service time, 0.75 gives 4x, 0.9 gives 10x, 0.95 gives 20x).

## Producing the curve
Stepped open-model load with holds (each step 5-10 min). For each step, take steady-state values: achieved throughput X, p50/p95/p99 latency, error rate, and utilisation of key resources.
Plot: X (x-axis) vs p95 (y-axis), and offered vs achieved throughput (divergence = saturation or generator limit).

## Locating the knee
- Where p95 exceeds ~1.5-2x its low-load value, or where marginal throughput gain per step drops below ~50% of the previous step (both are working rules of thumb; pick and state your own criterion).
- Check which USE metric saturates at that step (CPU, DB connections, thread pool queue, disk I/O wait).

## USL (Universal Scalability Law)
X(N) = λN / (1 + σ(N-1) + κN(N-1)) with concurrency N: σ = contention (serialisation), κ = coherency (crosstalk). Gunther's own page writes the same law as C(N) = N / (1 + α(N-1) + βN(N-1)) with X(N) = C(N)·X(1), where α is contention and β is coherency; the CRAN `usl` package fits it from a few points. A short least-squares fit works too:
```python
import numpy as np
from scipy.optimize import curve_fit
def usl(N, lam, s, k): return lam * N / (1 + s * (N - 1) + k * N * (N - 1))
N = np.array([1, 2, 4, 8, 16, 32, 64])
# X = measured throughput at each concurrency
(lam, s, k), _ = curve_fit(usl, N, X, p0=[X[0], 0.01, 0.0001], bounds=(0, [1e4, 1, 1]))
n_peak = np.sqrt((1 - s) / k)      # concurrency where throughput peaks (k > 0)
```
On synthetic data generated with λ=100, σ=0.05, κ=0.001 plus 1% noise, the fit returned λ=100.8, σ=0.0492, κ=0.00103 and a peak at N = 30.3 (the exact curve peaks at N = 31, X = 904). κ > 0 means throughput eventually declines as concurrency grows.

## Report wording (illustrative numbers, not measurements)
"Throughput scales linearly to ~420 req/s; knee at ~480 req/s (DB CPU 85%, p95 290 -> 610 ms); maximum ~510 req/s with errors beyond. Recommended operating limit 350 req/s."

## Gotchas
- Closed-model tests flatten the curve artificially (load self-limits); use arrival rate.
- Generator saturation looks like a knee: verify generator CPU and dropped iterations.

## Verify
Repeat the knee step: latency and throughput reproduce within normal variance.

## Checked
Python 3.14 with NumPy and SciPy in a scratch venv; k6 v1.4.0; fetched pages.
- Computed: M/M/1 factors 1/(1-U) for U = 0.5, 0.75, 0.9, 0.95; the USL curve fit above (seeded noise) and its peak N = sqrt((1 - sigma) / kappa); the exact curve's peak by enumeration (N = 31, X = 903.8).
- Fetched: Neil Gunther's USL page (formula with alpha/beta, C(N) = X(N)/X(1)), CRAN `usl` package page, k6 breakpoint-testing guide (ramping-arrival-rate, abortOnFail), Brendan Gregg's USE method page (URL live). A k6 `abortOnFail` threshold with `delayAbortEval` stopped a ramp and exited with code 99 (see the breakpoint skill).
