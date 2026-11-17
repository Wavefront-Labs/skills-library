---
id: computing-software.cloud-infrastructure-engineering.azure.storage-account-default-access-tier-choice-and-changes
name: storage-account-default-access-tier-choice-and-changes
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, blob-storage, account-access-tier, default-tier-change, inferred-tier, access-tiers]
level: practitioner
status: docs-checked
description: "Pick a storage account's default access tier and change it safely: inferred vs explicit tiers, the cost of switching every inferred blob, and better alternatives."
sources: ["https://learn.microsoft.com/azure/storage/blobs/access-tiers-overview", "https://learn.microsoft.com/azure/storage/blobs/access-tiers-online-manage", "https://learn.microsoft.com/azure/storage/blobs/access-tiers-best-practices"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Default access tier: choose and change

**Goal:** set the right default tier up front and avoid a surprise bill from flipping it later.

## How the default works
- General-purpose v2 / Blob Storage accounts have a default access tier (Hot, Cool or Cold; the archive tier can't be the default).
- Blobs uploaded without a tier get the default as an **inferred** tier (shown as inferred, for example Hot (inferred), in the portal).
- Blobs with an explicit tier (set at upload, Set Blob Tier, or lifecycle) keep it when the default changes.
- Premium block blob accounts can't be tiered with Set Blob Tier or lifecycle management.

## Choosing
- Hot default: active workloads, unpredictable reads; higher storage, lower access costs.
- Cool default: backup/archive-like workloads where nearly everything is written once, rarely read
  (30-day minimum, early deletion charges, higher read costs).
- Most estates: keep Hot default, tier explicitly with lifecycle rules or set tier at upload for known-cold data.

## Changing the account default
```bash
az storage account show -g rg -n st --query accessTier
az storage account update -g rg -n st --access-tier Cool
```
- Every blob with an **inferred** tier changes tier: on a general-purpose v2 account, switching to a cooler default is billed as write operations (per 10,000) for those blobs;
  switching to a warmer default is billed as read operations (per 10,000) plus data retrieval (per GB). On accounts with millions of blobs this can be a large one-off cost.
- Estimate first: count the blobs whose tier is inferred (blob inventory reports can help).

## Alternatives to a default change
- Lifecycle rule targeting specific prefixes/age.
- Set tier at upload in the app (for example the `--tier` option on upload).
- Separate accounts (or containers with lifecycle filters) for hot and cold data.

## Gotchas
- Archive can't be the default tier.
- The default tier change applies only to blobs whose access tier hasn't been explicitly set.

## Verify
- [ ] Inventory report before/after shows expected tier distribution; cost analysis shows the one-off transaction spike was anticipated.

## Checked

2026-10-24, against MicrosoftDocs/azure-docs (storage/blobs/access-tiers-overview, access-tiers-online-manage, access-tiers-best-practices): default tier options (Hot, Cool, Cold), archive not allowed as default, inferred-tier behaviour, billing of default-tier changes on general-purpose v2 accounts (write operations when cooler, read operations plus retrieval when warmer), premium block blob accounts not tierable, 30-day Cool minimum, `az storage account update --access-tier`. Removed the unconfirmed inventory field name, SDK option name, early-deletion remark on default changes and the minimum-duration clock statement.

Method: documentation only; no commands were run.
