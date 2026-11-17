---
id: computing-software.cloud-infrastructure-engineering.azure.data-residency-and-region-selection
name: data-residency-and-region-selection
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, data-residency, region-selection, data-sovereignty, gdpr, eu-data-boundary, allowed-locations-policy, paired-regions, geo-redundant-storage, availability-zones, sovereign-cloud, compliance]
level: advanced
status: docs-checked
description: "Choose Azure regions under data residency rules: where each service stores and replicates data, EU Data Boundary, paired-region effects, allowed-locations policy and evidence."
sources: ["https://learn.microsoft.com/en-us/azure/reliability/cross-region-replication-azure", "https://azure.microsoft.com/en-us/explore/global-infrastructure/data-residency/", "https://learn.microsoft.com/en-us/privacy/eudb/eu-data-boundary-learn", "https://learn.microsoft.com/en-us/azure/governance/policy/samples/built-in-policies", "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-setup-guide/regions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data residency and region selection

**Goal:** a primary and DR region choice you can defend to an auditor: customer data stays in
the permitted geography at rest, in backups and in replicas, and Policy prevents drift.

## 1. Gather the constraint
- Legal requirement in words: "personal data of UK customers stored in the UK", "EU only",
  "no transfer outside country X". Distinguish **at rest**, **in processing**, and **support access**.
- Classify the data each workload holds; residency typically applies to customer content,
  not to telemetry about the platform.

## 2. Pick regions
Score candidate regions on: in-geography for residency; **availability zones** present;
service availability (`az provider show -n Microsoft.Web --query "resourceTypes[?resourceType=='sites'].locations"`
or the *Products by region* page); capacity/quota for required SKUs; latency to users; price.
- **Paired regions**: check the region pair (and whether the region has one) on the cross-region replication page before relying on geo-redundancy.
- Prefer zone-redundant in one region plus a deliberate DR region, rather than defaulting to the pair.

## 3. Where data actually goes
| Feature | Residency effect |
|---|---|
| Geo-redundant storage and backup options | replicate to a secondary region; pick a local or zone-redundant option if that region is out of bounds |
| Cosmos DB, SQL geo-replicas | wherever **you** add a region |
| Azure CDN, Microsoft Entra ID | CDN caches at edge locations around the world; Entra ID is a non-regional service (see the global infrastructure data residency page) |
- **EU Data Boundary**: see the EU Data Boundary page for what it covers and the service-specific exclusions.
- Sovereign needs beyond that: see the Azure sovereign cloud offerings and customer-managed key options in the sources.

## 4. Enforce and prove
```bash
az policy assignment create -n allowed-locations --scope <mg-id> --policy <allowed-locations-definition-id> --params '{"listOfAllowedLocations":{"value":["uksouth","ukwest"]}}'
```
Look up the built-in *Allowed locations* and *Allowed locations for resource groups* definition IDs in the built-in policies list and assign both.
- Test global resource types (Front Door, DNS) against the allowed-locations policy before enforcing it.
- Add deny/audit policies for geo-redundant storage SKUs and GRS backup where the pair is out of scope.
- Evidence: Resource Graph query of all resource `location`s and storage SKU per subscription, exported monthly.

## Gotchas
- Backups and DR copies are the usual breach of residency, not the primary database.
- Changing a region later is a migration, not a setting; data move tools differ per service.

## Verify
- [ ] Written residency requirement mapped to chosen primary/DR regions and to each data store's redundancy setting.
- [ ] Allowed-locations policies assigned at the landing-zone MG; compliance shows no non-compliant resources.
- [ ] ARG export shows no storage/backup redundancy that replicates outside the permitted geography.

## Checked
2026-10-28. Confirmed: `az provider show --namespace Microsoft.Web --query "resourceTypes[?resourceType=='sites'].locations"` pattern (resource providers page); CDN edge caching and Entra ID as a non-regional service (global infrastructure page); `az policy assignment create` flags passed the CLI reference check.
Removed (not confirmed): paired-region examples, the `--backup-storage-redundancy` value, Azure OpenAI/Log Analytics/Service Bus rows, EU Data Boundary scope wording, built-in policy GUIDs, the `global` exclusion claim, and the preview-feature gotcha.

Method: documentation only; no commands were run.
