---
id: computing-software.cloud-infrastructure-engineering.azure.azcopy-authentication-entra-sas-and-managed-identity
name: azcopy-authentication-entra-sas-and-managed-identity
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azcopy, azcopy-login, azcopy-auth, azcopy-auto-login-type, managed-identity, sas]
level: practitioner
status: docs-checked
description: "Authenticate AzCopy v10 with Entra (interactive, managed identity, service principal, Azure CLI token) or SAS, including headless env-var auto-login and required data roles."
sources: ["https://learn.microsoft.com/azure/storage/common/storage-use-azcopy-v10", "https://github.com/Azure/azure-storage-azcopy", "https://learn.microsoft.com/azure/storage/blobs/authorize-access-azure-active-directory"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AzCopy authentication: Entra, SAS and managed identity

**Goal:** AzCopy jobs run unattended with an identity, not a pasted SAS, and fail clearly when
permissions are missing.

## Entra methods
AzCopy can authorise with Microsoft Entra ID (credentials once, no SAS appended to each command) or with a SAS token. The identity needs an Azure RBAC data role on the account or container, for example **Storage Blob Data Contributor** to write; control-plane roles alone don't grant data access. Role assignments can take up to 30 minutes to propagate.

Headless via environment variables (no interactive login). `AZCOPY_AUTO_LOGIN_TYPE` accepts `DEVICE`, `SPN`, `MSI`, `AZCLI`, `PSCRED` and `WORKLOAD` (case-insensitive):
```bash
# managed identity (VM, Arc, ACI)
export AZCOPY_AUTO_LOGIN_TYPE=MSI
export AZCOPY_MSI_CLIENT_ID=<uami-client-id>        # only for user-assigned
# service principal with certificate
export AZCOPY_AUTO_LOGIN_TYPE=SPN AZCOPY_SPA_APPLICATION_ID=<app-id> AZCOPY_TENANT_ID=<tenant> \
       AZCOPY_SPA_CERT_PATH=/secure/sp.pfx AZCOPY_SPA_CERT_PASSWORD=<pwd>
# reuse Azure CLI / Azure PowerShell sign-in
export AZCOPY_AUTO_LOGIN_TYPE=AZCLI      # or PSCRED
# workload identity
export AZCOPY_AUTO_LOGIN_TYPE=WORKLOAD
azcopy copy ./out "https://stdata.blob.core.windows.net/exports/" --recursive
```
Interactive: `azcopy login --tenant-id <tenant>` (device code by default); `azcopy login --login-type=MSI` (the `--identity` and `--service-principal` flags are deprecated in favour of `--login-type`); `azcopy login status`; `azcopy logout`.
AzCopy also reads `AZCOPY_SPA_CLIENT_SECRET` and `AZCOPY_MSI_OBJECT_ID` / `AZCOPY_MSI_RESOURCE_STRING` as environment settings.

## SAS
Append the SAS token to each source or destination URL, quoted: `"https://stdata.blob.core.windows.net/exports?sv=...&sig=..."`.
For service-to-service copies, a SAS (or S3 access key) is required on the source unless it is public; Blob and Blob (Data Lake) endpoints additionally support OAuth on both source and destination.
Prefer a user delegation SAS (Entra-signed) over an account-key SAS.

## Diagnostics
- `azcopy jobs show <job-id> --with-status=Failed` lists failed transfers of a job.
- `AZCOPY_LOG_LOCATION` moves the log folder.
- A 403 after a fresh role assignment may just be propagation delay; a 403 with correct roles can also be the storage firewall (see the storage security skill).

## Gotchas
- A SAS that expires before a long job finishes makes the job fail midway; make the expiry longer than the job plus a resume margin.
- `AZCOPY_AUTO_LOGIN_TYPE` takes effect without an explicit login; unset it when debugging identity problems.

## Verify
- [ ] `azcopy list "https://stdata.blob.core.windows.net/exports"` works with the chosen environment variables and no SAS.
- [ ] Storage logs show `AuthenticationType` OAuth for the job's requests.

## Checked

2026-10-24, against the Azure/azure-storage-azcopy source (release v10.34.1, 2026-10-22: cmd/login.go, cmd/loginStatus.go, cmd/jobsShow.go, cmd/copy.go, common/environment.go), MicrosoftDocs/azure-docs storage-use-azcopy-v10 and the Entra authorization article: environment variable names and the AZCOPY_AUTO_LOGIN_TYPE value set, `--login-type`, deprecation of `--identity` and `--service-principal`, `azcopy login status`, `jobs show --with-status`, S2S SAS requirement and OAuth on both sides for Blob and Blob (Data Lake), AZCOPY_LOG_LOCATION, Storage Blob Data Contributor role, 30-minute role propagation. Removed the unconfirmed Reader role statement, 10-minute propagation, keyring remark, v10.22 claim, error-code mappings, default log directory and Azure Files remark.

Method: documentation only; no commands were run.
