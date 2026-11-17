---
id: computing-software.systems-network-administration.pki-tls-administration.key-ceremony-script
name: key-ceremony-script
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [key-ceremony-script, pki-hsm, hsm, key-ceremony, dual-control, witness, pki-tls-administration]
level: practitioner
status: draft
description: "Plan and run a root key generation ceremony with roles, script, witnesses, tamper evidence and a signed record."
sources:
  - https://csrc.nist.gov/pubs/sp/800/57/pt2/r1/final
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Root key ceremony script
Goal: a documented, witnessed event that produces the root with no single point of trust.
Roles: ceremony administrator, two or three key custodians (HSM role holders), internal witness, external auditor, scribe.
Script outline:
1. Pre-ceremony: dry run, bill of materials, HSM firmware check, hash and verify the OS image, review script with all roles.
2. Room: access log, phones and recorders per policy, video of the room if the CPS requires.
3. Boot from verified media; record serial numbers of HSM, smart cards, tamper bags.
4. Initialise HSM, set SO and custodian credentials, generate root key (`CKA_EXTRACTABLE=false`), export wrapped backup shares.
5. Self-sign root with `basicConstraints`, `keyUsage`; print and hash the certificate; read fingerprint aloud and cross-check.
6. Sign issuing CA CSR, create first CRL.
7. Seal cards in numbered tamper-evident bags; witnesses sign each step.
8. Publish fingerprint of the root on at least two channels.
Gotcha: unscripted improvisation is the failure mode; any deviation is recorded, not fixed silently.
Verify:
- [ ] Signed ceremony record with hashes and bag numbers exists.
- [ ] Root fingerprint matches across the cert, the record and the publication.
