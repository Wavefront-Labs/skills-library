---
id: computing-software.cloud-infrastructure-engineering.azure.storage-entra-authorization-and-default-to-oauth
name: storage-entra-authorization-and-default-to-oauth
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, storage-security, entra-authorization-storage, auth-mode-login, default-to-oauth, storage-data-roles]
level: practitioner
status: docs-checked
description: "Move Azure Storage access to Entra ID: data-plane roles, --auth-mode login, SDK credentials, portal default-to-OAuth, and verifying no one still uses keys."
sources: ["https://learn.microsoft.com/azure/storage/blobs/authorize-access-azure-active-directory", "https://learn.microsoft.com/azure/storage/blobs/authorize-data-operations-portal", "https://learn.microsoft.com/azure/storage/blobs/authorize-data-operations-cli", "https://learn.microsoft.com/azure/storage/common/shared-key-authorization-prevent"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Entra authorization for Azure Storage

**Goal:** every human and app accesses storage data with Entra identities and RBAC, so keys and SAS can be disabled.

## Roles (data plane)
Storage Blob Data Reader / Contributor / Owner (Owner can set ownership and manage access control on data), plus the equivalent queue, table and file data roles; see the built-in roles list for exact names.
A role can be assigned at subscription, resource group, storage account or container scope; use the narrowest that works.
```bash
az role assignment create --assignee <objectId> --role "Storage Blob Data Reader" \
  --scope "/subscriptions/<sub>/resourceGroups/rg/providers/Microsoft.Storage/storageAccounts/st/blobServices/default/containers/reports"
```
Creating a storage account does not automatically give you data permissions through Entra ID; assign a data role explicitly. Role assignments can take up to 30 minutes to propagate.

## CLI / tools
```bash
az storage blob list --account-name st --container-name reports --auth-mode login -o table
```
If you omit `--auth-mode` or set it to `key`, the CLI attempts to use the account access key. Set the environment variable
`AZURE_STORAGE_AUTH_MODE=login` in shells and pipelines so data commands use Entra.

## SDKs
```python
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
svc = BlobServiceClient("https://st.blob.core.windows.net", credential=DefaultAzureCredential())
```

## Portal
Enable **Default to Microsoft Entra authorization in the Azure portal** when creating the account (Advanced tab, Security section) or on an existing account's configuration. It sets only the default method; a user can still choose to authorise with the access key.

## Prove keys aren't used, then disable
```kusto
StorageBlobLogs
| where TimeGenerated > ago(14d)
| summarize count() by AuthenticationType, CallerIpAddress, UserAgentHeader
```
When no key or SAS authorisation remains, disallow Shared Key authorisation on the account (`allowSharedKeyAccess` false; a separate skill covers this).

## Gotchas
- Role assignments can take up to 30 minutes to propagate.
- Some tools and services only support keys or SAS - inventory before disabling Shared Key.

## Verify
- [ ] Logs show only OAuth for two weeks; portal browsing works for users with data roles only.

## Checked

2026-10-24, against MicrosoftDocs/azure-docs (storage/blobs authorize-access-azure-active-directory, authorize-data-operations-cli, authorize-data-operations-portal, storage/common shared-key-authorization-prevent) and the Azure Monitor StorageBlobLogs table reference: `--auth-mode login` and the default-to-key behaviour, `AZURE_STORAGE_AUTH_MODE`, role scopes, 30-minute propagation, portal default-to-Entra setting, `AuthenticationType` values `AccountKey` and `SAS`. Removed the unconfirmed `--default-to-oauth-authentication` flag, azcopy login line, listKeys remark and Azure Files Kerberos remark.

Method: documentation only; no commands were run.
