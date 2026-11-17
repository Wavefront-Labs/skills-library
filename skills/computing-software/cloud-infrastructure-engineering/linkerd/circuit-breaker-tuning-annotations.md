---
id: computing-software.cloud-infrastructure-engineering.linkerd.circuit-breaker-tuning-annotations
name: circuit-breaker-tuning-annotations
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, circuit-breaking, annotations, backoff]
level: advanced
status: docs-checked
description: "Tune consecutive-failure circuit breaking with the max-failures, min-penalty, max-penalty and jitter-ratio annotations on a Service."
sources:
  - https://linkerd.io/2.19/reference/circuit-breaking/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Once `balancer.linkerd.io/failure-accrual: consecutive` is set on a Service, four more annotations adjust how aggressively the breaker trips and how it probes for recovery. All are set on the Service.

- `balancer.linkerd.io/failure-accrual-consecutive-max-failures`: how many failures in a row mark an endpoint unavailable. The effective value seen in policy output by default is 7.
- `balancer.linkerd.io/failure-accrual-consecutive-min-penalty`: the minimum time an endpoint stays unavailable. Defaults to 1 second.
- `balancer.linkerd.io/failure-accrual-consecutive-max-penalty`: the upper bound on the time between probe requests. It must be non-zero and greater than the min penalty. If absent, the default is one minute (`1m`).
- `balancer.linkerd.io/failure-accrual-consecutive-jitter-ratio`: jitter applied to probation backoffs, a floating-point number between 0.0 and 100.0. Default 0.5.

Example:

```bash
kubectl annotate svc/bb \
  balancer.linkerd.io/failure-accrual-consecutive-max-failures=3 \
  balancer.linkerd.io/failure-accrual-consecutive-max-penalty=30s
```

Lower max-failures reacts faster but risks tripping on transient errors. A shorter max penalty means failed endpoints are probed more often, which speeds recovery and also sends more traffic to a still-broken replica. Jitter spreads probes from many clients so they do not all hit a recovering endpoint at the same moment.

## Checked

2026-11-03. Confirmed against: https://linkerd.io/2.19/reference/circuit-breaking/.

Removed or reworded: Nothing; annotation names, defaults and ranges all match the reference page.

Method: documentation only; no commands were run.
