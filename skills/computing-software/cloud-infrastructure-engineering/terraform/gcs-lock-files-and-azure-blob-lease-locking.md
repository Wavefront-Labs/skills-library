---
id: computing-software.cloud-infrastructure-engineering.terraform.gcs-lock-files-and-azure-blob-lease-locking
name: gcs-lock-files-and-azure-blob-lease-locking
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, blob-lease, gcs-lock, state-locking, gcs-backend, azurerm-backend]
level: practitioner
status: docs-checked
description: "How the gcs and azurerm backends handle state locking, the roles they document, and how to clear a stuck lock with force-unlock, with the manual fallbacks marked as last resort."
sources: ["https://developer.hashicorp.com/terraform/language/backend/gcs", "https://developer.hashicorp.com/terraform/language/backend/azurerm", "https://learn.microsoft.com/en-us/rest/api/storageservices/lease-blob"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Locking on GCS and Azure Storage

Both backends support state locking natively; no extra table.

## GCS
- The backend stores state as an object under the configured `prefix`; workspace states
  are `<prefix>/<name>.tfstate`. Enable Object Versioning on the bucket for recovery.
- Credentials must have the Storage Object Admin role on the bucket (documented for the
  `credentials` argument).
- Note the compatibility promises page lists `gcs` as maintained by outside contributors.

Stuck lock:
```bash
terraform force-unlock <LOCK_ID>          # preferred; the ID is printed in the lock error
```
The lock object's name and format are not documented on the backend page. If force-unlock
fails, list the bucket prefix, read the object that is not the `.tfstate`, and delete it
only after confirming no run is active.

## Azure Storage (azurerm)
- The backend page says it supports state locking and consistency checking with Azure
  Blob Storage native capabilities. Azure blob leases lock a blob for write and delete
  operations; a lease can last 15 to 60 seconds or be infinite (`x-ms-lease-duration: -1`).
- Documented least-privilege role for the container: Storage Blob Data Contributor.

Stuck lock:
```bash
terraform force-unlock <LOCK_ID>
```
If a lease is left behind, break it with Azure's break-lease operation (see the Lease Blob
API page: a break ends the lease, but another client cannot acquire a new one until the
break period has expired). Only do this when no run is active.

## Common issues
| Symptom | Likely cause |
|---|---|
| Lock error naming another run | Another run holds the lock or a crash left it |
| Authorization error on lock | The identity can read but lacks the role the backend page lists |
| Workspace switching shows "locked" for another workspace | Each workspace has its own state and lock |

## Verify
- [ ] Concurrent plan in a second terminal shows the lock error with the first run's ID.
- [ ] After a normal run, `terraform plan` acquires the lock without waiting.

## Checked
Date: 2026-10-28.
Confirmed: GCS backend page (state object `<prefix>/<name>.tfstate`, locking supported, Storage Object Admin role, Object Versioning advice); azurerm backend page (native locking, Storage Blob Data Contributor); Lease Blob page (lease lock for write and delete, 15 to 60 seconds or infinite, break semantics); compatibility promises page (gcs maintained by outside contributors).
Removed as unconfirmed: the `.tflock` object name and generation precondition, per-permission list, `gsutil` and `az storage blob lease break` commands, `terraformlockid` metadata, error code table (`LeaseAlreadyPresent`, `412`).
Method: documentation only; no commands were run.
