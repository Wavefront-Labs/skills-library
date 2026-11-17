---
id: computing-software.systems-network-administration.pki-tls-administration.root-intermediate-tiers
name: root-intermediate-tiers
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [root-intermediate-tiers, pki-hierarchy, pki, root-ca, intermediate-ca, pki-tls-administration]
level: practitioner
status: draft
description: "Design a two- or three-tier CA hierarchy: root, policy and issuing intermediates, how to split by purpose and lifetime, and what to avoid."
sources:
  - https://www.rfc-editor.org/rfc/rfc5280
  - https://www.rfc-editor.org/rfc/rfc3647
  - https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Root and intermediate CA tiers
Goal: a hierarchy where the root almost never touches the network and issuing CAs can be replaced without re-trusting everything.
- Two tier (offline root + online issuing CA) fits most organisations. Add a third (policy) tier only when you need separate administrative or legal domains.
- Split issuing CAs by purpose, not by team: one for TLS server, one for client/device, one for code signing. Each gets its own EKU constraints.
- Lifetimes: root 15-20 years, intermediate 5-10 years, leaf 90 days or less. An intermediate must outlive the leaves it signs by at least one renewal cycle.
- Naming: put the generation in the CN (`Example Issuing CA G2`) so replacements are visible.
- Keep the root key algorithm at least as strong as every subordinate (RSA 4096 or P-384).
Gotcha: cross-signing or a flat single-CA design looks simpler but makes a CA key compromise force re-trusting every client.
Verify:
- [ ] `openssl x509 -in issuing.pem -noout -text` shows `CA:TRUE, pathlen:0` for an issuing CA.
- [ ] Each tier has a documented purpose, lifetime and owner.
