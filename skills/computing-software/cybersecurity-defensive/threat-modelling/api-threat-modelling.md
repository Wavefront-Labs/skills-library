---
id: computing-software.cybersecurity-defensive.threat-modelling.api-threat-modelling
name: api-threat-modelling
category: computing-software
field: cybersecurity-defensive
product: threat-modelling
tags: [threat-modelling, api-threat-modelling, owasp-api-top-10, bola, authorization, rate-limiting, stride]
level: practitioner
status: docs-checked
description: "Threat model APIs with the OWASP API Security Top 10 lens: object and function level authorisation, authentication, resource limits, mass assignment and inventory."
sources: ["https://owasp.org/API-Security/editions/2023/en/0x11-t10/", "https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html", "https://www.threatmodelingmanifesto.org/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API threat modelling

**Goal:** find the design flaws APIs actually suffer from (mostly authorisation and
business logic) before they ship.

## Model inputs
- API inventory for the service: endpoints, methods, versions, who calls them (SPA, mobile,
  partners, internal services), authentication per caller type. Use the OpenAPI spec.
- Data objects exposed and their ownership rules (which user/tenant may read/write each).
- Gateways, WAF, auth server, backend services and data stores in the DFD.

## Walk the OWASP API Security Top 10 (2023) per endpoint group
1. **BOLA (object level authz):** every `{id}` in a path or body: is ownership checked
   server-side for each request? Can tenant A fetch tenant B's object by changing the ID?
2. **Broken authentication:** token validation (signature, `aud`, `exp`), password reset and
   login endpoints rate-limited, no API keys in URLs.
3. **Broken object property level authz:** mass assignment (`"role":"admin"` accepted in
   update bodies) and excessive data exposure (returning fields the client hides).
4. **Unrestricted resource consumption:** pagination limits, payload size, expensive queries
   per-client rate limits and quotas, costs of downstream
   calls (SMS, email).
5. **Broken function level authz:** admin endpoints reachable by normal users; HTTP method
   switching (`GET` allowed but `DELETE` unprotected).
6. **Unrestricted access to sensitive business flows:** ticket buying, sign-up, voting at bot scale.
7. **SSRF:** endpoints fetching URLs supplied by users (webhooks, imports, previews).
8. **Security misconfiguration:** CORS, verbose errors, missing TLS, default credentials on gateways.
9. **Improper inventory management:** old versions (`/v1`) still live without fixes, shadow
   endpoints, debug endpoints.
10. **Unsafe consumption of third-party APIs:** trusting partner data, following redirects.

## Mitigations to record
Centralised authorisation checks (policy engine or middleware) with deny by default,
response schemas (allowlist fields), request schema validation rejecting unknown properties,
gateway rate limits, API inventory with owners and deprecation dates.

## Gotchas
- Authorisation pushed to the frontend; the API must enforce everything.
- Internal APIs assumed safe because "only our services call them"; one SSRF changes that.

## Verify
Write negative tests from the threat list: cross-tenant ID access returns 404/403, unknown
properties rejected, rate limit returns 429; run them in CI.

## Checked

2026-10-28. Confirmed in the OWASP API Security Top 10 2023 list: API1 BOLA, API3 object property level authorization (mass assignment), API4 unrestricted resource consumption, API7 SSRF, API9 improper inventory, API10 unsafe consumption; OWASP REST Security Cheat Sheet: 429 Too Many Requests for rate limiting, API keys must not be in URLs. Removed: GraphQL depth/complexity and per-resolver claims (not in the fetched pages).
Method: documentation only; no commands were run.
