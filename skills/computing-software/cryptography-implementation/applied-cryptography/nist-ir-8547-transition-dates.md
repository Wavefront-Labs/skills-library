---
id: computing-software.cryptography-implementation.applied-cryptography.nist-ir-8547-transition-dates
name: nist-ir-8547-transition-dates
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, ir-8547-deadlines, nist-ir-8547, pq-migration, deprecation, post-quantum]
level: practitioner
status: docs-checked
description: "Plan against NIST IR 8547 post-quantum transition dates: 112-bit RSA/ECC deprecated after 2030 and all quantum-vulnerable algorithms disallowed after 2035."
sources: ["https://csrc.nist.gov/pubs/ir/8547/ipd"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NIST IR 8547 transition dates

## Timeline (initial public draft, November 2024; confirm the final text)
| Algorithm family | 112-bit security strength | 128-bit or more |
|---|---|---|
| Digital signatures (RSA, ECDSA, EdDSA) | deprecated after 2030, disallowed after 2035 | disallowed after 2035 |
| Key establishment (RSA, DH, ECDH) | deprecated after 2030, disallowed after 2035 | disallowed after 2035 |

Replacements: ML-KEM (FIPS 203), ML-DSA (FIPS 204), SLH-DSA (FIPS 205), LMS/XMSS (SP 800-208).
Symmetric primitives with at least 128 bits of classical security are believed to meet at least security category 1,
so they are far less affected; the few 112-bit symmetric standards are to be disallowed in 2030.

## Planning
1. Inventory where RSA/ECC is used (CBOM).
2. Prioritise data with confidentiality beyond 2035 (harvest-now-decrypt-later) for hybrid KEM now.
3. Signatures with long validity (roots, firmware) next.
4. Map each system's replacement and its date against the 2030/2035 milestones.

## Verify
- [ ] Roadmap cites IR 8547 version and dates; reviewed when the final version is published.

## Checked
2026-11-01. Confirmed against the NIST IR 8547 initial public draft PDF (released 12 November 2024): the
deprecated-after-2030 and disallowed-after-2035 rows for signatures and key establishment at 112-bit and 128-bit-plus
strength; FIPS 203/204/205 and SP 800-208 named as replacements; symmetric section (128-bit primitives at category 1
or better, 112-bit symmetric standards disallowed in 2030). Removed: CNSA 2.0 and EU roadmap dates, and the named
example algorithms per strength (not confirmed in this batch).
Method: documentation only; no commands were run.
