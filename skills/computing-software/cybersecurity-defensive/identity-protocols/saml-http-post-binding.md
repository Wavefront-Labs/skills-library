---
id: computing-software.cybersecurity-defensive.identity-protocols.saml-http-post-binding
name: saml-http-post-binding
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [saml-http-post-binding, saml-bindings, http-post, relaystate, samlresponse, form, acs, identity-protocols]
level: practitioner
status: docs-checked
description: "Deliver SAML messages with an auto-submitting HTML form: base64 SAMLResponse, RelayState handling, and CSRF and caching precautions."
sources:
  - https://docs.oasis-open.org/security/saml/v2.0/saml-bindings-2.0-os.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTTP POST binding and RelayState

Goal: use the standard binding for assertions.

Method: the sender returns an HTML form with hidden fields `SAMLResponse` (base64 of XML, no deflate) and optional `RelayState`, posted to the ACS URL, usually auto-submitted by a script. Signatures are embedded (enveloped XML signature).

- RelayState must not exceed 80 bytes and should be integrity protected by the sender; a responder must return the exact value it received. No mechanism protects the pairing of RelayState with the SAML message, so do not attach sensitive state to it. Treat it as untrusted input: map it to a server-side stored return URL or validate it against an allow-list to avoid open redirects.
- Responders should send `Cache-Control: no-cache, no-store` and `Pragma: no-cache` with the form page.
- The spec examples include a `noscript` block with a submit button for browsers without JavaScript.

Gotchas:
- If the message is signed, its `Destination` must equal the URL where it was received; the recipient must check it.
- Do not use HTTP error status codes for SAML failures; return a SAML Status (for a refusal, second-level `RequestDenied`).
- The binding gives no confidentiality from the user agent; use TLS if the content must be protected in transit.

Verify: complete a login with browser dev tools and confirm RelayState round-trips.

## Checked
Method: 2026-11-09 documentation only; no commands were run. Converted SAML V2.0 Bindings to text and read section 3.4.3 (RelayState 80 bytes) and 3.5 (HTTP POST binding: hidden form controls, base64, signing, caching headers, security considerations, error reporting). Removed the CSP form-action and SameSite cookie gotchas (not in the spec).
