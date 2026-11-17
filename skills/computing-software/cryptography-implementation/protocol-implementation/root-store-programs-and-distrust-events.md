---
id: computing-software.cryptography-implementation.protocol-implementation.root-store-programs-and-distrust-events
name: root-store-programs-and-distrust-events
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, root-store, ca-distrust, ccadb, chrome-root-store, mozilla-nss, trust-store, certifi, certificate-validation, webpki]
level: practitioner
status: draft
description: "Track root store programs (Mozilla, Chrome, Apple, Microsoft) and CA distrust events, check exposure of your certificates and clients, and update bundled trust stores."
sources: ["https://www.ccadb.org/", "https://g.co/chrome/root-policy", "https://wiki.mozilla.org/CA"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Root store programs and distrust events

## Programs
| Program | Used by |
|---|---|
| Mozilla NSS | Firefox, most Linux distributions' ca-certificates, certifi (Python), Node's bundled roots |
| Chrome Root Store | Chrome on all platforms since 2022-2023 |
| Apple Root Program | iOS, macOS, Safari |
| Microsoft Trusted Root Program | Windows, Edge (with its own checks) |
CCADB is the shared database where CAs disclose roots, intermediates and audits.

## Distrust events (patterns)
- Gradual distrust by issuance date: certificates issued after a cutoff stop being trusted while older ones run out
  (Symantec 2018; Entrust in Chrome for certificates issued after 11 Nov 2024; others since).
- Root expiry: ISRG/IdenTrust cross-sign expiry in 2021 broke old Android, OpenSSL 1.0.x and embedded clients with
  frozen stores.

## When a distrust is announced
1. Inventory certificates by issuing CA (CT search for your domains, internal scans) and find any from the affected CA.
2. Re-issue from another CA before the cutoff; update CAA records.
3. For clients and devices you ship: check which trust store they use and whether the change affects them.

## Keeping bundled stores fresh
- certifi (Python), Node bundled roots, Java cacerts and Go-on-scratch images (`ca-certificates.crt` copied in) are
  snapshots; update them with dependency upgrades.
- Embedded devices: plan trust store updates in firmware; include more than one root so a single expiry or distrust
  does not brick connectivity.

## Verify
- [ ] Certificate inventory shows issuing CA for every public certificate.
- [ ] Dependency bot updates certifi/ca-certificates regularly.
