---
id: computing-software.systems-network-administration.pki-tls-administration.offline-root-storage
name: offline-root-storage
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [offline-root-storage, pki-hierarchy, pki, offline-root, air-gap, pki-tls-administration]
level: practitioner
status: draft
description: "Run the root CA offline: air-gapped machine, rare signing events, key storage, backups, CRL refresh schedule and access control."
sources:
  - https://www.rfc-editor.org/rfc/rfc3647
  - https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Offline root CA operation
Goal: the root key exists only where it can be signed with under dual control, and is otherwise inert.
1. Dedicated host (or VM image on encrypted media) never joined to a network or domain; remove NIC and wireless.
2. Root key in an HSM or smart card with M-of-N activation; paper or encrypted USB backup in separate safes.
3. Power on only to (a) sign or renew an intermediate, (b) publish a new CRL. Typical CRL validity is 6-12 months, so schedule a CRL ceremony before it lapses.
4. Move files with write-once media; hash them on both sides (`sha256sum`).
5. Log every power-on in a signed ceremony record.
Gotcha: an offline root whose CRL expires breaks revocation checking for every intermediate (Windows reports `CRYPT_E_NO_REVOCATION_CHECK` or offline). Put the next-CRL date in the team calendar.
Verify:
- [ ] `openssl crl -in root.crl -noout -nextupdate` is more than 60 days away.
- [ ] Ceremony logs, hash records and two backups are present.
