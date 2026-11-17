---
id: computing-software.cloud-infrastructure-engineering.kubernetes.sli-definition-from-ingress-and-mesh
name: sli-definition-from-ingress-and-mesh
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, slo-dashboards, sli-definition, sli, promql, service-mesh]
level: practitioner
status: docs-checked
description: "Define availability and latency SLIs from ingress controller and service mesh metrics, exclude noise, and turn them into recording rules and burn-rate alerts."
sources: ["https://sre.google/workbook/alerting-on-slos/", "https://sre.google/workbook/implementing-slos/", "https://istio.io/latest/docs/reference/config/metrics/", "https://kubernetes.github.io/ingress-nginx/user-guide/monitoring/", "https://github.com/kubernetes/ingress-nginx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Defining SLIs from ingress and mesh metrics

An SLI is good events divided by valid events, measured as close to the user as possible.

## Availability from ingress-nginx
```promql
sum(rate(nginx_ingress_controller_requests{ingress="shop",status!~"5.."}[5m]))
/
sum(rate(nginx_ingress_controller_requests{ingress="shop"}[5m]))
```

## Latency (share of requests faster than 250 ms)
```promql
sum(rate(nginx_ingress_controller_request_duration_seconds_bucket{ingress="shop",le="0.25"}[5m]))
/
sum(rate(nginx_ingress_controller_request_duration_seconds_count{ingress="shop"}[5m]))
```
The threshold must be an existing bucket boundary. ingress-nginx's default `--time-buckets` start at
0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5 seconds, so 0.25 exists and 0.3 does not; change the controller's
bucket flags if you need another threshold. The ingress-nginx project has announced its retirement
(best-effort maintenance only until March 2026), so these metric names apply to existing deployments;
check the metric names of the controller you are migrating to.

## From Istio (server-side view)
```promql
sum(rate(istio_requests_total{reporter="destination",destination_workload="checkout",response_code!~"5.."}[5m]))
/ sum(rate(istio_requests_total{reporter="destination",destination_workload="checkout"}[5m]))
```
The `reporter` label is `destination` for the server-side proxy and `source` for the client-side proxy;
pick one consistently.

## Exclude noise
- Health checks and probes (`path` label or a separate ingress).
- 4xx caused by clients are usually "good" for availability; 429 from your own rate limiting
  may be "bad". Decide and write it down.

## Recording rules and alerts
Record the ratio at several windows (`5m`, `30m`, `1h`, `6h`, `3d`), then alert with multi-window burn
rates. Google's SRE Workbook table for a 99.9 % SLO (error budget 0.001): page when both the 1h and 5m
error ratios exceed 14.4 x 0.001 (2 % of budget in 1 hour), page when both the 6h and 30m ratios exceed
6 x 0.001 (5 % of budget in 6 hours), and open a ticket for a 1 x burn over 3 days (10 % of budget).
Generators (Sloth, Pyrra) write these rules from a short SLO spec.

## Verify
Inject errors on a test route; the SLI drops and the fast-burn alert fires within minutes.

## Checked

2026-10-27. Release: ingress-nginx docs and source (main), Istio metrics reference, SRE Workbook (accessed October 2026)
- Corrected the burn-rate table: the SRE Workbook lists 14.4x over 1 hour (page), 6x over 6 hours (page) and 1x over 3 days (ticket), with a 5-minute and 30-minute short window for the first two; the old text called the 6x/6h rule a ticket.
- Corrected the latency example: ingress-nginx's default histogram buckets include 0.25 but not 0.3 seconds, so the `le="0.3"` query would return nothing by default.
- Confirmed `nginx_ingress_controller_requests`, `nginx_ingress_controller_request_duration_seconds` and the `status` and `ingress` labels (ingress-nginx monitoring docs and metrics source), and the Istio `reporter` label semantics (Istio metrics reference).
- Noted the ingress-nginx retirement announcement (project README: best-effort maintenance until March 2026).

Method: documentation only; no commands were run.
