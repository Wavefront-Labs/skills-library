---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.gcp-committed-use-discounts
name: gcp-committed-use-discounts
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, rate-optimization, gcp-committed-use-discounts, committed-use-discounts, sustained-use-discounts, google-cloud, flexible-cud, commitment-discounts]
level: practitioner
status: docs-checked
description: "Use Google Cloud committed use discounts: resource-based vs spend-based (flexible) CUDs, sustained use discounts, sharing, sizing and no-cancel terms."
sources: ["https://cloud.google.com/compute/docs/instances/committed-use-discounts-overview", "https://cloud.google.com/docs/cuds-spend-based", "https://cloud.google.com/compute/docs/sustained-use-discounts"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Google committed use discounts (CUDs)

## Types
- **Resource-based CUDs** (Compute Engine): commit to a minimum amount of resources (vCPUs, memory,
  GPUs, local SSD, sole-tenant nodes; separate license and block-storage categories) for 1 or 3
  years, tied to a region and project. The 3-year plan discounts more. Hardware commitments give
  up to 70% for memory-optimised series and up to 55% for other series. A commitment covers only
  its own category and cannot mix hardware, licenses and storage.
- **Spend-based CUDs**: commit to a minimum hourly spend for 1 or 3 years, bought at billing-account
  level, separately for each service that offers them.
  - **Compute flexible CUD**: one commitment spans Compute Engine, GKE (Standard and Autopilot) and
    Cloud Run (instance-based services, jobs, worker pools). Documented rates for many machine
    series are 28% (1-year) and 46% (3-year); check the overview table for your series. The
    hourly commitment fee is paid regardless of usage. Overage is charged at on-demand rates.
  - Other services have their own spend-based CUDs; see the product list in the CUD docs.
- **Sustained use discounts** (automatic, no action needed) apply to VMs from Compute Engine and
  GKE, for example general-purpose N1, N2 and N2D vCPUs and memory. Discount steps rise at 25%,
  50%, 75% and 100% of the month, and reset each month. SUDs do not apply to usage already
  covered by CUDs, nor to App Engine or Dataflow VMs.
- Some spend-based CUDs are migrating to a new consumption model that uses discounts rather than
  credits; the move is flagged on the Billing Overview page, and it changes how the discount
  appears in exported data. In the legacy program the commitment amount was the on-demand price.

## Sizing
1. Use the CUD analysis report (Billing -> Committed use discounts) to judge coverage and
   utilisation, and Recommender for commitment recommendations
   (`gcloud recommender recommendations list --recommender=<RECOMMENDER_ID> --location=<REGION> --project=<PROJECT_ID>`).
2. Resource-based: size to steady-state minimum usage per series per region.
3. Flexible: commit to the steady floor of eligible hourly spend not covered by resource-based CUDs.
4. Layer: resource-based for stable series, flexible for the variable mix.

## Sharing
- A resource-based commitment can cover usage in the purchasing project only, or across all
  projects under the billing account, depending on the account's CUD sharing configuration.
  New billing accounts created on or after 16 June 2026 have sharing enabled by default.
- Spend-based CUDs apply to eligible usage in any project the billing account pays for.
- Google documents "Attribution of committed use discount fees and credits" for how fees and
  credits are split across projects; align it with your chargeback policy.

## Gotchas
- Commitments cannot be cancelled. Resource-based commitments bill monthly whether used or not;
  spend-based commitments cost the agreed monthly amount for the full term.
- Purchasing spend-based CUDs needs the Billing Account Administrator role.
- A spend-based commitment cannot be moved between billing accounts except via Cloud Billing Support.
- A purchase in the last 10 minutes of an hour skips an extra hour before it starts.

## Verify
- [ ] Coverage and utilisation per commitment type tracked monthly.
- [ ] Sharing and attribution settings documented and match chargeback.

## Checked

Method: docs-checked 2026-11-09 against Compute Engine CUD overview (searched and read in part), spend-based CUDs page (read in full) and sustained use discounts page (searched, not read in full). Removed unconfirmed: the 37%/55% and 28%/46% general-purpose rate pairs outside the table quoted, per-series SUD exclusion list, Recommender ID, cud-analysis page claims, "reservations" note, proportional vs priority attribution wording.
