---
id: computing-software.cloud-infrastructure-engineering.observability.slo-based-alerting
name: slo-based-alerting
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [observability, alerting, slo-based-alerting, burn-rate, multiwindow, multi-burn-rate, error-budget, recording-rules, prometheus, promql, histogram, latency-slo, sloth, pyrra, openslo, promtool, alert-unit-tests, low-traffic, minimum-events, datadog-slo, google-cloud-monitoring-slo, cloudwatch-application-signals, grafana-slo, nobl9, alertmanager]
level: advanced
status: draft
description: "Implement SLO burn-rate alerts: recording rules for availability and histogram latency SLIs, generating rules with Sloth/Pyrra, low-traffic guards, vendor SLO alerts, and promtool tests."
sources: ["Google SRE Workbook - Alerting on SLOs", "Sloth documentation", "Pyrra documentation", "Prometheus documentation - Unit testing for rules"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SLO-based alerting — implementing burn-rate pages that hold up in production

**Goal:** working, tested alert rules that page when an SLO's error budget is burning fast
enough to matter — for availability *and* latency SLIs, on busy and quiet services alike.

The burn-rate thresholds (14.4x/1h+5m, 6x/6h+30m, 1x/3d+6h) and why multiwindow works are in
`computing-software.cloud-infrastructure-engineering.site-reliability-engineering.slos-and-error-budgets`.
This skill is the implementation.

## 1. Recording rules: ratios per window
Compute the error ratio once per window, by summing *before* dividing:
```yaml
groups:
- name: slo-checkout
  rules:
  - record: slo:sli_error:ratio_rate5m
    labels: {slo: checkout-availability}
    expr: |
      sum(rate(http_requests_total{job="checkout",code=~"5.."}[5m]))
      /
      sum(rate(http_requests_total{job="checkout"}[5m]))
  # repeat for 30m, 1h, 2h, 6h, 1d, 3d
```
Long windows (3d) over raw counters are expensive to evaluate; Sloth/Pyrra compute them from shorter recorded windows instead.

## 2. Latency SLIs from histograms
Error = requests slower than the threshold = total − requests in the `le` bucket at the threshold:
```promql
1 - (
  sum(rate(http_request_duration_seconds_bucket{job="checkout",le="0.3"}[1h]))
  /
  sum(rate(http_request_duration_seconds_count{job="checkout"}[1h]))
)
```
The threshold must be an existing bucket boundary — otherwise you're measuring a different SLO. Native histograms (Prometheus 2.40+, stable later) avoid fixed buckets but query differently; check your version.

## 3. Generate, don't hand-write
Sloth spec (one per service, in the repo):
```yaml
version: prometheus/v1
service: checkout
slos:
- name: availability
  objective: 99.9
  sli:
    events:
      error_query: sum(rate(http_requests_total{job="checkout",code=~"5.."}[{{.window}}]))
      total_query: sum(rate(http_requests_total{job="checkout"}[{{.window}}]))
  alerting:
    name: CheckoutAvailability
    page_alert:   {labels: {severity: page}}
    ticket_alert: {labels: {severity: ticket}}
```
`sloth generate -i checkout.yaml -o rules.yaml` emits recording rules and the multiwindow alerts. Pyrra does the same as a Kubernetes CRD with a UI. Generated rules keep 50 services consistent.

## 4. Low-traffic services
At 20 requests/hour one failure is a 5% error ratio → instant 14.4x page. Options, in order:
1. **Synthetic traffic** to raise the event count (also detects zero-traffic outages).
2. **Minimum-event guard:** `and sum(increase(http_requests_total{job="x"}[1h])) > 100`.
3. Longer windows only (6h/3d), accepting slower detection.
4. Aggregate small services into one journey-level SLO.

## 5. Vendor equivalents
Datadog SLO burn-rate monitors, Google Cloud Monitoring SLO burn-rate alerting policies (`select_slo_burn_rate`), Grafana SLO, Nobl9, CloudWatch Application Signals SLOs — all implement the same idea; check whether they support **two windows per condition** (some only offer one, giving slower reset or noisier pages).

## 6. Test the rules
`promtool test rules slo_test.yaml` with synthetic series:
```yaml
tests:
- interval: 1m
  input_series:
  - series: 'http_requests_total{job="checkout",code="500"}'
    values: '0+20x120'
  - series: 'http_requests_total{job="checkout",code="200"}'
    values: '0+980x120'
  alert_rule_test:
  - eval_time: 65m
    alertname: CheckoutAvailability
    # promtool matches the FULL label set: copy the labels your generator really emits
    # (Sloth adds sloth_* labels). The ticket alert also fires here, so list it too.
    exp_alerts:
    - exp_labels: {severity: page}
    - exp_labels: {severity: ticket}
```
(2% errors = 20x burn on a 99.9% SLO, so the page should fire.) Add a test that 0.05% errors does **not** fire. Run in CI on every rule change.

## Gotchas
- `rate()` over a window shorter than 4x the scrape interval returns gaps; with 60 s scrapes, 5m is the practical minimum.
- Counter resets and missing series make ratios `NaN`; add absent-data alerts separately.
- Label mismatches between numerator and denominator silently produce empty results — use `sum` without `by` or identical `by` on both sides.
- A latency SLO page needs a different runbook from an availability page; route them separately.

## Verify
- [ ] Each SLO has generated recording rules and page/ticket alerts from a spec in version control.
- [ ] Latency SLO thresholds match histogram buckets.
- [ ] promtool tests prove fire and no-fire cases.
- [ ] Low-traffic SLOs have a guard or synthetic traffic.
- [ ] Alerts link to the SLO dashboard and runbook.

Uncertain: Sloth spec fields and native-histogram status per version should be checked against current releases.
