---
id: computing-software.systems-network-administration.pki-tls-administration.crypto-inventory-agility
name: crypto-inventory-agility
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [crypto-inventory-agility, pki-pqc-migration, crypto-agility, cbom, algorithm-deprecation, migration-plan, pki-tls-administration]
level: practitioner
status: draft
description: "Create a cryptographic bill of materials, find hardcoded algorithms and plan staged algorithm and CA migrations."
sources:
  - https://csrc.nist.gov/pubs/sp/800/131/a/r2/final
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cryptographic inventory and agility plan
Goal: be able to change algorithms and CAs on a schedule, not in a crisis.
1. Inventory: certificates (see inventory), TLS configs, SSH keys, code-signing keys, VPNs, databases, libraries with `openssl`/`bcprov` dependencies. Use CycloneDX CBOM format where possible.
2. Classify by data lifetime and exposure; long-lived confidential data goes first.
3. Find hardcoded choices: pinned hashes, cert pinning, `SHA1withRSA` strings, fixed key sizes.
4. Abstract: central TLS config templates, no per-app cipher lists, certificate files fetched from a secrets store.
5. Migration pattern: dual-publish (ECDSA + RSA, or classical + hybrid), measure, then retire the old.
6. SP 800-131A Rev 2 lists algorithm transitions (SHA-1 and 2-key 3DES disallowed; confirm Rev 3 status).
Test environments with a private CA that issues the new profile.
Gotcha: certificate pinning in mobile apps is the biggest blocker to CA rotation; ship dual pins or move to pinning the CA key.
Verify:
- [ ] CBOM covers all internet-facing and CA systems.
- [ ] Each deprecated algorithm has an owner and retirement date.
