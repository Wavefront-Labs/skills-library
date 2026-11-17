---
id: repair-maintenance.reliability-engineering-failure-analysis.life-data-analysis.weibull-analysis-and-replacement-intervals
name: weibull-analysis-and-replacement-intervals
category: repair-maintenance
field: reliability-engineering-failure-analysis
product: life-data-analysis
tags: [life-data-analysis, weibull, weibull-analysis, beta, eta, shape-parameter, characteristic-life, mtbf, mttf, b10-life, suspensions, censored-data, maximum-likelihood, median-ranks, bathtub-curve, infant-mortality, wear-out, reliability-function, replacement-interval, optimal-replacement, python, scipy, reliasoft, cmms-data]
level: advanced
status: draft
description: "Fit a Weibull to failure data with suspensions (runnable Python), read beta for infant mortality vs random vs wear-out, compute B10 life and reliability, and set or reject a replacement interval."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Weibull analysis and replacement intervals

**Goal:** turn a list of failure (and non-failure) ages for one component and one
failure mode into numbers that answer "does it wear out, and if so when should we
replace it?" — instead of quoting a single MTBF that hides the pattern.

> Draft: the Python below was run and gives the shown output. Small samples (< ~10
> failures) give wide confidence bounds; report them, or treat the result as a guide.

## 1. Get clean data
- **One failure mode per analysis.** Mixing "bearing seized" with "seal leaked"
  produces a meaningless β. Pull from CMMS work orders and read the descriptions.
- **Age = operating time since install/overhaul** (hours, cycles, km, tonnes) for
  that item, not calendar dates between any failures on the machine.
- **Suspensions (right-censored data):** units removed unfailed, still running, or that
  failed by a *different* mode. They matter — dropping them makes life look shorter.
- Watch for inconsistent units and "replaced on PM" mislabelled as failures.

## 2. Fit (maximum likelihood, with suspensions)
```python
import numpy as np
from scipy.stats import weibull_min
from scipy.optimize import minimize

fail = np.array([1200, 1850, 2300, 2900, 3400, 4100])   # hours at failure
susp = np.array([1500, 3000, 4500, 4500])               # still running / removed unfailed

def nll(p):
    beta, eta = np.exp(p)            # log-params keep them positive
    return -(weibull_min.logpdf(fail, beta, scale=eta).sum()
             + weibull_min.logsf(susp, beta, scale=eta).sum())

res = minimize(nll, x0=np.log([1.5, 3000]), method="Nelder-Mead")
beta, eta = np.exp(res.x)
print(f"beta={beta:.2f} eta={eta:.0f} h")
print("B10 life =", round(weibull_min.ppf(0.10, beta, scale=eta)), "h")
print("R(2000 h) =", round(weibull_min.sf(2000, beta, scale=eta), 3))
```
Output: `beta=2.41 eta=3979 h`, `B10 life = 1562 h`, `R(2000 h) = 0.826`.
(`pip install numpy scipy`. The `reliability` Python package or commercial tools such
as Weibull++ give the same plus confidence bounds and probability plots.)

Also make a **probability plot** (median ranks, Bernard's approximation
F ≈ (i − 0.3)/(n + 0.4), adjusted for suspensions) and check the points lie near a
straight line. A kink suggests mixed modes or a failure-free period (3-parameter
Weibull with γ).

## 3. Read β (shape) and η (scale)
| β | Pattern | Maintenance implication |
|---|---|---|
| < 1 | infant mortality (falling failure rate) | fix installation, QA, burn-in; **time-based replacement makes it worse** |
| ≈ 1 | random (constant rate) | time-based replacement useless; use condition monitoring or run-to-failure |
| 1–4 | early wear-out | CBM if a P-F interval exists; replacement may pay if failure is costly |
| > 4 | strong, predictable wear-out | scheduled replacement works well |
η = age by which **63.2%** have failed. **MTTF = η·Γ(1 + 1/β)** (use `scipy.special.gamma`).
MTBF alone can't tell you any of this — β = 0.5 and β = 5 can share an MTBF.

## 4. Set (or reject) a replacement interval
Only if β > 1 and failure costs more than planned replacement:
- **Reliability target approach:** replace at the age where R(t) falls to target, e.g.
  B10 (90% survive) for important items: here ≈ 1560 h.
- **Cost approach (age replacement):** minimise cost per hour
  C(T) = [Cp·R(T) + Cf·(1 − R(T))] / ∫₀ᵀ R(t)dt, with Cp = planned replacement cost,
  Cf = failure cost (incl. downtime). Solve numerically (`scipy.integrate.quad`
  + `minimize_scalar`). Benefit grows with β and the Cf/Cp ratio; if Cf/Cp < ~2 the
  optimum is often "run to failure".
- Compare with a **condition-based task** — usually cheaper when a P-F interval exists.

## 5. Report
β, η with confidence bounds, number of failures and suspensions, the plot, the
recommended interval or strategy, and assumptions (one mode, operating context).
Re-run as data accumulates.

## Gotchas
- Leaving out suspensions biases life short and recommends wasteful replacements.
- Calendar time on intermittently used equipment distorts β.
- Two lines on a probability plot = two failure modes; split them.
- A β < 1 result is a quality/installation problem, not a PM-interval problem.

## Verify
- [ ] Single failure mode; ages in operating units; suspensions included.
- [ ] Fit method stated (MLE preferred with suspensions or < 20 failures).
- [ ] Probability plot reasonably straight.
- [ ] β interpreted correctly before any interval is proposed.
- [ ] Interval justified by reliability target or cost model, compared against CBM.
