---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.least-loaded-and-weighted-round-robin
name: least-loaded-and-weighted-round-robin
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [least-loaded-round-robin, weighted-round-robin-impl, load-balancing-policy, orca, load-balancing]
level: advanced
status: docs-checked
description: "Choose datacenter LB policies: round robin's failure modes, least-loaded and its sinkhole pitfall, and weighted round robin from backend load reports (gRFC A58)."
sources: ["https://sre.google/sre-book/load-balancing-datacenter/", "https://github.com/grpc/proposal/blob/master/A58-client-side-weighted-round-robin-lb-policy.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Least-loaded and weighted round robin policies

The SRE Book chapter Load Balancing in the Datacenter compares three policies.

## Simple round robin
Each client sends to each backend in its subset in turn (skipping lame-duck ones). It beats random choice but
the book saw up to 2x CPU spread between least and most loaded tasks, caused by small subsets, varying query
cost, machine diversity and unpredictable performance (antagonistic neighbours, restarts).

## Least-loaded round robin
Each client tracks active requests per backend and round-robins among those with the fewest.
- **Sinkhole**: a seriously unhealthy task may return fast errors, look idle and attract traffic. Fix: count
  recent errors as active requests.
- Limits: active count is a poor proxy for capability (requests that mostly wait on I/O), and a client sees only
  its own requests. Large services still saw about 2x spread, similar to round robin.

## Weighted round robin
Each client keeps a capability score per backend in its subset. Backends include their current query rate,
error rate and utilisation (typically CPU) in each response, including health checks; clients adjust scores
periodically, and failed requests are penalised. The book reports it drastically narrowed the spread between
the most and least utilised tasks.

### gRPC implementation (gRFC A58)
gRPC's `weighted_round_robin` policy is client-side balancing with direct load reports from backends, per-call
by default or periodic out-of-band when `enable_oob_load_report` is set. Per A58 the weight is
`qps / (utilization + (eps / qps) * error_utilization_penalty)`, with these config fields and defaults:
- `blackout_period`: default 10 seconds; a new endpoint gets no weight for that long.
- `weight_expiration_period`: default 3 minutes; stale load reports stop being used.
- `error_utilization_penalty`: default 1.0, must not be negative.
Check the gRFC for the remaining fields (such as the OOB reporting interval and weight update period).

## Choosing
| Situation | Policy |
|---|---|
| homogeneous backends, uniform cheap requests | round robin may be enough |
| variable request cost, no load reports | least-loaded, with errors counted as active requests |
| heterogeneous machines, need efficiency | weighted round robin with backend load reports |

## Checked
2026-11-01. Confirmed against the SRE Book chapter Load Balancing in the Datacenter and gRFC A58 (policy name,
weight formula, config field names and defaults). Removed: power-of-two-choices and Envoy `LEAST_REQUEST`
settings, the Go ORCA call, and verify targets, which neither page states.
Method: documentation only; no commands were run.
