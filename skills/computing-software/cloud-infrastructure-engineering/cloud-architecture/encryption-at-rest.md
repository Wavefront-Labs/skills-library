---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.encryption-at-rest
name: encryption-at-rest
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, data-protection, encryption-at-rest, cmk, sse-kms, customer-managed-keys, disk-encryption, double-encryption]
level: practitioner
status: draft
description: "Design encryption at rest: provider-managed vs customer-managed keys per data class, enforcement by policy, key access separation, and the operational costs of CMKs."
sources: ["https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html", "https://learn.microsoft.com/azure/security/fundamentals/encryption-atrest", "https://cloud.google.com/docs/security/encryption/default-encryption"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Encryption at rest design

## Options
| Option | Control | Cost/ops |
|---|---|---|
| Provider-managed keys (default) | Provider controls keys; always on for major services | None |
| Customer-managed keys (CMK) in KMS/Key Vault/Cloud KMS | You control key policy, rotation, disable/revoke, audit of key use | Per-key and per-request charges; availability dependency |
| HSM-backed / external key (CloudHSM, Managed HSM, Cloud EKM, XKS) | Keys outside provider control | High cost and latency; outage risk |
| Application-level / client-side encryption | Data encrypted before storage | App complexity, limits querying |

## Decide per data class
- Public/internal: provider-managed.
- Confidential/regulated: CMK where you need revocation, separation of duties or audit of key use.
- Highly restricted / sovereignty: HSM/external keys or client-side.

## Steps
1. Map data stores to classes; pick key type.
2. Key hierarchy: one key per workload/environment/data class (not one key for everything).
3. Key policy separation: key admins cannot use keys; data users cannot manage keys.
4. Enforce via policy (deny unencrypted or non-CMK resources for confidential tags).
5. Enable rotation (KMS automatic annual or configurable; Key Vault rotation policy).
6. Monitor key usage and deletion attempts (scheduled deletion waiting period 7-30 days in KMS).

## Gotchas
- Disabling a CMK makes data unavailable instantly - an availability risk and an attacker lever.
- Cross-account access needs both key policy and resource policy.
- KMS request throttling at high volumes; use data keys / bucket keys (S3 Bucket Keys reduce KMS calls).

## Verify
- [ ] Policy compliance shows 100% confidential stores on CMK.
- [ ] Key policies reviewed for separation of duties.
