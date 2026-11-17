---
id: computing-software.cryptography-implementation.key-management.key-metadata-and-labelling
name: key-metadata-and-labelling
category: computing-software
field: cryptography-implementation
product: key-management
tags: [cryptography-implementation, key-management, key-types-and-cryptoperiods, key-metadata, key-labels, sp-800-130, kms-tags, key-inventory]
level: practitioner
status: docs-checked
description: "Record the metadata every key needs: identifier, owner, algorithm, purpose, state, dates, parent key, and how to keep labels useful without leaking secrets."
sources: ["https://csrc.nist.gov/pubs/sp/800/130/final", "https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final", "https://docs.aws.amazon.com/kms/latest/developerguide/tagging-keys.html", "https://docs.aws.amazon.com/kms/latest/developerguide/abac.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Key metadata and labelling

SP 800-57 Part 1 section 6.2.3 lists example metadata elements that should
accompany a key, and SP 800-130 section 6.2 covers key metadata for a
cryptographic key management system. Without it you cannot rotate, audit,
answer "what does this key protect", or prove a key was destroyed. SP 800-57
leaves the choice of elements to the implementer.

## Minimum metadata

| Field | Example |
|---|---|
| Key identifier | `alias/orders-field-enc` / version id |
| Owner / custodian | team and on-call contact |
| Algorithm and length | AES-256-GCM, P-256 |
| Purpose (single) | field encryption for `orders.card_last4` |
| State and dates | active since 2026-03-01, deactivate 2028-03-01 |
| Parent / wrapping key | KEK id and wrapping algorithm that protect it |
| Source | generated in HSM / imported |
| Protection | HSM, software, TPM |
| Data classification | sensitivity of what the key protects |
| Integrity mechanism | MAC or signature over the record |
| Linked policy | cryptoperiod, rotation schedule, backup requirement |

## Where to store it

- KMS tags/labels for owner, classification, data system, cost centre.
  AWS KMS tags can drive attribute-based access control (condition key
  `aws:ResourceTag/<tag-key>`); changing a tag can change access, so give
  tag-management permission (for example `kms:TagResource`) only to
  principals who need it.
- Ciphertext headers: key id and version, so data can always find its key.
- A central inventory for keys outside KMS.

## Rules

- Never put confidential data in tag keys or values; AWS notes tags are
  accessible to many services, including billing.
- Bind metadata integrity: SP 800-57 points to SP 800-152 for protecting
  metadata integrity and its association with the key. In your own key store,
  MAC or sign the metadata record together with the key.
- Make missing metadata a deploy-time failure (policy-as-code checks on
  infrastructure-as-code KMS resources requiring tags).

## Verify

- [ ] Every KMS key has owner, purpose and classification tags (scripted check).
- [ ] Every ciphertext format includes a key id/version.

## Checked

2026-11-01. Confirmed: SP 800-57 Pt1 Rev 5 section 6.2.3 (metadata element
examples: identifier, algorithm, owner, cryptoperiod, key type, source,
application, sensitivity, state, wrapping key and algorithm, integrity
mechanism; implementer selects elements; SP 800-152 for integrity), SP 800-130
section 6.2 Key Metadata exists, AWS KMS Tags page (no sensitive data in tags;
tags used for ABAC), AWS KMS ABAC page (`aws:ResourceTag`, tag changes can change
authorization). Removed: AWS description-field advice, CBOM/CMDB, FIPS level
and post-quantum algorithm examples, "must be bound" wording.

Method: documentation only; no commands were run.
