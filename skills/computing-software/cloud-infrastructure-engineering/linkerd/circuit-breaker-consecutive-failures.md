---
id: computing-software.cloud-infrastructure-engineering.linkerd.circuit-breaker-consecutive-failures
name: circuit-breaker-consecutive-failures
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, circuit-breaking, failure-accrual, resilience]
level: practitioner
status: docs-checked
description: "Enable consecutive failure accrual on a Service so Linkerd stops routing to an endpoint that keeps failing, and confirm the resulting policy with the diagnostics command."
sources:
  - https://linkerd.io/2.19/tasks/circuit-breakers/
  - https://linkerd.io/2.19/reference/circuit-breaking/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Linkerd's circuit breaking tracks consecutive failures from each endpoint in its internal load balancer. When an endpoint fails too many times in a row, it is ignored and traffic goes to the remaining replicas. After a backoff period the endpoint is reintroduced so Linkerd can see whether it recovered.

Enable it by annotating the Service:

```bash
kubectl annotate -n circuit-breaking-demo svc/bb balancer.linkerd.io/failure-accrual=consecutive
```

Then print the policy the proxy will use for the Service and port:

```bash
linkerd diagnostics policy -n circuit-breaking-demo svc/bb 8080 -o json | jq '.protocol.Kind.Detect.http1.failure_accrual'
```

The output shows `ConsecutiveFailures` with `max_failures` 7, a `min_backoff` of 1 second, a `max_backoff` of 60 seconds and a `jitter_ratio` of 0.5. Seven consecutive failures trip the breaker.

Points to remember:

- Circuit breaking is incompatible with ServiceProfiles. While a ServiceProfile exists for the annotated Service, proxies do not perform circuit breaking.
- The annotation goes on the Service, not on the workload.

## Checked

2026-11-03. Confirmed against: https://linkerd.io/2.19/tasks/circuit-breakers/, https://linkerd.io/2.19/reference/circuit-breaking/.

Removed or reworded: Viz observation bullet and the closing usage advice.

Method: documentation only; no commands were run.
