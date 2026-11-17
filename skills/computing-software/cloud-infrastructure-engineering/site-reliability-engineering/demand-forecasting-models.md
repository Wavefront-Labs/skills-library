---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.demand-forecasting-models
name: demand-forecasting-models
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [demand-forecasting-model, growth-projection, capacity-planning, predict-linear]
level: practitioner
status: docs-checked
description: "Forecast demand for capacity planning: the SRE Book requirements for the forecast, and Prometheus predict_linear as a short-horizon linear projection with its limits."
sources: ["https://sre.google/sre-book/introduction/", "https://prometheus.io/docs/prometheus/latest/querying/functions/#predict_linear"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Demand forecasting models

## What the forecast must do (SRE Book, Introduction)
Capacity planning needs an accurate organic demand forecast that extends beyond the lead time required to acquire
capacity, an accurate incorporation of inorganic demand sources (see
`computing-software.cloud-infrastructure-engineering.site-reliability-engineering.organic-and-inorganic-demand-planning`),
and regular load testing to correlate raw capacity to service capacity. Forecast the demand driver (requests, stored
bytes) and convert it to resources using the measured per-instance capacity (see
`computing-software.cloud-infrastructure-engineering.site-reliability-engineering.capacity-load-testing-and-benchmarks`).

## Short-horizon linear projection (Prometheus predict_linear)
- `predict_linear(v range-vector, t scalar)` predicts the value of a series `t` seconds from now using simple linear
  regression over the range vector `v`.
- The range vector needs at least two float samples. If `+Inf` or `-Inf` appears in it, the prediction is `NaN`.
- Use it only with gauges; it works only on float samples, and histogram-only elements are ignored (in mixed series only
  the float samples are used).
- It extrapolates a straight line from the window you give it, so it suits steady growth such as a filling resource over a
  short horizon, not seasonal or compounding demand. Choose the window and horizon deliberately and check the result
  against actuals.

## Gotchas
- Past launches and outages inside the fit window distort a linear fit; separate known steps before projecting.
- A forecast that stops short of the acquisition lead time does not satisfy the requirement above.

## Verify
- [ ] The forecast horizon exceeds the lead time to acquire capacity.
- [ ] Forecast versus actual is reviewed regularly.

## Checked

Checked 2026-11-09. Confirmed against the SRE Book Introduction (capacity planning requirements) and the Prometheus
functions page (predict_linear semantics and limits). Removed: the Forecasting Principles and Practice source (not read),
the table of linear, compound and seasonal models, the Holt-Winters and Prophet sketch, the 95th percentile weekly peak
rule, P50/P90 provisioning, the 15 percent MAPE backtest threshold and the two-year seasonality requirement, none of
which appeared on the pages read.

Method: docs-checked 2026-11-09 against the pages above, read from downloaded copies; no commands were run.
