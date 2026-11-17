---
id: computing-software.cybersecurity-defensive.identity-protocols.oidc-mix-up-and-idp-confusion
name: oidc-mix-up-and-idp-confusion
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oidc-mix-up-and-idp-confusion, oidc-security-considerations, mix-up, idp-confusion, iss-parameter, rfc9207, multi-idp, identity-protocols]
level: sme
status: docs-checked
description: "Defend RPs that talk to several OPs against mix-up attacks with per-OP redirect URIs, state bound to the OP, iss validation and RFC 9207."
sources:
  - https://www.rfc-editor.org/rfc/rfc9700.txt
  - https://www.rfc-editor.org/rfc/rfc9207.txt
  - https://openid.net/specs/openid-connect-core-1_0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IdP mix-up in OIDC clients

Goal: prevent the code from one OP being redeemed at another.

Method (clients that talk to two or more authorization servers):
- For each authorization request, store the issuer you sent the request to and bind it to the user agent. Storing only the authorization server URL is not sufficient.
- Defence 1: have the OP send its issuer in the response (the `iss` response parameter of RFC 9207, or the `iss` claim of an ID Token returned in the response) and compare it with the stored issuer by simple string comparison; abort on mismatch. OPs advertise the parameter with `authorization_response_iss_parameter_supported`; a client that knows the OP supports it must reject responses lacking `iss`.
- Defence 2: use a distinct redirect URI for each issuer (for example `/callback/<op>`) and check the response arrived at the URI for the stored issuer.
- After the token exchange, validate `iss` and `aud` in the ID Token against that same OP.

Gotchas:
- RFC 9700 says no mix-up defence is required when a client interacts with only one authorization server.
- Distinct redirect URIs do not work when a client registers once for many issuers.

Verify: start login with OP A and answer the callback with OP B's `iss`; the client must stop.

## Checked
2026-11-02. Confirmed against RFC 9700 section 4.4.2, RFC 9207 sections 2 to 4 and OpenID Connect Core 1.0 section 3.1.3.7. Removed: "bind state to the OP", the dynamic-discovery allow-list advice and the malicious-OP narrative, which these documents do not state in that form.
Method: documentation only; no commands were run.
