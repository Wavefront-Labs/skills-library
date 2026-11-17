---
id: computing-software.cybersecurity-defensive.identity-access-management.oauth-grant-types
name: oauth-grant-types
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [oauth-grant-types, oauth2, authorization-code-pkce, client-credentials, device-authorization-grant, oauth-2-1, federation-protocols, oauth-grant-selection, oauth-grant-selection]
level: practitioner
status: docs-checked
description: "Choose the right OAuth 2.0 grant per client type: auth code + PKCE, client credentials, device flow, token exchange, and why implicit and password grants are retired."
sources: ["https://datatracker.ietf.org/doc/html/rfc9700", "https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/", "https://datatracker.ietf.org/doc/html/rfc8628", "https://datatracker.ietf.org/doc/html/rfc7636"]
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# OAuth 2.0 grant type selection

| Client | Grant | Notes |
|---|---|---|
| Server-side web app (confidential) | Authorization code + PKCE | PKCE with method `S256` |
| SPA / browser app (public) | Authorization code + PKCE | Or a backend-for-frontend (BFF) holding tokens server-side - preferred for sensitive apps |
| Native/mobile app | Authorization code + PKCE with the system browser | Avoid embedded user agents (see the OAuth 2.1 draft security considerations) |
| Service/daemon, no user | Client credentials | Prefer private_key_jwt or mTLS client auth over shared secret; or workload identity federation |
| Input-constrained device (TV, CLI) | Device authorization grant (RFC 8628) | Enable only where needed |
| Service acting for a user downstream | Token exchange / on-behalf-of | Down-scope audience |
| **Implicit** | Do not use | Omitted from the OAuth 2.1 draft (`response_type=token`) |
| **Resource owner password (ROPC)** | Do not use | Omitted from the OAuth 2.1 draft |

## Configuration checks
- Exact string matching of redirect URIs (OAuth 2.1 draft); no wildcards.
- `state` (or PKCE + OIDC `nonce`) to prevent CSRF/code injection; PKCE method `S256` only.
- Short-lived access tokens.
- Scopes minimal; audience-restricted tokens per API.
- Consider sender-constrained tokens (DPoP RFC 9449 or mTLS RFC 8705) for high-value APIs.

## Verify
- [ ] App registration inventory: no implicit grant enabled, no ROPC clients.
- [ ] Each client's grant matches the table.

## Checked

2026-10-28. Confirmed: RFC 9700 (asymmetric client authentication such as mTLS or private key JWT; `nonce` against code injection); OAuth 2.1 draft (implicit and ROPC omitted, exact redirect matching, `S256`, backend-for-frontend recommendation, DPoP RFC 9449 and mTLS RFC 8705 sender-constrained tokens, embedded user agents section); RFC 8628 and RFC 7636 titles. Removed: the RFC 9700 PKCE-for-confidential-clients attribution, RFC 8693 number, token lifetime figure, refresh-rotation claim, device-code phishing and Entra Conditional Access statements, and the `oauth2AllowImplicitFlow` setting name.
Method: documentation only; no commands were run.
