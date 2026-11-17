---
id: computing-software.cryptography-implementation.key-management.tenant-key-isolation-in-saas
name: tenant-key-isolation-in-saas
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, tenant-key-isolation, customer-managed-keys, byok, multi-tenant, encryption-context, kms]
level: advanced
status: draft
description: "Isolate tenant keys in multi-tenant SaaS: per-tenant data keys, customer-managed keys (BYOK/HYOK), encryption context binding, revocation behaviour and costs."
sources: ["https://docs.aws.amazon.com/whitepapers/latest/saas-tenant-isolation-strategies/saas-tenant-isolation-strategies.html", "https://docs.aws.amazon.com/kms/latest/developerguide/encrypt_context.html", "https://cloud.google.com/kms/docs/cmek"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tenant key isolation in SaaS

## Tiers
1. **Shared key, per-tenant context**: one KMS key; every request binds `tenant_id` as encryption context/AAD.
   Cheap; isolation enforced by IAM conditions (`kms:EncryptionContext:tenant_id`).
2. **Per-tenant KMS key**: separate key per tenant; IAM policy per key; clean crypto-shredding on offboarding.
   KMS key costs and quotas scale with tenants.
3. **Customer-managed key (BYOK/CMEK)**: key lives in the customer's KMS account; customer grants your role use
   and can revoke it.
4. **HYOK/external key store**: key outside the cloud (AWS XKS, Google EKM).

## Design points
- Use envelope encryption: per-tenant (or per-object) DEKs wrapped by the tenant's KEK.
- Always bind tenant ID into AAD, even with per-tenant keys, to stop cross-tenant ciphertext swaps.
- Customer revocation: define behaviour (fail closed, cached DEK TTL, how quickly service stops). Document
  that revocation makes data inaccessible, including backups.
- Monitor key-access errors per tenant; a revoked CMK should alert, not silently break jobs.

## Pitfalls
- Caching decrypted DEKs across tenants in one cache without tenant scoping.
- Search indexes, caches and analytics copies left outside the tenant-key scope.

## Verify
- [ ] Test: tenant A's ciphertext fails to decrypt under tenant B's context; revoked CMK stops access within SLA.
