---
id: computing-software.database-administration.cloud-nosql-databases.cosmos-network-and-encryption
name: cosmos-network-and-encryption
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [cosmos-network-and-encryption, cosmos-security, cosmos-db, azure-cosmos-db, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Lock down network paths and manage keys."
sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-configure-private-endpoints
  - https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-configure-firewall
  - https://learn.microsoft.com/en-us/azure/cosmos-db/database-encryption-at-rest
  - https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-setup-customer-managed-keys
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network and encryption controls

**Goal:** Lock down network paths and manage keys.

## Steps
- Use private endpoints and set publicNetworkAccess to Disabled, or restrict access with IP firewall rules (changes can take up to 15 minutes to propagate; requests from outside the list get 403) combined with subnet and virtual network access control.
- Data is encrypted at rest by default (AES-256) with service-managed keys; you can add a second layer with customer-managed keys in Azure Key Vault, which should be configured at account creation and need soft delete and purge protection on the vault.
- Customer-managed keys with continuous backup currently support only a user-assigned managed identity for creating the account.

## Gotcha
Revoking a customer-managed key has account-level effects (see "How do I revoke an encryption key?" on the CMK page); a backup can miss data written up to one hour before a revocation.

## Checked

2026-11-03. Confirmed against the private endpoints, IP firewall, encryption at rest and customer-managed keys pages: publicNetworkAccess flag, firewall 403 and 15-minute propagation, subnet/virtual network combination, AES-256 default, second layer with CMK, creation-time deployment, soft delete and purge protection, continuous backup identity limit, revocation backup note.
Removed: Always Encrypted, diagnostic settings to Log Analytics, and the "revoked key makes account unavailable" claim (none on the pages read). Replaced the unrelated RBAC source.
Method: documentation only; no commands were run.

## Verify
- [ ] Public access is disabled and private DNS resolves to the private endpoint.
