---
id: computing-software.cybersecurity-defensive.identity-protocols.saml-enveloped-signature
name: saml-enveloped-signature
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [saml-enveloped-signature, saml-xml-signature, xmldsig, enveloped-signature, reference, canonicalization, exc-c14n, identity-protocols]
level: advanced
status: docs-checked
description: "Sign a SAML Response or Assertion with an enveloped XML signature whose Reference URI points at the signed element ID, with exclusive canonicalisation."
sources:
  - https://docs.oasis-open.org/security/saml/v2.0/saml-core-2.0-os.pdf
  - https://www.w3.org/TR/xmldsig-core1/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enveloped signature and Reference URI

Goal: sign and verify correctly.

Method (SAML Core 2.0 section 5.4): SAML assertions and protocol messages MUST use enveloped signatures. The signed root element MUST carry an `ID`; the `ds:Signature` is a child of that element and sits after `saml:Issuer` (Issuer then Signature in the schema order). The signature MUST contain a single `ds:Reference` with a same-document URI `#<ID>` of the element being signed. Core says implementations SHOULD use exclusive canonicalisation (`http://www.w3.org/2001/10/xml-exc-c14n#`, with or without comments) in `ds:CanonicalizationMethod` and as a `ds:Transform`, and SHOULD NOT use transforms other than `http://www.w3.org/2000/09/xmldsig#enveloped-signature` and exclusive c14n. Verifiers MAY reject other transforms; if they accept them they MUST ensure no content of the message is excluded from the signature.

- `ds:KeyInfo` may be absent (Core does not require it), so the verifier must know the issuer's key from agreed configuration.
- Sign the Assertion, the Response, or both; agree with the peer which one is required.
- For algorithm choice see saml-signature-algorithms.

Gotchas:
- Verify the signature, then read data only from the element the signature covered, never re-query the document by name.
- Your XML library must be told which attribute is the ID type, or the Reference cannot be resolved.

Verify: alter one character of the assertion and confirm validation fails.

## Checked

2026-11-09. Confirmed in SAML Core 2.0 sections 5.4.1 to 5.4.5 (enveloped, single Reference, exc-c14n, transforms, KeyInfo optional) and the schema listing of `ds:Signature` after `Issuer` in Assertion. Removed: WantAssertionsSigned (a metadata attribute, not in the cited pages), setIdAttribute (library-specific), whitespace/pretty-print claim.
Method: documentation only; no commands were run.
