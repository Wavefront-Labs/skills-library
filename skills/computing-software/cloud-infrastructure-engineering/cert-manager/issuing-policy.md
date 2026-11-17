---
id: computing-software.cloud-infrastructure-engineering.cert-manager.issuing-policy
name: issuing-policy
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [issuing-policy, issuer, selfsigned, ca, letsencrypt, csr-mapping]
level: intro
status: docs-checked
description: "Know that each cert-manager issuer decides what issued certificates look like: SelfSigned and CA copy everything, Let's Encrypt applies its own rules."
sources:
  - https://cert-manager.io/docs/policy/issuing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each issuer decides what its certificates contain and which properties they carry. cert-manager enforces no mapping between a CertificateRequest or CertificateSigningRequest and the issued certificate. The one fixed rule: the public key in the issued certificate must match the key in the request.

Per issuer:
- SelfSigned and CA: cert-manager implements the policy itself. It is simple and not configurable: all requested properties are copied into the certificate.
- Let's Encrypt (ACME): its own, more complex policy. It always issues 90-day validity and supports only a limited set of (extended) key usages.

Practical consequences:
- Let's Encrypt issues 90 day certificates regardless of the requested lifetime.
- Because SelfSigned and CA copy everything, they do not constrain what a requester asks for.
- Other issuers have full autonomy over what their certificates look like.

## Checked

2026-11-03: Confirmed against the Issuing Policy page: issuers decide certificate contents, only the public key must match, SelfSigned and CA copy all requested properties and are not configurable, and Let's Encrypt always issues 90 day certificates with a limited set of (extended) key usages. Removed: the claims that ACME issuers may ignore `duration`, that approval policy is the fix, and that Vault, CyberArk and external issuers override CSR properties (the page says only that each issuer has full autonomy).

Method: documentation only; no commands were run.
