---
id: computing-software.cybersecurity-defensive.identity-access-management.token-lifetime
name: token-lifetime
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [token-lifetime, refresh-token-revocation, session-lifetime, sign-in-frequency, continuous-access-evaluation, oauth-tokens, federation-protocols, token-lifetime-and-revocation, token-lifetime-and-revocation]
level: practitioner
status: draft
description: "Set token and session lifetimes and revoke refresh tokens on compromise: access vs refresh vs session cookies, sign-in frequency, CAE, and per-IdP revocation commands."
sources: ["https://learn.microsoft.com/en-us/entra/identity-platform/refresh-tokens", "https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-session-lifetime", "https://developer.okta.com/docs/guides/revoke-tokens/main/", "https://datatracker.ietf.org/doc/html/rfc7009"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Token lifetimes and refresh token revocation

## Token types
| Token | Typical lifetime | Revocation |
|---|---|---|
| Access token (JWT) | 60-90 min (Entra), configurable elsewhere | Usually not revocable before expiry (self-contained) unless CAE-aware or introspected |
| Refresh token | Entra: 90 days sliding (24 h for SPAs) | Revocable centrally |
| IdP session cookie | Browser session / persistent | Sign-out, session revoke |
| App session cookie | App-defined | App must check |

## Policy
- Use Conditional Access **sign-in frequency** (e.g. 4-12 h for admins/unmanaged devices) and disable persistent browser session on unmanaged devices, rather than custom token lifetimes.
- Enable **Continuous Access Evaluation** so CAE-aware services (Exchange, SharePoint, Teams, Graph) reject tokens on user disable, password change, risk or IP change in near real time.
- Short access tokens (5-15 min) for your own APIs with introspection or revocation lists for high risk.

## Revoke on compromise
- Entra: `Revoke-MgUserSignInSession -UserId <upn>` (invalidates refresh tokens and session cookies); also reset password, disable account, remove/re-register MFA methods, review new devices and app consents.
- Okta: `DELETE /api/v1/users/{id}/sessions?oauthTokens=true`.
- Google Workspace: Admin console -> user -> Sign-in cookies -> Reset; revoke OAuth tokens per app.
- Generic OAuth: RFC 7009 `/revoke` endpoint for the refresh token.

## Gotchas
- Revoking refresh tokens does not kill already-issued access tokens for non-CAE apps; they live until expiry (up to ~1 h; CAE-capable tokens can last 28 h because they are revocable - make sure CAE is not disabled).
- Primary Refresh Tokens on devices: also disable/remove the device if it is compromised.
- Third-party SaaS with its own session ignores IdP revocation; terminate sessions in the app too.

## Verify
- [ ] Revocation runbook tested: after revoke, Outlook/Teams prompt within minutes.
- [ ] CA policies set sign-in frequency for privileged roles.
