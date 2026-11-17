---
id: computing-software.cloud-infrastructure-engineering.google-cloud.carbon-footprint-and-sustainability
name: carbon-footprint-and-sustainability
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, sustainability, carbon-footprint, low-carbon-regions, carbon-free-energy, cfe-percent, grid-carbon-intensity, carbon-footprint-export, scope-3-emissions, green-software, region-picker, carbon-aware-scheduling, unattended-project-recommender, sustainability-reporting, ghg-protocol]
level: practitioner
status: draft
description: "Measure and reduce GCP carbon: Carbon Footprint reports and BigQuery export, low-carbon region choice with the region picker, carbon-aware batch scheduling, idle cleanup that cuts CO2e and cost."
sources: ["https://cloud.google.com/carbon-footprint/docs/overview", "https://cloud.google.com/carbon-footprint/docs/export", "https://cloud.google.com/sustainability/region-carbon", "https://cloud.google.com/architecture/framework/sustainability", "https://cloud.google.com/carbon-footprint/docs/methodology", "https://cloud.google.com/recommender/docs/unattended-project-recommender"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Carbon footprint and sustainability

**Goal:** the organisation can report cloud emissions per team with a defensible methodology,
and the easy reductions — region choice, idle cleanup, batch timing — are done because they also save money.

## 1. Measure
- **Carbon Footprint** (console → Carbon Footprint, per billing account): monthly gross **location-based** and **market-based** emissions (tCO2e) by project, service, region; scope 1, 2 and 3 per the GHG Protocol, methodology published (includes Google's data-centre overhead and hardware embodied emissions).
- Export to BigQuery for allocation to teams: Carbon Footprint → Export → dataset; table `carbon_footprint` with `usage_month`, `project.id`, `service.description`, `location.region`, `carbon_footprint_kgCO2e.scope1/2/3`, `carbon_model_version`. Join with the billing export on project/label for per-cost-centre reports.
```sql
SELECT usage_month, project.id, service.description,
       ROUND(SUM(carbon_footprint_total_kgCO2e.location_based),1) AS kg_loc,
       ROUND(SUM(carbon_footprint_total_kgCO2e.market_based),1)   AS kg_mkt
FROM `prj-c-billing.carbon.carbon_footprint`
WHERE usage_month >= DATE_SUB(DATE_TRUNC(CURRENT_DATE(), MONTH), INTERVAL 12 MONTH)
GROUP BY 1,2,3 ORDER BY kg_loc DESC;
```
- Data lands ~15th of the following month; the model version changes yearly (restated history), so report by `carbon_model_version`.
- `roles/billing.carbonViewer` for the dashboard/export.

## 2. Reduce: region choice (the biggest lever)
- Google publishes per-region **carbon-free energy % (CFE)** and **grid carbon intensity (gCO2e/kWh)**; the console marks regions with a leaf icon ("Low CO2") when CFE ≥ 75 % or intensity ≤ 200 gCO2e/kWh. The **region picker** tool trades carbon, price and latency.
- For new workloads without latency/residency constraints, prefer low-carbon regions (e.g. `europe-north1`, `europe-west9`, `northamerica-northeast1`, `us-central1` ranks well; check the current table — it moves yearly).
- Org policy `gcp.resourceLocations` can allow-list low-carbon regions for folders where that is acceptable (dev/test, batch, analytics) — it is the only way to make the default stick.
- Data residency and DR requirements win over carbon; document the trade-off per folder.

## 3. Reduce: use less
- **Idle cleanup**: the Unattended Project Recommender (`google.resourcemanager.projectUtilization.Recommender`) flags projects with no activity; idle VM/disk/IP recommenders — removing them cuts emissions and cost together (see `cost-optimisation-cuds-and-rightsizing`).
- **Elasticity**: scale-to-zero (Cloud Run, Autopilot, scheduled VM stop) — an idle VM at 5 % CPU still has ~30-60 % of its peak power draw.
- **Right-size** and **newer hardware** (C3/N4/Tau/Arm T2A: more work per watt); Spot capacity uses otherwise-idle machines.
- **Batch timing**: shift flexible jobs (Dataflow FlexRS, Batch, nightly ETL) to low-carbon hours/regions; Google's own *carbon-intelligent computing* does this for internal workloads — you can approximate with a Cloud Scheduler window per region's cleaner hours or by routing Batch to the cleaner region.
- **Storage**: Autoclass/lifecycle to colder classes, delete snapshots and buckets nobody reads; data has a footprint even at rest.
- **Managed over self-managed**: Spanner/BigQuery/Cloud Run share hardware at higher utilisation than a dedicated VM fleet.

## 4. Report
- Monthly dashboard: tCO2e by team (labels), trend vs baseline, intensity metric (kgCO2e per unit of business work or per $), % of compute in low-carbon regions, idle-resource backlog.
- For corporate reporting: Carbon Footprint data is designed for GHG Protocol Scope 3 category 1 (purchased services) in your own inventory; Google's "24/7 CFE by 2030" commitment and region CFE data support market-based claims — keep the export and methodology version as evidence.
- Compute Engine and other services also expose energy/carbon in Active Assist's sustainability hub with recommendations and estimated savings.

## Gotchas
- Location-based vs market-based numbers differ a lot (Google's PPAs); pick one for targets and state it.
- Moving data between regions to "go greener" costs egress and may violate residency; evaluate end to end.
- The leaf icon threshold is a snapshot; a region can lose it when grids change — review annually.
- Carbon export covers Google Cloud only; Workspace and Marketplace SaaS are not included.
- Small absolute numbers tempt "nothing to do"; the useful signal is **intensity per unit of work** and the idle share, not the total.

## Verify
- [ ] Carbon Footprint export populated for the last 12 months; team-level report joins billing labels with < 5 % unallocated emissions.
- [ ] `gcp.resourceLocations` on the dev/analytics folders allows only leaf-marked regions, and new resources there land in them.
- [ ] Idle-project and idle-VM recommendations are under a set backlog; last quarter's cleanup is visible as a drop in location-based kgCO2e.
- [ ] One flexible batch workload runs in a low-carbon region/window and its emissions per run are lower than before (export shows it).
