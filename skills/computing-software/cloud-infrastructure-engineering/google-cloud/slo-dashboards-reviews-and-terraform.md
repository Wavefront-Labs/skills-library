---
id: computing-software.cloud-infrastructure-engineering.google-cloud.slo-dashboards-reviews-and-terraform
name: slo-dashboards-reviews-and-terraform
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, slo-monitoring, slo-dashboards, slo-reporting, slo-review, slo-tuning, slo-terraform, error-budgets, burn-rate]
level: practitioner
status: gated
description: "Define Cloud Monitoring services and SLOs in Terraform with burn-rate alerts, build SLO dashboards and monthly reports, and run SLO reviews that tune targets and SLIs."
sources: ["https://cloud.google.com/stackdriver/docs/solutions/slo-monitoring", "https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/monitoring_slo", "https://cloud.google.com/stackdriver/docs/solutions/slo-monitoring/alerting-on-budget-burn-rate", "https://sre.google/workbook/implementing-slos/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SLO dashboards, reviews and Terraform

## 1. SLOs as code
```hcl
resource "google_monitoring_custom_service" "checkout" {
  service_id   = "checkout"
  display_name = "Checkout API"
}
resource "google_monitoring_slo" "availability" {
  service             = google_monitoring_custom_service.checkout.service_id
  slo_id              = "availability-28d"
  goal                = 0.999
  rolling_period_days = 28
  request_based_sli {
    good_total_ratio {
      good_service_filter  = "metric.type=\"loadbalancing.googleapis.com/https/request_count\" resource.type=\"https_lb_rule\" resource.label.backend_service_name=\"checkout-bes\" metric.label.response_code_class!=500"
      total_service_filter = "metric.type=\"loadbalancing.googleapis.com/https/request_count\" resource.type=\"https_lb_rule\" resource.label.backend_service_name=\"checkout-bes\""
    }
  }
}
resource "google_monitoring_alert_policy" "fast_burn" {
  display_name = "checkout fast burn"
  combiner     = "OR"
  conditions {
    display_name = "fast burn rate"
    condition_threshold {
      filter          = "select_slo_burn_rate(\"${google_monitoring_slo.availability.id}\", \"<WINDOW>s\")"
      comparison      = "COMPARISON_GT"
      threshold_value = <BURN_THRESHOLD>
      duration        = "0s"
    }
  }
  notification_channels = [var.pager_channel]
}
```
Add a slow-burn policy (longer window, lower threshold) to a ticket channel. Burn rate above 1 means the SLO is missed if the error rate is sustained. App Engine and Istio services are detected automatically per the SLO docs; Terraform argument names here are (gated: unconfirmed, source is paywalled or blocked).

## 2. Dashboards and reporting
- Service view (Monitoring → Services) shows SLI, compliance and remaining error budget per SLO.
- Custom dashboard tiles for a portfolio view using SLO time-series selectors (see Retrieving SLO data in the SLO docs).
- Monthly report per service: compliance, budget consumed, top incidents eating budget.

## 3. SLO review (monthly)
Ask: did users complain while we were within SLO (SLI or target too loose)? Did we burn budget with
no user pain (too strict, or SLI measuring the wrong thing)? Did the error budget policy trigger and
was it followed (feature freeze, reliability work)? Adjust **one** thing at a time and record why.

## Gotchas
- Good/total filters must count the same requests; mismatched filters give >100% or nonsense.
- Excluding 4xx can hide client-visible breakage such as 429s from your own rate limiter.
- Changing the SLO definition resets comparability; keep the old SLO for a period in parallel.

## Verify
- [ ] `terraform plan` clean; the service page shows the SLO with budget data.
- [ ] Synthetic error injection in staging triggers the fast-burn alert.

## Checked
2026-10-28. Confirmed: SLO monitoring overview (App Engine and Istio services), burn-rate alerting page (`select_slo_burn_rate`, burn rate above 1 means out of SLO if sustained), load balancer SLI page (`https_lb_rule`, `response_code_class`).
Gated: the Terraform registry page for `google_monitoring_slo` returned empty text, so the Terraform argument names (`rolling_period_days`, `request_based_sli`, `good_total_ratio`, `basic_sli`) are unconfirmed.
Removed: 14.4 and 6 thresholds, window lengths, `select_slo_budget_fraction`/`select_slo_compliance` names, Cloud Run/GKE auto-detection claim, and the BigQuery export flow.
Method: documentation only; no commands were run.
