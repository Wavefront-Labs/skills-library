---
id: computing-software.cybersecurity-defensive.identity-protocols.saml-relaystate-handling
name: saml-relaystate-handling
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [saml-relaystate-handling, saml-web-sso-profile, relaystate, deep-link, return-url, open-redirect, identity-protocols]
level: practitioner
status: docs-checked
description: "Carry the original deep link through SAML SSO using server-side state keyed by RelayState, and avoid open redirects and size limits."
sources:
  - https://docs.oasis-open.org/security/saml/v2.0/saml-profiles-2.0-os.pdf
  - https://docs.oasis-open.org/security/saml/v2.0/saml-bindings-2.0-os.pdf
  - https://docs.oasis-open.org/security/saml/v2.0/saml-sec-consider-2.0-os.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Preserving return URL across SSO

Goal: bring users back to the page they requested.

Method: store the target URL server-side under a random key, send the key as RelayState, and after the ACS validates the response look up the key and redirect. The bindings spec says RelayState must not exceed 80 bytes and should be integrity protected by its creator, and the security considerations say it should also be confidentiality protected (symmetric primitives can be used because the same entity produces and consumes it). A random key looked up server-side is one way to meet that.

Gotchas:
- Passing a raw URL as RelayState allows open redirects after login; restrict to paths you expect (practice).
- No mechanism protects the pairing of RelayState with the SAML message, so do not attach sensitive state to it.
- IdP-initiated logins may carry a RelayState agreed with the SP, which can be the URL of a resource at the SP; handle it separately.

Verify: tamper with RelayState and confirm the SP falls back to a default landing page.

## Checked
Method: 2026-11-09 documentation only; no commands were run. Read SAML V2.0 Bindings 3.4.3 and 3.5.5.2 (80 byte limit, integrity protection, RelayState pairing), Security Considerations 6.4.6 (integrity and confidentiality protection) and Profiles 4.1.5. Removed the few-minutes retention and multi-tab cookie claims (not stated); added the bindings and security considerations PDFs as sources.
