---
id: computing-software.cybersecurity-defensive.pomerium.tls-cipher-baseline
name: tls-cipher-baseline
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [tls-ciphers, tls-1-2, downstream-tls, upstream-tls, hsts]
level: advanced
status: docs-checked
description: "Reference the TLS versions, cipher suites and curves Pomerium accepts downstream and upstream, for compliance and scanner reviews."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/internals/security.md
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/internals/connection.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Downstream (client to Pomerium)**: minimum TLS 1.2. TLS 1.2 suites, in order: ECDHE-ECDSA-AES256-GCM-SHA384, ECDHE-RSA-AES256-GCM-SHA384, ECDHE-ECDSA-AES128-GCM-SHA256, ECDHE-RSA-AES128-GCM-SHA256, ECDHE-ECDSA-CHACHA20-POLY1305, ECDHE-RSA-CHACHA20-POLY1305. Curves: X25519, NIST P-256.

**Upstream (Pomerium to app)**: minimum TLS 1.2. Supports those six suites plus ECDHE-ECDSA-AES128-SHA, ECDHE-RSA-AES128-SHA, AES128-GCM-SHA256, AES128-SHA, ECDHE-ECDSA-AES256-SHA, ECDHE-RSA-AES256-SHA, AES256-GCM-SHA384 and AES256-SHA. Curves: X25519, P-256, P-384, P-521. HSTS with a long duration is on by default. Mutual TLS is used when client certificates are provided.

**Hosted control plane**: Pomerium proxy to the control plane uses TLS 1.3. The Zero web console is minimum TLS 1.2 and prefers 1.3.

The connection page also states that minimum TLS requirements are fixed and not configurable.

If a scanner flags the legacy CBC or non-AEAD suites, note that the documented lists put them on the upstream leg and the Zero web console, while the downstream listener offers only the six AEAD suites.

## Checked

2026-11-04. Read the Security and Threat Model page and the Connections page: downstream and upstream versions, suite lists and order, curves, HSTS default, mutual TLS, hosted control plane TLS 1.3 and Zero console minimum, and the non-configurable minimum all confirmed. Reworded the final scanner note, which wrongly implied the Zero web console is limited to AEAD suites.

Method: documentation only; no commands were run.
