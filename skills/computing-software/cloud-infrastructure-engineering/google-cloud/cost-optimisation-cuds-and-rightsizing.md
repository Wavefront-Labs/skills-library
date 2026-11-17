---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cost-optimisation-cuds-and-rightsizing
name: cost-optimisation-cuds-and-rightsizing
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cost-optimization, cost-optimisation, committed-use-discounts, cud, spend-based-cud, resource-based-cud, flexible-cud, sustained-use-discounts, rightsizing, recommender, idle-resources, cost-controls, finops, machine-family-selection, spot-vms, autoscaling-cost, storage-cost, cost-anomaly-detection, cud-analysis]
level: practitioner
status: docs-checked
description: "Cut GCP spend in the order that pays: idle and oversized resources via Recommender, autoscaling and Spot, then resource vs spend-based CUDs."
sources: ["https://cloud.google.com/docs/cuds", "https://cloud.google.com/compute/docs/instances/committed-use-discounts-overview", "https://cloud.google.com/recommender/docs/recommenders", "https://cloud.google.com/compute/docs/sustained-use-discounts"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cost optimisation: CUDs and rightsizing

**Goal:** the bill reflects work done, not resources forgotten; commitments cover the
steady floor without stranding money; and a surprise shows up as an alert, not an invoice.

## 1. Order of operations (cheapest savings first)
1. **Delete idle**: Recommender has idle recommenders for VMs (`google.compute.instance.IdleResourceRecommender`), persistent disks (`google.compute.disk.IdleResourceRecommender`), IP addresses (`google.compute.address.IdleResourceRecommender`), custom images (`google.compute.image.IdleResourceRecommender`), reservations (`google.compute.IdleResourceRecommender`), GKE clusters and Cloud SQL instances (`google.cloudsql.instance.IdleRecommender`). Unattached disks and reserved IPs are pure waste. List with `gcloud recommender recommendations list --recommender=google.compute.instance.IdleResourceRecommender --location=<ZONE> --project=<PROJECT_ID>`.
2. **Right-size**: `google.compute.instance.MachineTypeRecommender` (VMs), `google.compute.instanceGroupManager.MachineTypeRecommender` (MIGs) and `google.cloudsql.instance.OverprovisionedRecommender` (Cloud SQL). Apply through your infrastructure code, not by hand.
3. **Schedule**: dev/test VMs off nights and weekends, dev clusters scaled down, Cloud SQL dev instances stopped.
4. **Choose the right SKU**: newer machine families are generally cheaper per unit of work than older ones; check current pricing pages rather than assuming. Use storage lifecycle rules for cold data and Standard Network Tier for bulk egress where latency allows.
5. **Elasticity**: autoscaling MIGs/GKE/Cloud Run with sane minimums, **Spot** VMs for fault-tolerant work.
6. **Commit** to what is left.

## 2. Commitments
| Type | Covers | Term | Flexibility |
|---|---|---|---|
| **Resource-based CUD** (Compute Engine) | vCPUs, memory, GPUs, local SSD, sole-tenant nodes, OS licences, Exapool block storage; a specific type and amount in a specific region | 1 year or 3 years; 3-year gives a higher discount | tied to region; shared across projects depending on the billing account's CUD sharing configuration |
| **Compute flexible CUD** (spend-based) | hourly spend on eligible Compute Engine, GKE and Cloud Run usage | 1 year or 3 years | any project or region in the billing account, no single machine configuration |
| **Service-specific spend-based CUDs** | AlloyDB, BigQuery, Bigtable, Spanner, Cloud SQL, Memorystore, and others listed on the CUDs page | 1 year or 3 years | scope differs per service (for example Cloud SQL applies in the region you purchased) |
| Sustained-use discounts | automatic, for eligible Compute Engine resources used for a large part of the month | none | automatic; see the SUD page for which machine series qualify |

- Discount rates differ by machine series, term and service and change over time: read them from the CUD pages for the series you use, and do not copy percentages into plans.
- A purchased resource-based commitment cannot be cancelled and is billed monthly until the end of the term whether or not the resources are used. A compute flexible commitment is an hourly commitment fee paid for the whole term regardless of usage.
- For memory-optimized machine series, compute flexible CUDs are available only on 3-year commitments; a 1-year flexible commitment consuming that usage gets no discount.
- Size with the CUD analysis in Cloud Billing and commit to the steady floor of usage, never to the average.
- Order: resource-based first for stable large fleets, flexible CUDs for the variable remainder.
- Track commitment utilisation in Cloud Billing and in the billing export; low utilisation means you over-committed.

## 3. Governance and visibility
- Enforce cost labels (such as cost-center, env, owner) at project creation; export billing data to BigQuery and report by label.
- **Budgets** per project with forecast thresholds, plus cost anomaly alerts for the surprises.
- FinOps cadence: monthly review of top SKUs, CUD utilisation, and the Recommender savings backlog.
- Org policy guard rails: restrict machine families and regions in non-prod; use quota caps as a backstop.

## 4. Service-specific quick wins
- **GKE**: Autopilot for spiky or small clusters, Spot node pools with taints, vertical pod autoscaler in recommendation mode, right-size resource requests.
- **Cloud Run**: raise concurrency above 1; use `min-instances` only where cold starts hurt.
- **Cloud SQL**: stop dev instances, delete old backups and replicas.
- **Logging/Monitoring**: exclusion filters and sampling for noisy logs and metrics.
- **Storage**: delete orphan snapshots; use lifecycle rules.

## Gotchas
- A 3-year commitment outlives the hardware you may want to leave. Prefer 1-year for families you may migrate off.
- Spend-based commitments cover hourly spend; bursty nightly batch does not use a flat hourly commitment well.
- Rightsizing recommendations are only as good as the metrics: VMs without the Ops Agent have no memory metric, so install it before trusting them.
- Deleting idle resources without a snapshot or export is how you learn what "idle" was hiding; snapshot first, delete after a quarantine period.

## Verify
- [ ] Recommender shows no idle VMs or disks older than your quarantine period.
- [ ] Every commitment has high utilisation; CUD analysis shows no large uncovered steady-state usage.
- [ ] Dev environments stop on schedule (the billing export shows the nightly dip).
- [ ] A cost anomaly alert fired on a deliberate test spend and reached the owner.

## Checked
2026-11-09. Confirmed against the Compute Engine CUD overview, the Google Cloud CUDs page and the Recommender recommenders table: CUD types and 1/3-year terms, resource-based eligible resources and region scope, non-cancellable monthly billing, flexible CUD coverage (Compute Engine, GKE, Cloud Run), memory-optimized 3-year-only rule, the service list for spend-based CUDs, and the recommender IDs named. Removed: discount percentages, Spot discount range, the 8-day and 95 percent figures, gcloud purchase and describe examples, cross-skill references, cost-anomaly-detection and Cost Hub specifics (page stub or unconfirmed).
Method: documentation only; no commands were run.
