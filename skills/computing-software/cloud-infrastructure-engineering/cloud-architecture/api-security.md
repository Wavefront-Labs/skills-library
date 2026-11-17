---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.api-security
name: api-security
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, infrastructure-protection, api-security, owasp-api-top-10, bola, api-gateway, waf]
level: practitioner
status: docs-checked
description: "Secure cloud APIs against the OWASP API Security Top 10: object-level authorisation, authentication, inventory, rate limits, input validation and testing."
sources: ["https://owasp.org/API-Security/editions/2023/en/0x11-t10/", "https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API security (OWASP API Top 10)

## Steps
The OWASP API Security Top 10 (2023) is: API1 Broken Object Level Authorization, API2 Broken Authentication,
API3 Broken Object Property Level Authorization, API4 Unrestricted Resource Consumption, API5 Broken Function Level
Authorization, API6 Unrestricted Access to Sensitive Business Flows, API7 Server Side Request Forgery,
API8 Security Misconfiguration, API9 Improper Inventory Management, API10 Unsafe Consumption of APIs.

1. **Broken object level authorisation (API1:2023)**: check object-level authorisation in every function that
   accesses a data source using an ID from the user, i.e. in the service itself.
2. **Authentication (API2)**: serve HTTPS only; centralise user authentication in an IdP that issues access tokens.
   For JWTs, require integrity protection (never accept `{"alg":"none"}`), do not let the token header choose the
   verification algorithm, and validate `iss`, `aud` and `exp`. Do not rely only on API keys for sensitive or
   high-value resources. Consider mutually authenticated client certificates for highly privileged services.
3. **Property-level authorisation (API3)**: combines excessive data exposure and mass assignment; authorise at the
   object property level for both responses and accepted input.
4. **Resource consumption (API4)**: set a request size limit and reject larger requests with 413; use rate limiting
   (429 Too Many Requests); also watch per-request paid integrations (SMS, email), which raise cost.
5. **Function-level authorisation (API5)**: keep a clear separation between administrative and regular functions
   and check roles on both. Allow-list HTTP methods and reject others with 405.
6. **Business flows (API6)**: validate workflow state transitions on the server for every request, so endpoints cannot
   be called out of sequence.
7. **Inventory (API9)**: keep an updated inventory of hosts and deployed API versions and document every
   endpoint; this mitigates deprecated versions and exposed debug endpoints.
8. **Input validation**: validate length, range, format and type; use strong types; reject unexpected content;
   require a supported `Content-Type` (415 otherwise); do not expose management endpoints to the Internet.
9. **Test**: authorisation tests per endpoint with two users (A cannot read B's object) and log input-validation
   and auth failures.

## Gotchas
- Return generic error messages; do not leak stack traces or internal details.
- Keep credentials and API keys out of URLs, where they end up in logs.
- Unsafe consumption of third-party APIs (API10): developers tend to trust third-party data more than user input.

## Verify
- [ ] Cross-user object access tests pass for every endpoint.
- [ ] API inventory matches gateway and traffic discovery.

## Checked
2026-11-08. Confirmed against the OWASP API Security Top 10 2023 list (names and numbers) and the OWASP REST Security
Cheat Sheet (HTTPS, JWT validation, API keys, method allow-list, workflow state, input validation, 413/415/405/429,
management endpoints, generic errors, secrets in URLs). The cheat sheet was read for the sections used, not end to
end. Dropped RFC 9700 from sources because nothing in the skill depends on it and it was not read. Removed unsupported
claims: gateways cannot do object-level checks, sequential-ID advice, gateway schema validation from OpenAPI, WAF,
DAST, pagination caps and the mTLS-for-service-to-service rule.
Method: documentation only; no commands were run.
