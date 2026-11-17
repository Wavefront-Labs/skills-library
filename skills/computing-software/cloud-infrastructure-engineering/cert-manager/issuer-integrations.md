---
id: computing-software.cloud-infrastructure-engineering.cert-manager.issuer-integrations
name: issuer-integrations
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [issuers, external-issuers, in-tree, tiers, awspca, google-cas, ejbca]
level: intro
status: docs-checked
description: "Choose a cert-manager issuer: the five in-tree types, known third-party integrations, and how the docs tier them by maintenance and tutorials."
sources:
  - https://cert-manager.io/docs/configuration/issuers/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The issuers page is a catalogue, not a how-to. It does not explain Issuer versus ClusterIssuer scoping;.

In-tree issuers, shipped with cert-manager: ACME, CA, SelfSigned, Vault and Venafi TLS Protect.

Known third-party examples: CyberArk Certificate Manager (venafi-enhanced-issuer), Cloudflare Origin CA, AWS Private CA, Google CAS, EJBCA, step-issuer, Azure Key Vault; targets also include Microsoft ADCS, AWS KMS, FreeIPA, ZeroSSL and CFSSL.

Tiers, sorted by tier then name:
- Production-ready: has an end-to-end tutorial on a supported cert-manager version covering install, issuer setup, custom resource configuration and issuing a Certificate.
- Maintained: a release within the last 12 months.
- Unmaintained: everything else.

Flags in the table: venafi-enhanced-issuer and cview-issuer are not open source; tcs-issuer, freeipa-issuer, kms-issuer and keyvault-issuer had no release in 12 months. Tier criteria can change, and the production-ready check was last done October 3, 2024.

A footnote says listed issuers are known to support and honor approval, without naming which.

## Checked

2026-11-03: Confirmed against the Issuers page: in-tree issuers marked on the page (ACME, CA, Self-Signed, Vault, Venafi TLS Protect), the named third-party issuers and targets, the three tiers and their criteria, the not-open-source flags (venafi-enhanced-issuer, cview-issuer), the issuers with no release in 12 months, tier criteria being changeable, the 3 October 2024 check date, and the approval footnote. Removed: the parenthetical about Issuer and ClusterIssuer Secret namespace rules (not on this page) and the "(CyberArk)" label on the in-tree Venafi issuer (the page says Venafi TLS Protect).

Method: documentation only; no commands were run.
