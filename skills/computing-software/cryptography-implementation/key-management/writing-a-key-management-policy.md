---
id: computing-software.cryptography-implementation.key-management.writing-a-key-management-policy
name: writing-a-key-management-policy
category: computing-software
field: cryptography-implementation
product: key-management
tags: [cryptography-implementation, key-management, key-management-policy, ckms, key-management-practice-statement, sp-800-57-part-2, sp-800-130, governance, compliance, pci-dss]
level: advanced
status: draft
description: "Write a key management policy and practice statement per SP 800-57 Pt2 and SP 800-130: required sections, roles, per-key-class rules, and how auditors (PCI, SOC 2) read it."
sources: ["https://csrc.nist.gov/pubs/sp/800/57/pt2/r1/final", "https://csrc.nist.gov/pubs/sp/800/130/final", "https://csrc.nist.gov/pubs/sp/800/152/final", "https://www.pcisecuritystandards.org/document_library/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Writing a key management policy

SP 800-57 Part 2 separates the **Key Management Policy** (KMP: what must be
true, approved by management) from the **Key Management Practice Statement**
(KMPS: how this organisation actually does it). SP 800-130 lists the design
topics a cryptographic key management system (CKMS) must document. Auditors
(PCI DSS req 3.6-3.7, SOC 2 CC6, ISO 27001 A.8.24) ask for both.

## KMP sections

1. Scope: systems, data classifications, key types covered.
2. Roles: key owner, custodians, KMS administrators, auditors; separation
   rules (no single person can both administer and use a key).
3. Approved algorithms and minimum strengths (reference SP 800-131A / your
   crypto standard), with review date.
4. Cryptoperiods per key class.
5. Generation requirements (approved RBG, HSM/KMS for which classes).
6. Storage and protection (never plaintext outside HSM/KMS for class X).
7. Distribution and access control.
8. Rotation, revocation, compromise handling and notification.
9. Backup, archive, recovery and destruction.
10. Logging, audit, and review cadence.
11. Exceptions process (who approves, expiry).

## KMPS: the "how"

For each key class, a table row: algorithm, where generated, where stored,
who can use it (IAM roles), rotation mechanism (automatic KMS rotation / job
name), backup method, destruction method, monitoring. Link to runbooks.

| Key class | Alg | Store | Rotation | Owner |
|---|---|---|---|---|
| PII field DEKs | AES-256-GCM | wrapped by KMS CMK `pii-kek` | DEK per month, CMK yearly auto | Data platform |
| JWT signing | ES256 | KMS asymmetric | 90 days, JWKS overlap 7 days | Identity team |
| TLS edge | ECDSA P-256 | ACM | ACME/ACM auto | Platform |

## Practical rules

- Keep it short enough to be read; push tool specifics into the KMPS and runbooks.
- Every "must" needs an owner and a way to check it (a config rule, a scan, a report).
- Version the documents; review annually and after incidents or algorithm changes.

## Verify

- [ ] KMP approved and dated; KMPS covers every key class in the inventory.
- [ ] Each requirement maps to evidence (screenshot, config, log query) for audits.
- [ ] Exceptions have expiry dates and approvers.
