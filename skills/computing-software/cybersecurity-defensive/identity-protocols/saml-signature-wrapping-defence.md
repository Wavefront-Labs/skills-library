---
id: computing-software.cybersecurity-defensive.identity-protocols.saml-signature-wrapping-defence
name: saml-signature-wrapping-defence
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [saml-signature-wrapping-defence, saml-xml-signature, xsw, signature-wrapping, xml-security, duplicate-id, identity-protocols]
level: sme
status: docs-checked
description: "Prevent XSW attacks on SAML consumers: process only the signed element, require one Reference matching the root ID, and reject duplicate IDs."
sources:
  - https://docs.oasis-open.org/security/saml/v2.0/saml-core-2.0-os.pdf
  - https://www.w3.org/TR/xmldsig-core1/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# XML signature wrapping defence

Goal: ensure the data you trust is the data that was signed.

Method:
- SAML Core 2.0 (section 1.3.4, identifiers) says that where a data object declares an identifier there MUST be exactly one such declaration: reject any document with duplicate `ID` values.
- Section 5.4.2: the signed root element MUST carry an `ID`, and the signature MUST contain a single `ds:Reference` with a same-document URI equal to `#` plus that ID. Require exactly one Reference, and require that it points at the Response or Assertion you are about to consume.
- XML Signature 1.1 section 8.1.3 ("See" what is signed): operate over the data that was transformed and signed, not the original document. In practice, resolve the Reference to a specific node and pass that verified node on, not the document root, and never re-query the document by element name or position.
- Section 5.4.4 of Core: signatures SHOULD NOT use transforms other than enveloped-signature and exclusive c14n; verifiers MAY reject others, and if they accept them MUST ensure no message content is excluded from the signature.
- XML Signature 1.1 section 8.3 warns that executable content such as XSLT transforms can cause unacceptable processing or memory demand; allow-list the two expected transforms.

Gotchas:
- XML Signature 1.1 section 8.1.1: "only what is signed is secure"; a signature over one element does not protect other elements in the same document, so anything outside the verified node is attacker-controlled input.
- Do not roll your own verifier; use a maintained XML signature library and keep it patched.

Verify: run a signature-wrapping test set against your SP in a lab (move the signed assertion elsewhere and add an unsigned one; both must be rejected).

## Checked

2026-11-09. Confirmed in SAML Core 2.0 (identifier uniqueness, sections 5.4.2 and 5.4.4) and W3C XML Signature 1.1 (sections 8.1.1, 8.1.3, 8.3). Removed: claims about attack layouts (Extensions/Object relocation, XPath picking the first assertion), comment-injection truncation, past library bug classes, and schema-validation requirement, none of which the cited pages state.
Method: documentation only; no commands were run.
