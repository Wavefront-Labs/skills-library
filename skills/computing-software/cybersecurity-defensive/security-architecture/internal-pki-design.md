---
id: computing-software.cybersecurity-defensive.security-architecture.internal-pki-design
name: internal-pki-design
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [cryptography, internal-pki, certificate-authority, offline-root-ca, issuing-ca, adcs, smallstep, crl, ocsp, certificate-templates]
level: advanced
status: draft
description: "Design an internal PKI: offline root, issuing CAs, templates/profiles, revocation (CRL/OCSP), key protection in HSMs, and the operational runbooks."
sources: ["CompTIA Security+ SY0-701 objective 1.4 (PKI, certificate authorities, CRL, OCSP)", "Microsoft Learn - AD CS design and PKI best practices", "RFC 5280 X.509 certificate and CRL profile"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Internal PKI design

**Goal:** a certificate authority hierarchy that issues device, user and service certificates
securely, can revoke them, and survives a compromised issuing CA.

## Hierarchy
- **Offline root CA**: powered off, not networked, key in an HSM or at least encrypted and
  stored in a safe. Validity 15-20 years. Signs only subordinate CAs and its CRL (republish
  CRL before expiry, e.g. every 6-12 months, via a documented ceremony).
- **Issuing (subordinate) CAs**: online, validity about half the root's; separate CAs per
  purpose or security zone if needed (e.g. users/devices vs servers).
- Two tiers is right for most organisations; three only for complex delegation.

## Implementation choices
- Windows estates: AD CS Enterprise issuing CAs with autoenrolment via GPO.
- Cloud-native/DevOps: AWS Private CA, Google CAS, Azure Key Vault + a CA, smallstep `step-ca`,
  HashiCorp Vault PKI for short-lived service certificates.

## Profiles / templates
- Minimal EKUs per purpose (serverAuth, clientAuth, smartcardLogon). Never include "Any Purpose".
- Key sizes: RSA 3072+/ECDSA P-256+ for new CAs; SHA-256 or better.
- Subject from the directory, not from the requester, unless approval is required.
- Short validity for automated certs (days to 90 days), longer only where renewal is manual.

## Revocation
- Publish CRLs at HTTP CDPs reachable by all relying parties (not only LDAP); OCSP for large estates.
- Delta CRLs for frequent revocation; monitor CRL expiry: an expired CRL breaks validation everywhere.

## Protect the CA
- Issuing CA servers are tier 0: same protection as domain controllers.
- HSM-backed keys, M-of-N for root operations, documented ceremonies with witnesses and logs.
- Audit issuance (AD CS events 4886/4887) and alert on unusual templates or requesters.

## Gotchas
- AD CS template misconfigurations (enrollee supplies subject, broad enrol rights) give domain escalation: see AD CS hardening.
- Root validity shorter than subordinate validity causes silent failures later.
- Forgetting the root CRL republish date breaks the entire PKI on that date.

## Verify
- [ ] `certutil -verify -urlfetch <cert>` succeeds from clients in each network zone.
- [ ] CRL/OCSP expiry monitored; ceremony calendar maintained.
