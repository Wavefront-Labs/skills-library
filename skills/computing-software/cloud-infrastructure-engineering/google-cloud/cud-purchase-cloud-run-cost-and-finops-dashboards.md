---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cud-purchase-cloud-run-cost-and-finops-dashboards
name: cud-purchase-cloud-run-cost-and-finops-dashboards
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cost-optimisation, cud-recommendations, cud-purchase, committed-use-discounts, cloud-run-cost-optimization, finops-dashboards, looker-studio-billing]
level: practitioner
status: draft
description: "Buy committed use discounts from recommendations (resource vs spend-based), cut Cloud Run spend with billing mode, concurrency and min-instance choices, and build FinOps dashboards in Looker Studio."
sources: ["https://cloud.google.com/docs/cuds", "https://cloud.google.com/compute/docs/instances/committed-use-discounts-overview", "https://cloud.google.com/run/docs/tips/general#optimize_concurrency", "https://cloud.google.com/run/pricing", "https://cloud.google.com/billing/docs/how-to/visualize-data"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CUD purchase, Cloud Run cost and FinOps dashboards

## 1. Committed use discounts
| Type | Commits to | Flexibility |
|---|---|---|
| Resource-based (Compute) | vCPU/memory/GPU/local SSD of a machine series in a region, 1 or 3 years | none outside series/region |
| Spend-based (flexible / service CUDs) | $/hour across eligible services (Compute flex, Cloud Run, GKE Autopilot, Cloud SQL, etc.) | spans series/regions per CUD type |
Process: read the CUD recommender and the Billing **CUD analysis** report → commit to the steady
**floor** of usage (not the average) → buy in tranches quarterly.
```bash
gcloud recommender recommendations list --project=<P> --location=europe-west2 \
  --recommender=google.compute.commitment.UsageCommitmentRecommender
gcloud compute commitments create n2-eu-2026q4 --region=europe-west2 --plan=36-month \
  --type=GENERAL_PURPOSE_N2 --resources=vcpu=96,memory=384GB
```
Spend-based CUDs are bought in the Billing console against the billing account. Commitments
can't be cancelled; share them across projects via billing-account-level sharing.

## 2. Cloud Run cost
- **Billing mode**: request-based (CPU only during requests) for spiky HTTP; instance-based (`--no-cpu-throttling`) when there's background work or steady load — it's cheaper per vCPU-second and avoids throttled background tasks.
- **Concurrency**: raise from 1 to 40–80 for I/O-bound apps; fewer instances for the same load.
- **Min instances** only where cold starts break SLOs; they bill idle time.
- Right-size CPU/memory with the metrics tab (container CPU/memory utilisation); use CPU boost instead of permanently larger CPUs for slow starts.
- Cloud Run eligible for spend-based CUDs for steady baselines.

## 3. FinOps dashboards
- Enable **detailed** billing export to BigQuery (plus pricing export).
- Copy Google's Looker Studio billing template, point it at your export tables; add views by label (`team`, `env`, `app`), by project/folder and SKU; add CUD coverage/utilisation.
- Monthly: cost per team vs budget, top movers, unallocated (unlabelled) spend %; set budget alerts and cost anomaly notifications.

## Gotchas
- A CUD on N2 doesn't cover N4/C3 VMs you migrate to; align migrations with commitments.
- Billing export is not retroactive; enable it on day one.
- Labels on resources propagate to billing only from when they were applied.

## Verify
- [ ] CUD utilisation > 95% monthly; coverage of steady baseline reported.
- [ ] Dashboard shows < 5% unallocated spend.
