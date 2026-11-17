---
id: computing-software.cloud-infrastructure-engineering.azure.storage-key-rotation-reminders-and-key-vault-managed-keys
name: storage-key-rotation-reminders-and-key-vault-managed-keys
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, storage-security, storage-key-rotation, key-rotation-reminder, key-vault-managed-storage-keys, key-expiration-policy, storage-keys]
level: practitioner
status: docs-checked
description: "Rotate storage account keys safely: key expiration policy reminders, two-key rotation order, Key Vault guidance, and moving off keys entirely."
sources: ["https://learn.microsoft.com/azure/storage/common/storage-account-keys-manage", "https://learn.microsoft.com/azure/storage/common/shared-key-authorization-prevent"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage key rotation reminders and Key Vault managed keys

**Goal:** if account keys must exist, they rotate on schedule without outages; better, nothing
uses them.

## Reminders: key expiration policy
```bash
az storage account update -g rg -n stdata --key-exp-days 90
```
A key expiration policy is a reminder only: Azure doesn't rotate for you. Azure Policy (*Storage account keys should not be expired*) can monitor compliance. The `KeyCreationTime` property must be set to create the policy; older accounts may have it null until the keys are rotated once.

## Two-key rotation order (no downtime)
1. Apps currently use **key1**.
2. Regenerate the **secondary** key → update Key Vault secret / app config to it → restart/refresh apps.
3. Verify no requests still use the old key (`StorageBlobLogs | where AuthenticationType == "AccountKey"`; `AuthenticationHash` is the hash of the authentication token).
4. Regenerate the **primary** key. Next cycle, swap roles.
```bash
az storage account keys renew -g rg --account-name stdata --key secondary
```

## Automated rotation
Microsoft recommends managing account keys in Azure Key Vault and rotating them regularly; Key Vault lets you rotate without interrupting applications. See the Key Vault documentation for the current rotation tutorials and for the status of the managed storage account keys feature (not confirmed here).

## Get off keys
- Entra auth everywhere (data roles), user delegation SAS for external sharing.
- Then `az storage account update -n stdata -g rg --allow-shared-key-access false`.
  Check first: `StorageBlobLogs | where AuthenticationType in ("AccountKey","SAS") | summarize count() by CallerIpAddress` and read the compatibility list in the Shared Key article (Azure Cloud Shell and some other Azure tools and services depend on keys).

## Gotchas
- Rotating or regenerating a key revokes account and service SAS tokens signed with it; user delegation SAS tokens are unaffected.
- Regenerating a key can affect any application or Azure service that depends on it.

## Verify
- [ ] `az storage account show -n stdata --query "{exp:keyPolicy.keyExpirationPeriodInDays, created:keyCreationTime}"`.
- [ ] Target state: `allowSharedKeyAccess=false` and no app errors.

## Checked

2026-10-24, against MicrosoftDocs/azure-docs (storage/common/storage-account-keys-manage, shared-key-authorization-prevent): key expiration policy is a reminder, `KeyCreationTime` prerequisite, Azure Policy *Storage account keys should not be expired*, `az storage account keys renew` (`--key primary`), Key Vault recommendation, SAS revocation on rotation (user delegation SAS unaffected), `AuthenticationType` values. Removed the Key Vault deprecation claim and the Event Grid and Function rotation recipe (the Key Vault articles are not in the public docs repository and could not be read), plus the role-name, App Service refresh and Azure Files remount claims.

Method: documentation only; no commands were run.
