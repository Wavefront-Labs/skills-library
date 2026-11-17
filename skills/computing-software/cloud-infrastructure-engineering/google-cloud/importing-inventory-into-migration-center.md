---
id: computing-software.cloud-infrastructure-engineering.google-cloud.importing-inventory-into-migration-center
name: importing-inventory-into-migration-center
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, migration-center, migration-center-import, rvtools-import, csv-import, discovery-client, assessment]
level: practitioner
status: draft
description: "Load on-prem inventory into Migration Center from RVTools exports, CSV templates or the discovery client, fix import errors, and group assets for TCO and wave reports."
sources: ["https://cloud.google.com/migration-center/docs/import-data", "https://cloud.google.com/migration-center/docs/import-data-rvtools", "https://cloud.google.com/migration-center/docs/discovery-client"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Importing inventory into Migration Center

## Options
| Source | Effort | Data quality |
|---|---|---|
| **RVTools** export (VMware) | minutes | config only (vCPU, RAM, disks, OS); no utilisation over time |
| **CSV templates** (machine info, disks, perf, tags) | manual prep | as good as your CMDB |
| **Discovery client** (agentless collector VM) | install + creds | config + performance time series, dependencies |
| Third-party (StratoZone exports, Cloudamize etc.) | varies | varies |

## RVTools
1. Run RVTools against vCenter, **Export all to xlsx**.
2. Migration Center → Data import → Add data → **RVTools (XLSX)** upload.
3. Validation shows rejected rows (missing OS, duplicate VM names). Fix in the sheet or ignore templates/powered-off VMs.

## CSV
Download templates (`vmInfo.csv`, `diskInfo.csv`, `perfInfo.csv`, `tagInfo.csv`). Required columns
include MachineId, MachineName, PrimaryIPAddress, OS name, CPU cores, MemoryGiB. Performance CSV
with timestamps lets rightsizing use real utilisation.

## Discovery client
Deploy the collector VM on-prem with read-only vCenter / OS credentials; it streams inventory and
utilisation (minimum ~1 week recommended, 30 days better) and network dependencies.

## After import
- Create **groups** (by application/wave via tags) and **preference sets** (region, machine series,
  sole-tenant, licence options, Spot/CUD pricing).
- Generate TCO / pricing reports per group; export to Sheets/CSV.

## Gotchas
- Without perf data, rightsizing assumes allocated = used: estimates are high.
- Duplicate assets from multiple sources: pick one source of truth per asset or merge.
- Imports and reports are per Migration Center project and region (data location setting).

## Verify
- [ ] Asset count matches vCenter (minus excluded); a group report produces a monthly cost estimate.
