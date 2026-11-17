---
id: computing-software.cloud-infrastructure-engineering.google-cloud.spot-pricing-and-price-history
name: spot-pricing-and-price-history
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, spot-vms, spot-pricing, spot-price-history, cloud-billing-catalog-api, pricing-export, cost-optimisation]
level: practitioner
status: docs-checked
description: "Find current Spot VM prices, keep your own price history from the Cloud Billing Catalog API or the BigQuery pricing export, and measure realised Spot savings."
sources: ["https://cloud.google.com/spot-vms/pricing", "https://cloud.google.com/billing/docs/reference/rest/v1/services.skus/list", "https://cloud.google.com/billing/docs/how-to/export-data-bigquery-tables/pricing-data", "https://cloud.google.com/compute/docs/instances/spot"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spot pricing and price history

Spot VMs are excess Compute Engine capacity sold at a discount to on-demand prices (the Spot VMs page says up to 91% for
many machine types, GPUs, TPUs and Local SSDs). Compute Engine may preempt them at any time, so use them for
fault-tolerant work such as batch or stateless applications.

## 1. Current prices
Per the Spot VMs page: use the Spot VMs pricing page, the Cloud Billing Catalog API, or sign up for Spot pricing
announcements. The Catalog API method is `services.skus.list` (`GET https://cloudbilling.googleapis.com/v1/{parent=services/*}/skus`)
with optional `currencyCode` (defaults to USD) and `pageSize` (defaults to 5000). Look up the Compute Engine service ID
via the services list rather than copying one, and read the SKU descriptions to pick out Spot SKUs.

## 2. Your own history
The pricing page shows only current prices, so capture history yourself:
- Enable the Cloud Billing pricing export to BigQuery. Data lands in a table named `cloud_pricing_export`. Pricing data is
  generated once per day (`pricing_as_of_time`) and each load has an `export_time` that always increases.
- Useful columns: `geo_taxonomy.regions` (regions of the SKU; null for GLOBAL SKUs) and `list_price.tiered_rates`
  (`usd_amount`, `start_usage_amount`; one row per tier, so UNNEST the array). The taxonomy fields are marked Preview
  and may change.
- Or schedule a job that stores Catalog API results in a dated table.

## 3. Realised savings
Take Spot usage and cost from the standard billing export and compare with the same usage priced at the on-demand SKU
rates you would actually pay, to report savings net of re-run costs from preemption.

## Gotchas
- Preempted Spot VMs that were stopped (TERMINATED) are not charged for VM hours, but attached persistent disks still
  incur storage charges; VMs preempted in the first minute are not billed (premium operating system charges still apply).
- Spot VMs do not reduce the cost of premium operating systems.
- Spot VMs are excluded from the Compute Engine SLA and are not covered by the Free Tier credits.
- Spot VMs consume standard quota unless you have been granted preemptible quota in the region.

## Verify
- [ ] A dashboard shows the daily Spot price per family and region for the period you track.
- [ ] A monthly report shows Spot spend against the on-demand equivalent.

## Checked
2026-11-09: read the Spot VMs concept page, services.skus.list reference and the pricing export data page. Removed:
the "60-91%" range, Compute Engine service ID and the curl/jq and SQL examples (SKU description strings and column
names for SKU text not confirmed), CUD/SUD and GPU-price-independence claims. The Spot pricing page itself is mostly
rates and was used only as a pointer; no figures kept.
Method: documentation only; no commands were run.
