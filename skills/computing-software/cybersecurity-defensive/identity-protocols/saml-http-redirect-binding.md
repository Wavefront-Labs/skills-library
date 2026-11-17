---
id: computing-software.cybersecurity-defensive.identity-protocols.saml-http-redirect-binding
name: saml-http-redirect-binding
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [saml-http-redirect-binding, saml-bindings, http-redirect, deflate, sigalg, signature, query-string, saml-request, identity-protocols]
level: advanced
status: docs-checked
description: "Encode and sign a SAML message on the query string: DEFLATE, base64, URL-encode, then SigAlg and Signature over the exact query string."
sources:
  - https://docs.oasis-open.org/security/saml/v2.0/saml-bindings-2.0-os.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTTP Redirect binding

Goal: send requests (and logout messages) by GET.

Method: serialise the XML, remove any ds:Signature from the message, DEFLATE it (RFC 1951), base64-encode with whitespace removed, then URL-encode into `SAMLRequest=` (or `SAMLResponse=`), plus `RelayState` (URL-encoded) if any. To sign, add `SigAlg=<alg URI>` and compute the signature over the string `SAMLRequest=value&RelayState=value&SigAlg=value` (each value URL-encoded, in that order; leave RelayState out entirely when absent), then add `Signature=` (base64, URL-encoded as needed). DSAwithSHA1 and RSAwithSHA1 must be supported by the binding.

Gotchas:
- Verify against the original URL-encoded values received on the query string, not a re-encoded form: URL-encoding is not canonical, so a re-encoding may not match the signer's.
- The parameters may arrive in any order; order them as the signing rules require before verifying.
- Messages that contain signed content, such as signed assertions, should not use this encoding because of their length.
- RelayState must not exceed 80 bytes and should be integrity protected by its creator.

Verify: decode a captured URL with a script and compare the signature input.

## Checked
Method: 2026-11-09 documentation only; no commands were run. Converted SAML V2.0 Bindings to text and read section 3.4 (HTTP Redirect binding: RelayState, DEFLATE encoding steps, SigAlg and Signature construction, verification notes). Removed the 2-8 KB URL size figure and the decompression-bomb advice (neither stated there).
