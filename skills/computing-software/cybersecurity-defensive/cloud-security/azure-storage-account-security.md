---
id: computing-software.cybersecurity-defensive.cloud-security.azure-storage-account-security
name: azure-storage-account-security
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [storage-account-security, azure-storage, shared-key-access, sas-tokens, private-endpoints, immutable-storage, cloud-data-protection]
level: practitioner
status: docs-checked
description: "Secure Azure storage accounts: disable shared key and anonymous access, Entra auth and user delegation SAS, firewall and private endpoints, soft delete, immutability."
sources: ["https://learn.microsoft.com/en-us/azure/storage/blobs/security-recommendations", "https://learn.microsoft.com/en-us/azure/storage/common/shared-key-authorization-prevent", "https://learn.microsoft.com/en-us/azure/storage/blobs/anonymous-read-access-prevent", "https://learn.microsoft.com/en-us/azure/storage/blobs/immutable-storage-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure storage account security

## Authentication
- Prefer Microsoft Entra ID (Azure RBAC, least privilege) to authorise blob requests over Shared Key.
- Disallow Shared Key (`allowSharedKeyAccess` = `false`): requests authorised with account keys are rejected, including service SAS and account SAS tokens for Blob Storage. A **user delegation SAS** (authorised with Entra ID) still works. The property is not set by default and a null value permits Shared Key; only Azure Resource Manager accounts support the property. Before flipping it, check logs for requests authorised with Shared Key or SAS.
- Revocation plan for SAS: revoke a user delegation key to invalidate all signatures made with it; revoke a service SAS tied to a stored access policy by deleting or renaming the policy or setting its expiry in the past. A service SAS without a stored access policy cannot be revoked, so keep it at one hour or less.
- Limit SAS tokens to HTTPS and give each only the permissions needed.
- If you must keep Shared Key: store account keys in Azure Key Vault and regenerate them periodically.
- Disable anonymous read access (`allowBlobPublicAccess` = `false`) for containers and blobs unless a scenario requires it.

## Network
- Enable storage firewall rules for specific IP ranges or VNet subnets; add the "trusted Microsoft services" exception only where needed (firewall rules otherwise block other Azure services, the portal and logging services).
- Use private endpoints (a private IP from your VNet) and VNet service tags.
- Set the minimum required TLS version for the account, and enable "Secure transfer required" so HTTP requests are rejected.

## Data protection
- Turn on soft delete for blobs and for containers.
- Immutable storage: legal holds and time-based retention put blobs in a WORM state (readable, not modifiable or deletable during the retention interval).
- Azure Resource Manager lock on the account prevents deleting or reconfiguring the account, not deleting data inside it.
- Data is encrypted at rest by default with Microsoft-managed keys; use customer-managed keys in Key Vault for more control.
- Disallow cross-tenant object replication.

## Monitoring
- Enable Microsoft Defender for Storage on all storage accounts.
- Enable storage logging that records how requests were authorised (anonymous, OAuth 2.0, Shared Key, SAS) and set Azure Monitor log alerts.

## Verify
- [ ] `az storage account show` with `--query "allowSharedKeyAccess"` returns `false` after you disable Shared Key.
- [ ] Anonymous access, firewall or private endpoint and TLS settings match your standard.
- [ ] Soft delete restore tested.

## Checked
2026-11-09: read the Blob storage security recommendations page in full and the sections of the Shared Key, anonymous access and immutable storage pages that cover `allowSharedKeyAccess`, user delegation SAS, log queries and WORM. Removed unconfirmed claims: user delegation SAS 7-day maximum, "keys never expire", new-account default for anonymous access, `publicNetworkAccess`, `minimumTlsVersion` and `supportsHttpsTrafficOnly` property values, `sasPolicy`, soft delete retention days, log category names, Defender for Storage feature list, Azure Policy compliance checks, the `publicNetworkAccess` portion of the verify command.
Method: documentation only; no commands were run.
