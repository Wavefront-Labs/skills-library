---
id: computing-software.cloud-infrastructure-engineering.azure.azure-artifacts-storage-limits-and-billing
name: azure-artifacts-storage-limits-and-billing
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-artifacts, artifacts-storage, artifacts-billing, retention-policies, feed-cleanup]
level: practitioner
status: docs-checked
description: "Manage Azure Artifacts storage: free 2 GiB allowance, billing, per-feed retention policies, deleting packages and recycle bin, and finding big consumers."
sources: ["https://learn.microsoft.com/azure/devops/artifacts/start-using-azure-artifacts", "https://learn.microsoft.com/azure/devops/artifacts/how-to/delete-and-recover-packages", "https://learn.microsoft.com/azure/devops/artifacts/artifact-storage"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure Artifacts storage and billing

**Goal:** keep Artifacts storage under budget without breaking builds that pin old versions.

## Billing model
- Every organisation gets **2 GiB free** Artifacts storage. Once it is reached you cannot publish new artifacts until you delete some or set up billing to increase the limit (Azure DevOps billing needs an Azure subscription connected).
- All package types (npm, NuGet, Python, Maven, Cargo, Universal) count toward billed storage, as do packages saved from upstream sources. Pipeline Artifacts and Pipeline Caching do not.
- Packages in the recycle bin still count until they are permanently deleted.
- Removing the Azure subscription from the organisation while over 2 GiB leaves packages read-only.
- Storage is shown in whole GiB (under 1 GiB displays as 0) and metrics update within about 24 hours, sometimes up to 48.

## See usage
The organisation-level and project-level storage views show total usage by artifact type and by project.

## Reduce
1. **Retention policy** per feed: *Enable package retention*, *Maximum number of versions per package* and *Days to keep recently downloaded packages*. Packages promoted to a **view** are exempt from retention policies.
2. Delete unneeded packages and versions manually, or unlist/deprecate/yank where a package type supports it.
3. Empty the **recycle bin**: deleted packages stay there 30 days before permanent deletion, and can be removed earlier by deleting them from the recycle bin.
4. Remove stale feeds and upstream-cached packages.

## Gotchas
- Deleted versions are permanently gone after the recycle bin period; builds pinning them fail. Promote releases to a view first.
- Once a version is published, its version number stays permanently reserved: you cannot modify that version or reuse the number for a new package, even after deletion.
- Metrics lag, so a freshly freed quota may not allow publishing for up to a day or two.

## Verify
- [ ] Storage usage is below the limit you pay for; every feed has a retention policy.

## Checked

Method: docs-checked 2026-11-09 against https://learn.microsoft.com/azure/devops/artifacts/artifact-storage (read the FAQ, size limits and increase-limit sections), https://learn.microsoft.com/azure/devops/artifacts/how-to/delete-and-recover-packages (retention, recycle bin, unlist and reserved version numbers) and the start-using-azure-artifacts page (2 GiB free). Dropped the removed set-up-retention-policies page (404) and the billing-setup page (not read), and unconfirmed claims: per-GiB tier pricing, REST delete URL, npm unpublish, and menu paths.
