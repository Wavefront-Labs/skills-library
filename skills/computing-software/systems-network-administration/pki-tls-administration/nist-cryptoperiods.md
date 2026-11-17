---
id: computing-software.systems-network-administration.pki-tls-administration.nist-cryptoperiods
name: nist-cryptoperiods
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [nist-cryptoperiods, pki-key-mgmt, nist-800-57, cryptoperiod, key-lifecycle, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Set key lifetimes and states (pre-activation to destruction) for CA, TLS and signing keys using NIST SP 800-57."
sources:
  - https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cryptoperiods and key lifecycle
Goal: documented lifetimes and rotation for every key type.
Suggested cryptoperiods (SP 800-57 Part 1 Rev 5, Table 1 and the per-key-type cryptoperiod text; longer or shorter may be warranted, but weigh the risks of going longer):
| Key | Originator-usage period |
|---|---|
| Private signature key | 1 to 3 years |
| Public signature-verification key | several years (depends on key size) |
| Private authentication key | 1 to 2 years |
| Symmetric authentication key | no more than 2 years, recipient-usage up to 3 years more |
- A private signature key must be destroyed at the end of its cryptoperiod.
- When the public key is certified by a CA, the private signature key's cryptoperiod ends at the notAfter date of the last certificate issued for that key. Several consecutive certificates may be issued for the same public key.
- A public verification key may outlive its private key; with a trusted timestamp, signatures made within the private key's usage period can still be verified later.
- Key states: pre-activation, active, suspended, deactivated, compromised, destroyed.
- The standard does not give separate CA-root versus TLS-server figures: the root CA lifetime and TLS leaf-key lifetime are your policy decisions inside these bounds.
Verify:
- [ ] Key register lists every CA key with activation and retirement dates.
- [ ] Each key type has a stated cryptoperiod and a documented reason where it exceeds Table 1.

## Checked
Method: docs-checked 2026-11-09 against NIST SP 800-57 Part 1 Rev 5 PDF (nvlpubs.nist.gov), read Table 1 and the per-key-type cryptoperiod text and the key-state glossary entries.
Removed: root CA 20-year and issuing CA 5-10 year figures, TLS server 1-2 year and code-signing 1-3 year rows (not in Table 1), the compromise procedure and certbot --reuse-key gotcha (not in source).
