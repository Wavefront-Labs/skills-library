---
id: computing-software.cybersecurity-defensive.identity-protocols.saml-idp-initiated-sso
name: saml-idp-initiated-sso
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [saml-idp-initiated-sso, saml-web-sso-profile, idp-initiated, unsolicited, login-csrf, relaystate, identity-protocols]
level: advanced
status: docs-checked
description: "Handle IdP-initiated SAML SSO safely: unsolicited responses carry no InResponseTo, so rely on the other checks; validate RelayState."
sources:
  - https://docs.oasis-open.org/security/saml/v2.0/saml-profiles-2.0-os.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IdP-initiated SSO and unsolicited responses

Goal: support app-portal launch tiles without losing the request binding SP-initiated SSO gives.

Method: the IdP delivers an unsolicited Response to the ACS with no preceding AuthnRequest. It must not contain an `InResponseTo` attribute, nor should any bearer SubjectConfirmationData, so the SP cannot bind it to a request. Rely on the other checks: signatures, `Recipient`, `NotOnOrAfter`, the audience restriction and the used-assertion-ID set. With metadata, the response should go to the SP's default AssertionConsumerService endpoint.

Gotchas:
- Because no request is remembered, an SP cannot tell a response it asked for from one pushed at it. Prefer SP-initiated flow where portal launch is not needed (practice).
- The IdP may send a binding-specific RelayState, agreed with the SP, that can be the URL of a resource at the SP; validate the target against an allow-list.
- The SP should be prepared to handle unsolicited responses by designating a default location to send the user.

Verify: submit a captured unsolicited response twice and from a second browser; the second must be rejected.

## Checked
Method: 2026-11-09 documentation only; no commands were run. Read SAML V2.0 Profiles 4.1.4.3-4.1.5 (unsolicited responses, InResponseTo rule, default ACS, RelayState, default location). Removed the login-CSRF scenario and its mitigation, and the advice about disabling unsolicited responses (not stated); description updated to match.
