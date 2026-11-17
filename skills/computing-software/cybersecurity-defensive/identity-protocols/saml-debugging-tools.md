---
id: computing-software.cybersecurity-defensive.identity-protocols.saml-debugging-tools
name: saml-debugging-tools
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [saml-debugging-tools, saml-conformance-interop, saml-tracer, xmlsec1, openssl, har, decode, identity-protocols]
level: practitioner
status: draft
description: "Decode and verify SAML messages with browser SAML tracer extensions, xmlsec1, openssl and metadata validators without leaking assertions."
sources:
  - https://docs.oasis-open.org/security/saml/v2.0/saml-conformance-2.0-os.pdf
  - https://kantarainitiative.github.io/SAMLprofiles/saml2int.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SAML debugging and signature tools

Goal: inspect messages quickly and safely.

Method:
- Capture with a SAML tracer browser extension or HAR export; Redirect payloads: base64-decode then raw inflate (`python -c "import zlib,base64,sys;print(zlib.decompress(base64.b64decode(sys.argv[1]),-15))"`); POST payloads: base64-decode only.
- Verify a signature: `xmlsec1 --verify --pubkey-cert-pem idp.pem --id-attr:ID urn:oasis:names:tc:SAML:2.0:assertion:Assertion msg.xml`.
- Check certificate dates: `openssl x509 -in idp.pem -noout -dates -fingerprint -sha256`.
- Validate metadata against the OASIS XSD with `xmllint --schema`.

Gotchas:
- Assertions in HAR files are bearer credentials until they expire; scrub or delete captures.
- Never paste live assertions into online decoder sites.
- Pretty-printing breaks signatures; verify the raw bytes.

Verify: the decoded request shows the expected Issuer and ACS URL.
