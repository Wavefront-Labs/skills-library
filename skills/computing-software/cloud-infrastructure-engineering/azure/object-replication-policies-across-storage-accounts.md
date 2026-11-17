---
id: computing-software.cloud-infrastructure-engineering.azure.object-replication-policies-across-storage-accounts
name: object-replication-policies-across-storage-accounts
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, object-replication, object-replication-policy, blob-replication, cross-region-replication, priority-replication]
level: practitioner
status: docs-checked
description: "Set up blob object replication between storage accounts: prerequisites, policy and rules with prefix filters, cross-tenant settings, replication status and lag monitoring."
sources: ["https://learn.microsoft.com/azure/storage/blobs/object-replication-overview", "https://learn.microsoft.com/azure/storage/blobs/object-replication-configure", "https://learn.microsoft.com/azure/storage/blobs/object-replication-priority-replication"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Object replication policies across accounts

**Goal:** asynchronously copy block blobs from a source container to a destination container in
another account/region (DR copy, data distribution, compute near users) with known lag.

## Prerequisites
- Source and destination: general-purpose v2 or premium block blob accounts; **versioning** on both; **change feed** on source. Block blobs only (no append or page blobs).
- Not supported on accounts with a hierarchical namespace (ADLS Gen2).
- Versioning cannot be disabled while an object replication policy exists on the account.
- Read and delete operations on the destination container are permitted while the policy is active.

## Create
```bash
az storage account or-policy create -g rg-dst --account-name stdst \
  --source-account stsrc --destination-account stdst \
  --source-container data --destination-container data-replica \
  --min-creation-time '2026-10-01T00:00:00Z' --prefix-match reports/ images/
```
CLI creates the policy on the destination then you apply the returned policy (with `policyId`
and `ruleId`) to the source:
```bash
az storage account or-policy show -g rg-dst --account-name stdst --policy-id <id> > policy.json
az storage account or-policy create -g rg-src --account-name stsrc -p @policy.json
```
Limits: a source account replicates to at most two destination accounts (one policy per destination), an account can be the destination of at most two policies, and a policy holds up to 1,000 rules (each source and destination container in only one rule). Rules can filter by prefix. With no `--min-creation-time` only blobs created after the rule are copied; `1601-01-01T00:00:00Z` copies existing blobs too.

## Cross-tenant
Cross-tenant replication is permitted by default for a storage account. To prevent it, set the account's `AllowCrossTenantReplication` property to false (not permitted while the account takes part in a cross-tenant policy: delete those policies first).

## Monitor
- Per-blob status: `az storage blob show ... --query 'objectReplicationSourceProperties[].rules[].status'` (the portal shows Complete once a blob has replicated).
- Metrics: *Operations pending for replication* and *Bytes pending for replication*, emitted per time bucket.
- **Priority replication** (opt-in, billed separately; see the pricing page) comes with an SLA: 99.0% of objects within 15 minutes when source and destination are in the same continent, for eligible workloads.
- Without priority replication, latency depends on blob size.

## Gotchas
- A delete on the source turns the current version into a previous version and that state replicates to the destination; previous versions are preserved.
- Archived blobs (source or destination) cannot be replicated.
- Snapshots are not replicated; replication works on versions.
- A destination version with an active version-level immutability policy can make replication of a source delete or update fail.
- Not a backup: a bad overwrite at the source replicates.

## Verify
- [ ] Upload a canary blob to a replicated prefix; it appears in destination and source shows `Complete`.
- [ ] Alert on pending-replication metrics above threshold.

## Checked
2026-10-27. Confirmed against Learn: object replication overview (prerequisites, limits, delete and snapshot behaviour, cross-tenant default, metrics), configure object replication, priority replication, and the az storage account or-policy CLI reference (flags matched).
Corrected: the destination is not read-only for reads and deletes; source deletes do replicate as a version change; cross-tenant replication is permitted by default.
Removed (unconfirmed): five-prefix limit, tier-change note, CMK note, lag-in-hours claim.
Method: documentation only; no commands were run.
