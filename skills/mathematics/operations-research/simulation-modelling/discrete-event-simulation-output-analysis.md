---
id: mathematics.operations-research.simulation-modelling.discrete-event-simulation-output-analysis
name: discrete-event-simulation-output-analysis
category: mathematics
field: operations-research
product: simulation-modelling
tags: [operations-research, simulation-modelling, simulation, discrete-event-simulation, des, simpy, anylogic, arena, simio, input-modelling, distribution-fitting, warm-up-period, welch-method, replications, batch-means, confidence-interval, common-random-numbers, variance-reduction, verification, validation, terminating-simulation, steady-state, random-seed, monte-carlo]
level: practitioner
status: verified
description: "Build and analyse a discrete-event simulation properly: fit inputs from data, verify and validate, handle warm-up, run enough replications for a CI, and compare scenarios with common random numbers."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Discrete-event simulation output analysis

**Goal:** use a simulation to compare options (staffing, layout, policy) with
statistically sound confidence intervals — not a single run's lucky number.

## 1. Scope the model
- **Question and KPI** first: "average wait in clinic B with 4 vs 5 nurses".
- **Terminating** (natural end: a clinic day, a shift) vs **steady-state** (a 24/7
  system's long-run behaviour). This decides the output method (sections 5–6).
- Include only processes that affect the KPI; detail costs build time and validation effort.

## 2. Input modelling
- Collect real inter-arrival and service times (≥ ~100 observations per input where possible).
- Plot histograms; fit candidate distributions (exponential, gamma, lognormal, Weibull)
  with `scipy.stats.<dist>.fit` or R `fitdistrplus`; compare by QQ plot and AIC.
  Goodness-of-fit p-values reject everything at large n — judge by plots.
- Arrival rates usually vary by time of day: use a **non-stationary Poisson** process
  (piecewise rates per hour), not one average rate.
- No data? Use a **triangular (min, mode, max)** from experts and flag it as an assumption.
- Check independence: service time may depend on customer type — model types separately.

## 3. Build (SimPy example skeleton)
```python
import simpy, random
def patient(env, nurses, waits, rng):
    t0 = env.now
    with nurses.request() as req:
        yield req
        waits.append(env.now - t0)
        yield env.timeout(rng.lognormvariate(2.3, 0.4))
def arrivals(env, nurses, waits, rng, rate):
    while True:
        yield env.timeout(rng.expovariate(rate))
        env.process(patient(env, nurses, waits, rng))
def run(seed, n_nurses, horizon=480, rate=0.3):
    rng = random.Random(seed); env = simpy.Environment(); waits = []
    nurses = simpy.Resource(env, capacity=n_nurses)
    env.process(arrivals(env, nurses, waits, rng, rate)); env.run(until=horizon)
    return sum(waits) / len(waits)
```
Mean service time is e^(2.3+0.08) = 10.8 minutes, so rate 0.3 per minute is an offered load of about 3.2 nurses (4 nurses run at about 81% utilisation). The original rate of 0.5 gave 5.4 nurses of load, so 4 or 5 nurses are overloaded and the day's mean wait grows without settling (about 61 minutes). Always compare the offered load (arrival rate x mean service time) with the capacity before reading any wait times. Run here: 30 replications of `run(seed, 4)` gave mean wait 3.9 minutes, CI half-width 0.88 using t(0.975, 29) = 2.045. The skeleton shares one `rng` for brevity; in real models use a **separate random stream
per input** (arrivals vs service) so scenarios stay synchronised (section 7).

## 4. Verify, then validate
- **Verification** (built right): trace a few entities step by step; run with
  deterministic times and check against hand calculation; test extremes (one server,
  zero arrivals); compare with an analytic queue formula where one applies (see
  mathematics.operations-research.queueing-theory.queue-capacity-planning-with-littles-law).
- **Validation** (right model): reproduce current-state KPIs from history (e.g. simulated
  average wait within the CI of observed wait) before testing changes. Show stakeholders
  an animation — they spot wrong logic quickly.

## 5. Terminating simulations: replications
Each replication = one independent day with a different seed. Output = one KPI value per
replication. CI: mean ± t₀.₉₇₅,ₙ₋₁ · s/√n.
How many? Run n₀ = 10 pilot replications, then n ≈ n₀ · (current half-width / target half-width)².
```python
import statistics as st
res = [run(seed, 4) for seed in range(30)]
m, s = st.mean(res), st.stdev(res); hw = 2.045 * s / 30**0.5   # t(0.975, 29)
```

## 6. Steady-state simulations: warm-up
Systems start empty, biasing early output low. Use **Welch's method**: average the KPI
time series across replications, smooth with a moving window, and pick the time after
which it flattens. Delete data before that point in every replication. Then use either
several long replications or **batch means** within one long run (batches large enough
that batch averages are roughly uncorrelated).

## 7. Comparing scenarios
- Use **common random numbers**: the same seeds for both scenarios, so differences come
  from the change, not luck. Then analyse **paired differences**: CI on (A − B) per seed.
  The variance reduction depends on the model: on the skeleton above the paired standard deviation (2.34) was only slightly below the independent-seed figure (2.41), so measure it rather than assume it.
- If the CI on the difference excludes 0, the scenarios differ; report its size in KPI units.
- Many scenarios → adjust for multiple comparisons or use ranking-and-selection procedures.

## Gotchas
- One run with one seed is an anecdote.
- Averages hide tails — report percentiles (90th percentile wait) per replication too.
- Fitted distributions with unbounded tails (lognormal) can generate absurd values; truncate at physical limits.
- Uncertain: "≥ 100 observations" for input fitting is a practical rule of thumb.

## Verify
- [ ] Inputs fitted from data (or flagged expert assumptions), with time-varying arrivals.
- [ ] Deterministic/extreme tests and an analytic comparison pass.
- [ ] Baseline reproduces historical KPIs.
- [ ] Warm-up removed (steady-state) or replications per period (terminating).
- [ ] Replication count meets a stated CI half-width.
- [ ] Scenarios compared with common random numbers and paired CIs.
