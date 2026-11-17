---
id: computing-software.cloud-infrastructure-engineering.azure.disaster-recovery-for-non-paired-regions
name: disaster-recovery-for-non-paired-regions
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, bcdr-design, non-paired-regions, region-pairs, geo-replication, availability-zones]
level: advanced
status: docs-checked
description: "Plan DR when your region has no pair or you choose a non-paired target: which services need explicit replication, GRS limitations, and architecture choices."
sources: ["https://learn.microsoft.com/azure/reliability/regions-paired", "https://learn.microsoft.com/azure/reliability/availability-zones-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DR for non-paired regions

**Goal:** get cross-region resilience in regions without an Azure pair or when data residency forces a different target.

## What pairing gives you (and what you lose)
Microsoft documents that you can build a resilient solution with paired regions, nonpaired regions or a mix. Pairing
provides: some services (for example geo-redundant storage, GRS) replicating to the pair, one region of each pair
prioritised for recovery in a geography-wide outage, and planned platform updates staggered across the pair.
Backup's Cross Region Restore restores to the paired secondary region. In a nonpaired region none of this is implied:
you choose the target and build each replication path yourself.

## Service-by-service approach
| Service | Approach when there is no pair |
|---|---|
| Storage | Do not assume GRS to a pair: check the redundancy options offered for the account's region, otherwise copy data to an account in your chosen region with your own job |
| Azure SQL, Cosmos DB | Their geo-replication features name a target region explicitly: check each service's page for region limits |
| Key Vault | Do not assume automatic replication: back up and restore secrets/keys into a vault in the DR region |
| Azure Backup | Cross Region Restore targets the paired region: confirm availability for your region, otherwise plan a second vault in the DR region |
| Site Recovery | Choose the target region explicitly and verify support for your source and target |
| AKS/App Service | Nothing automatic: deploy a second stamp from IaC |

## Design steps
1. Decide RTO/RPO per workload; zone redundancy may satisfy many requirements alone.
2. Pick a DR region inside the data-residency geography with the needed services and SKU capacity.
3. Implement replication explicitly for each data store; document what is not replicated.
4. Global routing (Front Door/Traffic Manager) with priority failover.
5. Check quota and capacity in the DR region before you need it.

## Verify
- [ ] Table of every data store with its replication mechanism and tested restore/failover result.

## Checked
2026-10-28. Confirmed against the Azure region pairs page (Learn: reliability/regions-paired): pairs and nonpaired regions
both supported, GRS as a pair-based example, prioritised recovery, staggered updates, Cross Region Restore to the paired
region. Removed: claims that Key Vault auto-replicates to the pair, Managed HSM multi-region replication, object replication
as the Storage substitute, per-service "any region" behaviour and capacity-reservation advice (none confirmed in the fetched pages).
Dead source regions-nonpaired (404) dropped.
Method: documentation only; no commands were run.
