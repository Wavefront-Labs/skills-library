---
id: computing-software.cloud-infrastructure-engineering.terraform.restoring-state-from-gcs-versioning-and-azure-snapshots
name: restoring-state-from-gcs-versioning-and-azure-snapshots
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, gcs-versioning, blob-snapshot, state-recovery, gcs-backend, azurerm-backend]
level: practitioner
status: docs-checked
description: "Restore a previous Terraform state from GCS object versioning or Azure blob versions and snapshots: listing generations, restoring, lock handling and verification."
sources: ["https://cloud.google.com/storage/docs/using-versioned-objects", "https://learn.microsoft.com/en-us/azure/storage/blobs/versioning-enable", "https://developer.hashicorp.com/terraform/cli/commands/state/push"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Restoring state from GCS and Azure versioning

## GCS (object versioning must be enabled beforehand)
```bash
# list generations of the state object
gcloud storage ls --all-versions gs://corp-tfstate/payments/default.tfstate
# gs://corp-tfstate/payments/default.tfstate#<GENERATION>
# download the good version
gcloud storage cp gs://corp-tfstate/payments/default.tfstate#<GENERATION> good.tfstate
jq '.serial, .lineage' good.tfstate
```
Google's doc restores a noncurrent version by copying it over the live object
(`gcloud storage cp gs://BUCKET/OBJECT#GENERATION gs://BUCKET`), which works without
Terraform. To push it through Terraform instead:
```bash
terraform state push good.tfstate               # add -force only if the safety checks block you
```
`state push` refuses a state whose `lineage` differs, or whose `serial` is lower than the
destination's; `-force` disables both checks and overwrites the destination state.

## Azure Blob
Enable **blob versioning** on the state storage account (Microsoft Learn: "Enable and manage
blob versioning"); with versioning on, you can restore an earlier version of a blob.
```bash
az storage blob list --account-name sttfstate -c tfstate --include v \
  --prefix payments/prod.tfstate --auth-mode login \
  --query "[].{v:versionId, t:properties.lastModified, cur:isCurrentVersion}" -o table
az storage blob download --account-name sttfstate -c tfstate -n payments/prod.tfstate \
  --version-id "2026-10-17T09:10:11.1234567Z" -f good.tfstate --auth-mode login
terraform state push good.tfstate        # add -force only if lineage or serial checks block you
```
`az storage blob snapshot` takes a snapshot of a blob; consider one before risky state surgery.

## Before pushing
- Lock: no runs in progress (pause pipelines).
- Compare `lineage` with the current state; `state push` refuses a different lineage
  unless `-force` is given, because it suggests completely different states.
- Back up the current (bad) state too.

## After
`terraform plan`; resources created after the restored version will show as new
(import them), resources deleted since will show as deleted outside Terraform.

## Verify
- [ ] `terraform state pull` content matches the good version you pushed.
- [ ] Plan reconciled with imports/no unexpected creates.

## Checked
- 2026-10-28. Confirmed against the Google Cloud "Use versioned objects" page (`gcloud storage ls --all-versions`, `OBJECT#GENERATION` syntax, restore with `gcloud storage cp`), the Microsoft Learn blob versioning page, the Terraform `state push` page (`lineage` and `serial` checks, `-force` behaviour) and the command checker for the `gcloud storage` and `az storage blob` commands (list with `--include`, download with `--version-id`, snapshot).
- Removed: the `gcloud storage ls -a` shorthand, the `gcloud storage cat` inspection, the claim that `state push` applies locking, the claim that copying over the live object bypasses the lock, soft delete, manual-copy wording for snapshots and the serial-increases check (not in the fetched docs).
Method: documentation only; no commands were run.
