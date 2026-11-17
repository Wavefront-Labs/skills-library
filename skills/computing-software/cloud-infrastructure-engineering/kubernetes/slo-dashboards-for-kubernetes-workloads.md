---
id: computing-software.cloud-infrastructure-engineering.kubernetes.slo-dashboards-for-kubernetes-workloads
name: slo-dashboards-for-kubernetes-workloads
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, slo, sli, red-method, use-method, burn-rate, multi-window-multi-burn-rate, grafana, error-budget, istio-metrics, hpa-interaction]
level: advanced
status: docs-checked
description: "Designing SLO dashboards for Kubernetes workloads from mesh-derived request metrics, and wiring multi-window multi-burn-rate alerts that do not page on normal rollouts."
sources: ["https://sre.google/workbook/alerting-on-slos/", "https://istio.io/latest/docs/reference/config/metrics/", "https://github.com/kubernetes/kube-state-metrics/blob/main/docs/metrics/workload/pod-metrics.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SLO dashboards for Kubernetes workloads: the right signals, the right alerting shape

**Goal:** build a per-workload SLO dashboard from signals that exist in a typical k8s stack,
and wire burn-rate alerting that survives normal rollout noise. The burn-rate math and
error-budget policy live in
`computing-software.cloud-infrastructure-engineering.site-reliability-engineering.slos-and-error-budgets`
and `...error-budget-policy`; this skill is about where the k8s-side numbers come from.

## 1. RED for request-serving workloads, USE for everything else
- **RED** (Rate, Errors, Duration) fits anything handling requests (HTTP/gRPC services). In a
  cluster with a service mesh, mesh telemetry avoids re-instrumenting every app: Istio's
  standard metrics include `istio_requests_total` (labelled with `response_code` and `reporter`)
  and `istio_request_duration_milliseconds`. Without a mesh or ingress layer you are back to
  app-level instrumentation
  (`computing-software.cloud-infrastructure-engineering.observability.instrumentation-strategy`).
- **USE** (Utilization, Saturation, Errors) fits resource-bound workloads (batch processors,
  queue consumers, databases) where requests per second is not the natural unit. Saturation
  means queue depth or wait time, not just CPU percentage.

## 2. The k8s-specific signal gotchas
- **Pod-level availability is not service-level availability.** A running pod says nothing about
  whether the app serves successfully; build the SLI from request-serving signals (RED), not
  from pod phase.
- **Rollouts are not incidents.** A rolling update changes the number of available replicas by
  design, so replica-count alerting pages on normal deploys. Alert on the RED signals (actual
  error rate and latency), which stay flat through a healthy rollout and move only if the new
  version is broken.
- **Autoscaling**: aggregate RED metrics at the Service or Deployment level
  (`sum by (...)`), never per pod, or dashboards become sawtooths as replicas change.
- **Shared clusters**: a team's latency SLO can burn from node-level contention that its own
  error rate does not show; check node-level CPU metrics before assuming the regression is in
  the team's code (see
  `computing-software.cloud-infrastructure-engineering.kubernetes.cadvisor-and-cgroup-container-metrics`).

## 3. Multi-window multi-burn-rate alerting, applied
The Google SRE Workbook chapter "Alerting on SLOs" describes alerting on burn rate with a long
window plus a shorter window, so an alert fires quickly for a fast burn and stops soon after the
problem ends. Its worked example for a 99.9% SLO is a burn rate of 14.4 over a 1 hour window
(the page's table gives the budget consumed for each window and burn rate):
```promql
(
  sum(rate(istio_requests_total{destination_service=~"<SERVICE_REGEX>", response_code=~"5.."}[5m]))
  /
  sum(rate(istio_requests_total{destination_service=~"<SERVICE_REGEX>"}[5m]))
) > (14.4 * 0.001)
and
(
  sum(rate(istio_requests_total{destination_service=~"<SERVICE_REGEX>", response_code=~"5.."}[1h]))
  /
  sum(rate(istio_requests_total{destination_service=~"<SERVICE_REGEX>"}[1h]))
) > (14.4 * 0.001)
```
See `computing-software.cloud-infrastructure-engineering.kubernetes.prometheus-operator-prometheusrule-and-alertmanagerconfig`
for how the Prometheus Operator hosts rules like this.

## 4. Dashboard layout that gets used
- Top: current error budget remaining and burn rate over a few windows.
- Middle: RED or USE time series for the window being burned, with deploy markers overlaid if
  available, so "did we just deploy?" is answered on the same screen.
- Bottom: k8s drill-down signals (pod restarts, replica counts, node CPU) so a responder does
  not jump dashboards mid-incident.
See `computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-dashboard-design`
for general dashboard craft.

## Gotchas
- An SLO defined on a metric nobody alerts on is decoration; confirm the alerting rule actually
  loaded before trusting that the dashboard reflects the same math as the pager.
- Do not let one SLO cover a Deployment that fronts very different traffic patterns
  (synchronous API plus async webhook delivery); split them.

## Verify
- [ ] The SLI's underlying metric excludes health checks and synthetic probes that would dilute the real error rate.
- [ ] A deliberate rolling update does not trigger the burn-rate alert.
- [ ] A deliberately injected error rate does trigger the fast-burn alert within its designed window.
- [ ] The dashboard and the alerting rule read from the same underlying query.

## Checked
2026-11-01. Confirmed: the SRE Workbook "Alerting on SLOs" page (burn rate, long and short windows, 14.4 burn rate over 1 hour), the Istio standard metrics page (`istio_requests_total`, `istio_request_duration_milliseconds`, `response_code`, `reporter`). Removed (not confirmed in fetched pages): the NGINX ingress metric name, HPA and endpoint kube-state-metrics names, `maxUnavailable` wording, the CPU throttling metric, the `for:` advice, the rules-API command and the 2% budget wording.
Method: documentation only; no commands were run.
