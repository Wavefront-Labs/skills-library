---
id: computing-software.cloud-infrastructure-engineering.azure.storage-account-design-and-redundancy
name: storage-account-design-and-redundancy
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, storage-account, storage-accounts, redundancy, lrs, zrs, grs, gzrs, ra-grs, ra-gzrs, general-purpose-v2, premium-block-blob, premium-file-shares, page-blobs, hierarchical-namespace, data-lake-storage, adls-gen2, account-failover, scalability-targets, ingress-egress-limits, storage-naming, blob-storage, queue-storage, table-storage]
level: practitioner
status: docs-checked
description: "Choose the storage account: GPv2 vs premium block blob/file, LRS/ZRS/GRS/GZRS redundancy, hierarchical namespace, scalability limits and failover."
sources: ["https://learn.microsoft.com/azure/storage/common/storage-account-overview", "https://learn.microsoft.com/azure/storage/common/storage-redundancy", "https://learn.microsoft.com/azure/storage/common/redundancy-migration", "https://learn.microsoft.com/azure/storage/common/storage-initiate-account-failover", "https://learn.microsoft.com/azure/storage/common/scalability-targets-standard-account"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage account design — type, redundancy and limits chosen for the workload

**Goal:** an account whose SKU matches the IO pattern, whose redundancy matches the
RPO/RTO you promised, and whose limits you won't hit at 3× growth.

## 1. Account type
| Workload | Kind / SKU | Why |
|---|---|---|
| Blobs, files, queues, tables — default | **StorageV2** (GPv2), `Standard_*` | Tiers (hot/cool/cold/archive), lifecycle, all redundancy options |
| Low-latency, high-transaction-rate blobs | **BlockBlobStorage** (premium block blobs), `Premium_LRS/ZRS` | Premium performance; can't be tiered with Set Blob Tier or lifecycle management |
| SMB/NFS file shares needing premium performance | Premium file shares (**FileStorage**), `Premium_LRS/ZRS` | The premium file shares account type is the one that supports NFS in Azure Files |
| Unmanaged disks / page blobs | avoid; use managed disks | |
| Analytics (Spark, Synapse, Databricks) | GPv2 + **hierarchical namespace** (`--enable-hierarchical-namespace`) = ADLS Gen2 | Directory semantics and ACLs; check the feature support table before enabling, as some blob features (for example versioning and point-in-time restore) are unavailable on HNS accounts |
```bash
az storage account create -n stappprod001 -g rg --kind StorageV2 --sku Standard_ZRS \
  --access-tier Hot --min-tls-version TLS1_2 --allow-blob-public-access false \
  --allow-shared-key-access false --https-only true --default-action Deny --bypass AzureServices
```
Names: 3–24 characters, lowercase letters and digits only, globally unique.

## 2. Redundancy
| SKU | Copies | Survives | Notes |
|---|---|---|---|
| LRS | 3 copies in one datacenter | hardware failure within the datacenter | at least 11 nines durability over a year; dev/test, reproducible data |
| ZRS | 3 across availability zones | zone outage | for production in regions with availability zones |
| GRS / RA-GRS | LRS in primary + async copy to a secondary region | region | at least 16 nines durability; Geo priority replication targets an RPO of 15 minutes or less for block blobs; RA- adds read access to the secondary endpoint |
| GZRS / RA-GZRS | ZRS in primary + LRS in secondary | zone + region | combines zone and region protection |
- Changing redundancy follows the supported-path table in "Change the redundancy option for a storage account" (some paths are a direct update, others need a conversion request or a manual copy).
- Premium block blob accounts: LRS and ZRS only.
- The archive tier isn't supported for ZRS, GZRS or RA-GZRS accounts.

## 3. Failover
- **Customer-managed failover** is started with `az storage account failover --failover-type <planned|unplanned>`; the account must use GRS, RA-GRS, GZRS or RA-GZRS.
- **Unplanned failover** promotes the secondary and data loss should be expected (writes after the last sync time are lost); it results in the loss of the geo-redundancy configuration, and reconfiguring GRS takes extra time and cost.
- **Planned failover** waits until all data is synchronised to the secondary, preventing data loss; use it for DR drills.
- Apps: use RA-* to read from the secondary during outages; writes still need failover.

## 4. Limits that bite
Check the current scalability and performance targets for standard storage accounts and for each service before sizing; the limits are per account and per object (blob, queue, table partition, file share).
By default you can create up to 250 storage accounts per region per subscription with standard endpoints (up to 1000 with a quota increase).
Hot partitions (sequential blob names, a single queue) hit per-object limits before account limits; spread load across names. Separate accounts per workload limit blast radius.

## 5. Other create-time decisions
- Disable shared key and anonymous blob access, and set a minimum TLS version at creation (Azure Policy can enforce this).
- Routing preference: Microsoft network routing is the default; Internet routing lowers network cost (see the endpoints and routing skill).
- Infrastructure encryption and CMK: see the customer-managed-keys skill.

## Gotchas
- Some blob features (for example versioning and point-in-time restore) are unavailable on HNS accounts — check before enabling "just in case".
- `access-tier` Cool on the account makes every new blob without an explicit tier cool; early-deletion fees follow for blobs moved or deleted within 30 days.
- GRS secondary data is not readable without RA-.
- After an unplanned failover geo-redundancy is lost; reconfigure it or the account stays single-region.
- `az storage account create` without `--default-action Deny` leaves the public endpoint open to all networks.

## Verify
- [ ] `az storage account show --query "{sku:sku.name,kind:kind,hns:isHnsEnabled,tls:minimumTlsVersion,shared:allowSharedKeyAccess,public:allowBlobPublicAccess}"` matches the design.
- [ ] Load test stays within the published scalability targets at the expected peak.
- [ ] Planned failover drill (or documented reason it isn't possible) recorded with measured RTO.

## Checked

2026-10-24, against MicrosoftDocs/azure-docs (storage/common storage-account-overview, storage-redundancy, redundancy-migration, storage-initiate-account-failover, storage-failover-customer-managed-planned and -unplanned, scalability-targets-standard-account): durability (LRS 11 nines, GRS 16 nines), Geo priority replication RPO of 15 minutes or less for block blobs, ZRS-family archive restriction, `az storage account failover --failover-type planned|unplanned`, failover prerequisites and consequences, 250 accounts per region (1000 with quota increase), premium file shares and premium block blob account types. Removed unconfirmed throughput figures, queue and table rates, region-pair remarks, HNS-failover claims, large-file-share and diagnostic-log details and the 60 percent load rule.

Method: documentation only; no commands were run.
