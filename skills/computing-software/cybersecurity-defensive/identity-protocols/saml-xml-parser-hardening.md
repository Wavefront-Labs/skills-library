---
id: computing-software.cybersecurity-defensive.identity-protocols.saml-xml-parser-hardening
name: saml-xml-parser-hardening
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [saml-xml-parser-hardening, saml-security-considerations, xxe, dtd, billion-laughs, xml-parser, secure-processing, identity-protocols]
level: advanced
status: draft
description: "Harden SAML message parsing: disable DTDs and external entities, limit size and depth, avoid XXE and billion laughs, and decompress with limits."
sources:
  - https://docs.oasis-open.org/security/saml/v2.0/saml-sec-consider-2.0-os.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# XML parser hardening for SAML endpoints

Goal: make the ACS endpoint safe to expose.

Method:
- Disable DOCTYPE or external entity resolution (Java: `XMLConstants.FEATURE_SECURE_PROCESSING`, `disallow-doctype-decl`; Python: use `defusedxml`; .NET: `DtdProcessing.Prohibit`).
- Cap request size (for example 512 KB) and nesting depth.
- For Redirect binding cap the inflated size and use streaming inflation.
- Validate against the schema before processing.
- Run signature verification before any other processing of attributes.

Gotchas:
- A SAML response is parsed before authentication; XXE here is pre-auth.
- XSLT and XPath transforms in ds:Transforms can run attacker-chosen code on old libraries; allow-list the two expected transforms.
- Do not log decoded assertions containing sensitive attributes.

Verify: send a payload with an external entity in a lab and confirm it is rejected.
