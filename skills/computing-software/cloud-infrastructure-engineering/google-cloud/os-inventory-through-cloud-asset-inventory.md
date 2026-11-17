---
id: computing-software.cloud-infrastructure-engineering.google-cloud.os-inventory-through-cloud-asset-inventory
name: os-inventory-through-cloud-asset-inventory
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-asset-inventory, asset-os-inventory, cai-os-inventory, vm-manager, os-config, package-inventory, vulnerability-response]
level: practitioner
status: docs-checked
description: "Query installed packages and OS versions across every VM in the org via Cloud Asset Inventory os-inventory exports to BigQuery, e.g. to find hosts with a vulnerable library."
sources: ["https://cloud.google.com/asset-inventory/docs/asset-inventory-overview", "https://cloud.google.com/compute/docs/instances/os-inventory-management", "https://cloud.google.com/sdk/gcloud/reference/asset/export"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OS inventory through Cloud Asset Inventory

## 1. Prerequisite: VM Manager OS inventory
OS data exists only for VMs running the OS Config agent with inventory enabled:
```bash
gcloud compute project-info add-metadata --project=<P> --metadata=enable-osconfig=TRUE
# enable the OS Config API first (see Set up VM Manager)
# per-zone check
gcloud compute os-config inventories list --location=<ZONE> --project=<P>
gcloud compute os-config inventories describe <VM> --location=<ZONE> --view=full
```
The agent scans inventory every 10 minutes by default (`osconfig-poll-interval` metadata, in minutes). VMs without external access can use Cloud NAT or another proxy to reach external sources.

## 2. Query org-wide
```bash
gcloud asset list --project=<P> --content-type=os-inventory \
  --asset-types=compute.googleapis.com/Instance --format=json
gcloud asset export --organization=<ORG_ID> --content-type=os-inventory \
  --asset-types=compute.googleapis.com/Instance \
  --bigquery-table=projects/<SEC_P>/datasets/cai/tables/os_inventory --output-bigquery-force
```
Then query the table in BigQuery, for example to find hosts with a vulnerable package. Inspect the exported schema once with `bq show --schema` before writing the query: the package fields differ per package manager.

## 3. OS version census
The OS info fields (`longName`, `kernelVersion`, `osconfigAgentVersion`, `updateTime`) per VM can feed a
dashboard to find end-of-life images and agents that stopped reporting.

## Gotchas
- VMs without the OS Config agent and inventory enabled have no OS inventory data.
- Cloud Asset Inventory exports are point-in-time snapshots (`--snapshot-time`), so schedule repeated exports for trending.

## Verify
- [ ] Count of instances in `os_inventory` ≈ running VMs with `enable-osconfig=TRUE`.
- [ ] A test VM with a known package version appears in the exported table.

## Checked
2026-10-27. Confirmed against the Cloud Asset Inventory overview (OS_INVENTORY content type, os-inventory), gcloud asset list and asset export reference pages (content types, --asset-types, --bigquery-table, --output-bigquery-force, --snapshot-time), the OS inventory management and view-os-details pages (enable-osconfig metadata, osconfig-poll-interval, 10-minute default scan, --view=full, OS info fields) and gcloud os-config inventories list and describe (--location with a zone, --view). Removed: containeranalysis API, VM service-account and Private Google Access claims, the jq path and the SQL query with guessed column paths, GKE container coverage claim, join-against-resource tip.
Method: documentation only; no commands were run.
