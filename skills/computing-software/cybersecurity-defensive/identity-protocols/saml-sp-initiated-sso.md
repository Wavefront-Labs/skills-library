---
id: computing-software.cybersecurity-defensive.identity-protocols.saml-sp-initiated-sso
name: saml-sp-initiated-sso
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [saml-sp-initiated-sso, saml-web-sso-profile, sp-initiated, web-sso, acs, authnrequest, flow, identity-protocols]
level: practitioner
status: docs-checked
description: "Walk the SP-initiated Web Browser SSO flow step by step and the checks the SP performs on the response."
sources:
  - https://docs.oasis-open.org/security/saml/v2.0/saml-profiles-2.0-os.pdf
  - https://docs.oasis-open.org/security/saml/v2.0/saml-core-2.0-os.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SP-initiated Web SSO flow

Goal: understand and test the recommended SAML flow.

Steps:
1. User requests a protected resource; SP stores target URL, generates AuthnRequest with a fresh ID and remembers it.
2. The SP sends the AuthnRequest to the IdP's SSO endpoint through the browser (commonly the Redirect binding), with RelayState if used.
3. IdP authenticates the user (or relies on a session) and returns a Response to the ACS through a binding such as POST (assertions delivered by POST must be signed) or Artifact.
4. SP validates: signatures on the assertion or response, Recipient, NotOnOrAfter, InResponseTo equal to its AuthnRequest ID, audience and other conditions; a bearer assertion must not be replayed.
5. SP creates a local session and sends the browser to the target.

Gotchas:
- Keep the ID of each AuthnRequest until its response arrives; without it you cannot check InResponseTo, so the state must be reachable from whichever node receives the ACS POST (practice).
- An assertion or response that is not valid, or whose subject confirmation cannot be met, should be discarded and not used to establish a security context.

Verify: HAR capture shows exactly one POST to the ACS and a Set-Cookie afterwards.

## Checked
Method: 2026-11-09 documentation only; no commands were run. Read SAML V2.0 Profiles section 4.1 (Web Browser SSO steps, AuthnRequest and Response usage, response processing rules, POST-specific rules). Removed the signed-cookie advice and the process-only-the-signed-element rule (not stated there); the Redirect-then-POST pairing is now described as a common choice, since the profile allows other bindings.
