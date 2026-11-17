---
id: computing-software.software-engineering.api-design.oauth2-scopes-and-api-keys
name: oauth2-scopes-and-api-keys
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, api-contracts, oauth2-scopes, api-keys, api-security, client-credentials, owasp-api-security]
level: practitioner
status: draft
description: "Secure APIs with OAuth 2 scopes and API keys: scope design, client credentials vs authorization code, key format, hashing, rotation and object-level authorisation."
sources:
  - https://www.rfc-editor.org/rfc/rfc6749
  - https://datatracker.ietf.org/doc/html/rfc9700
  - https://owasp.org/API-Security/editions/2023/en/0x11-t10/
  - https://github.blog/engineering/platform-security/behind-githubs-new-authentication-token-formats/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# OAuth 2 scopes and API keys

## Choosing a mechanism
| Caller | Mechanism |
|---|---|
| User via web/mobile app | OAuth 2 authorization code + PKCE (RFC 9700 best current practice); access tokens short-lived |
| Server-to-server, no user | OAuth 2 client credentials, or mTLS / workload identity |
| Developer scripts, simple integrations | API keys (scoped, revocable) or personal access tokens |
| Third-party apps acting for users | OAuth with granular scopes and consent screen |
Implicit and password grants are deprecated (OAuth 2.1 drops them).

## Scope design
- Scopes limit what a token may do on behalf of the client; they are not a substitute for per-user permission checks.
- Granularity by resource and access: `orders:read`, `orders:write`, `refunds:create`. Avoid one `admin` scope and avoid hundreds of tiny scopes users cannot understand.
- Read/write split at minimum; sensitive actions (payouts, deleting accounts) get their own scopes.
- Document scopes per operation in OpenAPI `security: [{oauth2: [orders:read]}]`.
- Enforce at the resource server: validate token signature, `iss`, `aud`, expiry, then check required scope for the route; return 401 for bad/missing tokens (`WWW-Authenticate: Bearer error="invalid_token"`), 403 `insufficient_scope` for missing scope.

## API key design
- Format: prefix + random secret + optional checksum, e.g. `acme_live_<32+ random bytes base62>` - the prefix enables secret scanning (GitHub secret scanning partner program) and identifies environment.
- Generate with a CSPRNG; show once at creation.
- **Store only a hash** (SHA-256 is fine for high-entropy keys; keep the prefix/last 4 for display). Lookup by hash.
- Send in a header (`Authorization: Bearer <key>` or `X-API-Key`), never in query strings (logs).
- Per-key scopes, expiry, owner, last-used timestamp, IP allow-lists for high-value keys.
- Rotation: allow two active keys per client so they can roll without downtime; revoke immediately on leak.

## Authorisation beyond authentication (OWASP API Top 10 2023)
- **API1 Broken Object Level Authorization:** every request that takes an id checks the caller may access that object (`WHERE id = ? AND tenant_id = ?`). Scopes do not cover this.
- **API5 Broken Function Level Authorization:** admin routes check roles, not obscurity.
- **API3 Broken Object Property Level Authorization:** do not return or accept fields the caller should not see/set (mass assignment).

## Verify
- [ ] Tests: token without scope -> 403; another tenant's id -> 404/403; expired token -> 401.
- [ ] Keys stored hashed; secret scanning catches committed keys (push protection on).
