---
id: computing-software.cryptography-implementation.applied-cryptography.queryable-encryption-for-databases
name: queryable-encryption-for-databases
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, queryable-encryption, searchable-encryption, always-encrypted, mongodb-queryable-encryption, deterministic-encryption]
level: advanced
status: draft
description: "Pick a queryable encryption approach for databases: deterministic and blind-index equality, MongoDB Queryable Encryption, Always Encrypted, and their leakage."
sources: ["https://www.mongodb.com/docs/manual/core/queryable-encryption/", "https://learn.microsoft.com/en-us/sql/relational-databases/security/encryption/always-encrypted-database-engine", "https://www.cs.cornell.edu/~tomer/papers/oakland15.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Queryable encryption for databases

## Options
| Approach | Queries | Leakage |
|---|---|---|
| Deterministic encryption (AES-SIV, Always Encrypted deterministic) | equality, join | equal values, frequency |
| Blind index (HMAC of value, truncated) | equality | frequency, reduced by truncation |
| MongoDB Queryable Encryption | equality, range (8.0) | structured leakage, no frequency for equality tokens |
| Always Encrypted with secure enclaves | equality, range, LIKE inside enclave | enclave trust |
| Order-preserving / revealing | range | order, often approximate value: avoid |

## Choosing
- Low-cardinality fields (gender, status) leak almost entirely under deterministic schemes; do not make them
  queryable.
- Prefer randomized encryption plus a blind index for high-cardinality exact-match fields (email, SSN).
- Keep keys client-side (driver-level), so a DB admin or backup holder sees only ciphertext.

## Operational notes
- Index and sort on encrypted columns is limited; plan queries before encrypting.
- Key rotation for deterministic data requires re-encrypting the column and rebuilding indexes.
- Attacks on property-preserving encryption (Naveed et al. 2015) recovered values from frequency analysis; use
  them only after a leakage review.

## Verify
- [ ] Leakage profile documented per queryable field and accepted by data owner.
