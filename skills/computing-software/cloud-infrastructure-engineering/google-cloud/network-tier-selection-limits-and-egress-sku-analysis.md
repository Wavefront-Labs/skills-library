---
id: computing-software.cloud-infrastructure-engineering.google-cloud.network-tier-selection-limits-and-egress-sku-analysis
name: network-tier-selection-limits-and-egress-sku-analysis
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, network-service-tiers, set-network-tier, project-default-tier, standard-tier-limitations, egress-cost-analysis, network-sku-analysis, billing-export]
level: practitioner
status: docs-checked
description: "Set Premium or Standard network tier per project and resource, know Standard Tier limits, and analyse egress cost by SKU in the billing export."
sources: ["https://cloud.google.com/network-tiers/docs/overview", "https://cloud.google.com/network-tiers/docs/set-network-tier", "https://cloud.google.com/billing/docs/how-to/export-data-bigquery-tables/standard-usage"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network tier selection, limits and egress SKU analysis

## 1. Set the tier
```bash
gcloud compute project-info update --project=<PROJECT_ID> --default-network-tier=STANDARD      # new resources only
gcloud compute addresses create <ADDRESS_NAME> --region=<REGION> --network-tier=STANDARD
gcloud compute instances create <INSTANCE_NAME> --zone=<ZONE> --network-tier=STANDARD
```
The project default tier is PREMIUM and applies only to newly created eligible resources that do not set a tier; changing it does not change existing resources. You choose a tier per resource (external IP address, forwarding rule, VM). For load balancers, an existing one is switched by deleting the forwarding rule and creating a new one with a Standard Tier IP address. Premium and Standard use separate pools of external IP addresses, so an address cannot simply change tier in place.

## 2. Standard Tier limitations
- **Regional only**: Standard Tier routes traffic over the public internet and uses Google's network only up to the peering point near the data centre, so distant users can see more hops and latency.
- Classic Application Load Balancers and classic proxy Network Load Balancers on Standard Tier need a single region with a regional IP and regional forwarding rule; Standard Tier removes their multi-region operation. Cloud CDN is always Premium Tier.
- Standard Tier is available to resources using regional external IP addresses in all regions. For Cloud Storage buckets as load balancer backends, the bucket must be in the same region as the forwarding rule; multi-regional buckets need Premium Tier.
- Google's guidance: Premium Tier to optimise for performance, Standard Tier to optimise for cost; if unsure, choose Premium (the default).

## 3. Egress analysis
```sql
SELECT sku.description, service.description AS service, project.id AS project,
       SUM(usage.amount_in_pricing_units) AS gib, SUM(cost) AS cost
FROM `<P>.billing.gcp_billing_export_v1_<ID>`
WHERE usage_start_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
  AND (LOWER(sku.description) LIKE '%egress%' OR LOWER(sku.description) LIKE '%network%')
GROUP BY 1, 2, 3 ORDER BY cost DESC LIMIT 50
```
Read SKU names for tier (Premium vs Standard), destination and source service, and compare them with the rows on the VPC network pricing page. Load balancers, Cloud NAT and protocol forwarding can add data-processing charges even for inbound traffic.

## Gotchas
- Changing the project default tier does not change existing IPs or load balancers: inventory and migrate deliberately.
- Standard Tier is regional only, so plan before choosing a tier for front ends.
- Cloud CDN and some interconnect and peering traffic have their own pricing, not the standard internet egress rates.

## Verify
- [ ] Top-10 egress SKUs and owners reviewed monthly.
- [ ] Standard Tier SKUs appear in the billing export for the workloads you moved.

## Checked
2026-11-09. Confirmed in the Network Service Tiers overview and set-network-tier pages (default PREMIUM, project default affects only new resources, per-resource tier, separate IP pools, Standard Tier regional-only behaviour, Cloud CDN always Premium, Cloud Storage backend rule, gcloud flags) and the VPC network pricing page (inbound processing charges for load balancers, Cloud NAT, protocol forwarding). BigQuery functions in the query are standard SQL; billing-export column names follow the Standard usage cost export page. Removed: claim that Standard Tier is unavailable in some regions (the page says all regions), cross-zone and replication surprises, CDN cheaper claim, and the lower-$/GiB check.
Method: documentation only; no commands were run.
