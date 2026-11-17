---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth21-changes-from-2-0
name: oauth21-changes-from-2-0
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth21-changes-from-2-0, oauth-2-1, oauth-2.1, draft, pkce-required, implicit-removed, password-removed, identity-protocols]
level: practitioner
status: docs-checked
description: "List what OAuth 2.1 changes: PKCE required, implicit and password grants removed, exact redirect matching, no bearer tokens in query, refresh rules."
sources:
  - https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OAuth 2.1 differences from RFC 6749

Goal: know the target state of OAuth.

Changes (draft-ietf-oauth-v2-1-17, 31 October 2026, section 10; the list is non-normative):
- The authorization code grant incorporates PKCE: clients MUST use code_challenge and code_verifier and authorization servers MUST enforce them, except under the conditions of section 7.5.1 (even then enforcement is RECOMMENDED). The PKCE `plain` method is removed and prohibited.
- Redirect URIs are compared by exact string match (RFC 3986 simple string comparison). The one exception is loopback redirect URIs used by native apps, where the server MUST allow a variable port.
- The Implicit grant (`response_type=token`) is omitted; `response_type=token` is no longer defined. Other response types such as OpenID Connect `id_token` are unaffected.
- The Resource Owner Password Credentials grant is omitted.
- Bearer tokens must not be sent in the URI query string.
- Refresh tokens for public clients must be sender-constrained or one-time-use. Refresh tokens issued to browser-based applications have extra lifetime constraints.
- The `redirect_uri` parameter is dropped from the token request in the authorization code flow, since PKCE prevents code injection.
- Authorization servers must support client credentials in the request content (body).

Gotchas:
- It consolidates RFC 6749, RFC 8252 (native apps), RFC 7636 (PKCE), the browser-based apps BCP (RFC 10017), RFC 9700 (security BCP) and RFC 6750 (bearer tokens); it is not a new protocol. It would obsolete 6749 and 6750 if approved.
- It is still an Internet-Draft (intended Standards Track), so in compliance statements cite the individual RFCs. Re-check the current revision before relying on this list.
- A 2.0 client that skips PKCE, relies on redirect pattern matching, or uses implicit or password grants will not interoperate with a server enforcing these rules.

Verify: check each change against the current authorization server configuration.

## Checked

Method: 2026-11-09 docs-only; read draft-ietf-oauth-v2-1-17 (ietf.org archive text) section 10 and 10.1-10.2, the PKCE paragraph in 4.1.1 and redirect URI validation in 4.1.1. Removed the unsourced statement about the device grant.
