---
id: computing-software.cloud-infrastructure-engineering.azure.storage-security-sas-firewall-and-keys
name: storage-security-sas-firewall-and-keys
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, storage-security, storage-firewall, sas, shared-access-signature, user-delegation-sas, service-sas, account-sas, stored-access-policy, storage-keys, shared-key-access, key-rotation, entra-auth, storage-blob-data-contributor, private-endpoint, service-endpoint, resource-instance-rules, anonymous-access, defender-for-storage, malware-scanning, sas-expiration-policy]
level: practitioner
status: docs-checked
description: "Secure a storage account: disable shared key and anonymous access, Entra data roles, user delegation SAS and stored access policies, firewall and private endpoint rules."
sources: ["https://learn.microsoft.com/azure/storage/common/storage-sas-overview", "https://learn.microsoft.com/azure/storage/common/shared-key-authorization-prevent", "https://learn.microsoft.com/azure/storage/common/storage-network-security", "https://learn.microsoft.com/azure/storage/common/storage-account-keys-manage"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage security — identity first, SAS only when you must, network closed

**Goal:** nothing reads a blob with an account key; SAS tokens are short, scoped and
revocable; the account is unreachable from the internet unless deliberately exposed.

## 1. Authorization ladder (prefer the top)
1. **Microsoft Entra ID with Azure RBAC data roles** (for example *Storage Blob Data Reader/Contributor/Owner* and the queue, table and file equivalents). Assign at the narrowest scope that works (account or container for blobs). Apps use managed identity; humans use `az login` with `--auth-mode login`.
2. **User delegation SAS** - secured with Entra credentials instead of the account key; Microsoft recommends it whenever a SAS is needed (see the SAS overview for the services it supports).
3. **Service SAS with a stored access policy** - the policy lives on the container, queue, table or file share; revoking means changing or deleting the policy. Limit: five stored access policies per container.
4. **Ad hoc service SAS / account SAS / raw keys** - avoid; use near-term expiry and HTTPS, and have a revocation plan. Rotating or regenerating the account key revokes SAS signed with it.

Disallowing Shared Key authorisation (`az storage account update --allow-shared-key-access false`) rejects requests authorised with the account key, including account SAS and service SAS; user delegation SAS requests are still permitted. Find who still uses keys first:
`StorageBlobLogs | where AuthenticationType in ("AccountKey","SAS") | summarize count() by CallerIpAddress`.
Read the Shared Key article's compatibility list (Azure Cloud Shell and other tools and services, and Azure Files workloads) before disabling.

## 2. Keys, when they must exist
- Two keys let you rotate without downtime: update clients to the other key, then regenerate. Set a key expiration policy as a rotation reminder (Azure Policy *Storage account keys should not be expired* monitors it). See the key rotation skill.
- Microsoft recommends keeping keys in Azure Key Vault and rotating them regularly.
- A **SAS expiration policy** on the account specifies a recommended interval over which a SAS is valid; violations are recorded (the `SasExpiryStatus` log column).

## 3. Network
- Use the storage firewall: deny by default, then allow specific IP ranges, virtual network subnets (the subnet needs a Virtual Network service endpoint), resource instances and trusted services.
- Once a subnet uses a service endpoint, its traffic reaches storage with a private source IP, so IP network rules for those subnets no longer take effect.
- A network security exception can allow trusted services, and read access to resource logs and metrics, through the firewall.
- **Private endpoints** give each storage sub-service (blob, dfs, file, queue, table, web) a private IP in your VNet; see the Private Link documentation for the DNS zones to use.

## 4. Anonymous access and public exposure
`az storage account create ... --allow-blob-public-access false` disables anonymous blob access at the account level.

## Gotchas
- `--auth-mode login` needs a data-plane role; a control-plane role alone does not grant data access.
- A SAS tied to a stored access policy follows the policy: changing the policy changes every outstanding SAS at once - that's the feature.
- Adding a service endpoint changes the subnet's source address for storage and can invalidate existing IP rules.

## Verify
- [ ] `az storage account show --query "{shared:allowSharedKeyAccess,public:allowBlobPublicAccess}"` returns false/false (or the exception is justified).
- [ ] Diagnostic logs show no `AccountKey` authentication for 7 days before disabling shared key.
- [ ] Access from outside the allowed networks is rejected.

## Checked

2026-10-24, against MicrosoftDocs/azure-docs (storage/common storage-sas-overview, shared-key-authorization-prevent, storage-network-security, storage-account-keys-manage, storage-account-create): SAS types and Microsoft's user delegation SAS recommendation, five stored access policies per container, SAS expiration policy, SAS revocation by key rotation, effect of disallowing Shared Key (user delegation SAS still allowed), firewall rule types and service endpoint behaviour (IP rules stop applying to subnets with service endpoints), trusted-service and logs-and-metrics exceptions, `--allow-blob-public-access false`. Removed the Defender for Storage section (its documentation is not in the public docs repository and could not be read), the unconfirmed seven-day user delegation limit, the Azure CLI SAS, policy, network-rule and private-endpoint commands, private-range IP-rule claim and the Azure Files key remark.

Method: documentation only; no commands were run.
