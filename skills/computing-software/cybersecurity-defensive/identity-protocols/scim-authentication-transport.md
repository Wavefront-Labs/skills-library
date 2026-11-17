---
id: computing-software.cybersecurity-defensive.identity-protocols.scim-authentication-transport
name: scim-authentication-transport
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [scim-authentication-transport, scim-operations-security, scim-auth, bearer-token, oauth, tls, rate-limit, least-privilege, identity-protocols]
level: practitioner
status: docs-checked
description: "Secure a SCIM endpoint: TLS 1.2+, OAuth bearer token or long-lived secret rotation, least-privilege scopes, rate limits, and logging without personal data."
sources:
  - https://www.rfc-editor.org/rfc/rfc7644#section-7
  - https://www.rfc-editor.org/rfc/rfc7642
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SCIM authentication, authorization and transport

Goal: prevent the provisioning API becoming an account-creation backdoor.

Method (from RFC 7644 sections 2 and 7):
- Require TLS for all SCIM traffic. The service provider MUST support TLS 1.2; the client MUST perform a TLS server identity check (RFC 6125).
- Bearer tokens (RFC 6750) and cookies MUST be sent over TLS, MUST contain enough entropy to resist guessing, and bearer tokens MUST have a limited lifetime that the service provider can determine. OAuth token refresh is the RFC's example of obtaining a new token.
- Authentication and authorization methods are out of scope for SCIM. HTTP Basic is the default authentication for OAuth bearer tokens and the RFC encourages stronger methods. The RFC also mentions TLS client authentication as an option.
- Advertise the schemes in `authenticationSchemes` (`type` is one of `oauth`, `oauth2`, `oauthbearertoken`, `httpbasic`, `httpdigest`).

Gotchas:
- If a service provider accepts anonymous requests such as a create, RFC 7644 section 7.6 sets out the risks; unauthenticated create is the opposite of this skill's goal.
- A token that can authorise reading, modifying or deleting resources is high value; RFC 7644 7.4 requires the entropy and lifetime rules above.

Verify: rotate the token and confirm the IdP reconnects using a test sync.

## Checked
2026-11-02. Confirmed against RFC 7644 sections 2, 7.2 to 7.4 and RFC 7643 section 5 (`authenticationSchemes`). Removed: "no HTTP redirect", "TLS 1.2+" (RFC says MUST support 1.2), 32 random bytes, secret-manager and rotation advice, scope and role design, rate limiting, IP restriction, logging and allow-list advice, none of which the RFCs state.
Method: documentation only; no commands were run.
