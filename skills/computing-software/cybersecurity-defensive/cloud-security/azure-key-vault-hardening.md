---
id: computing-software.cybersecurity-defensive.cloud-security.azure-key-vault-hardening
name: azure-key-vault-hardening
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [cloud-data-protection, key-vault-hardening, azure-key-vault, rbac-permission-model, purge-protection, private-endpoints, managed-hsm]
level: practitioner
status: docs-checked
description: "Harden Azure Key Vault: RBAC instead of access policies, soft delete and purge protection, private endpoints and firewall, per-app vaults, logging, and alerting on secret reads."
sources: ["https://learn.microsoft.com/en-us/azure/key-vault/general/security-features", "https://learn.microsoft.com/en-us/azure/key-vault/general/rbac-guide", "https://learn.microsoft.com/en-us/azure/key-vault/general/soft-delete-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure Key Vault hardening

## Permission model
- Use **Azure RBAC** rather than legacy access policies: consistent with
  the rest of Azure, supports PIM, scoped at vault or individual secret/key level.
- Roles: `Key Vault Secrets User` (read secret values) for apps' managed identities; `Key Vault Crypto
  User` for key operations; `Key Vault Administrator` only for platform admins (via PIM).
- With access policies, anyone with `Microsoft.KeyVault/vaults/write` (Contributor) can grant themselves
  data access: another reason to switch to RBAC.

## Data protection
- **Soft delete** (mandatory now, 7-90 days) and **purge protection** on: deleted vaults and objects are
  recoverable and cannot be purged before retention ends, even by admins (ransomware/insider defence).
- Key rotation policies for keys; expiry dates on secrets with Event Grid "near expiry" events.
- HSM-backed keys or Managed HSM where HSM protection is required.

## Network
- Firewall: disable public network access, with **private endpoints** in app VNets, or selected networks.
- "Allow trusted Microsoft services" only if a specific service needs it.

## Topology
One vault per application per environment (blast radius, clear ownership).
No shared "everything" vault.

## Logging and alerting
- Diagnostic settings: `AuditEvent` to Log Analytics/Sentinel.
- Alert on: `SecretGet` by unexpected identities or from public IPs, bulk `SecretList`/`SecretGet`,
  vault access policy or role assignment changes, purge attempts, firewall changes.

## Policy
Use Azure Policy built-in definitions for Key Vault (purge protection, private link, RBAC permission model, secret expiry); look up the exact names in the policy definitions list and assign in audit or deny.

## Gotchas
- Moving to RBAC flips the model at once; map existing access policies to role assignments first.

## Checked

2026-10-28: confirmed on Learn (security features, RBAC guide, soft-delete overview): RBAC roles Key Vault Administrator, Crypto User and Secrets User; a Contributor can grant themselves data-plane access via access policies; soft delete is on by default and cannot be disabled with a 7 to 90 day retention; with purge protection a deleted vault or object cannot be purged until retention passes. Removed: `enableRbacAuthorization` and `publicNetworkAccess` property names, FIPS level, Premium SKU, private DNS zone name, throttling claim, Defender/Tor claim, KQL sample and column names, exact policy names, purge-protection-irreversible and App Service reference gotchas.

Method: documentation only; no commands were run.

## Verify
Azure Policy compliance for the Key Vault definitions you assigned, vault not reachable from the internet
(`nslookup` resolves private IP from VNet, public access denied), and a test secret read raises the alert.
