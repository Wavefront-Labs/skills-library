---
id: computing-software.cybersecurity-defensive.security-architecture.security-patterns
name: security-patterns
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [security-patterns, security-design-patterns, secure-by-design, gatekeeper-pattern, valet-key, defense-in-depth, least-privilege]
level: practitioner
status: draft
description: "Apply proven security design patterns (gatekeeper, valet key, sidecar, broker, compartmentalisation, fail-secure) and recognise anti-patterns in architecture designs."
sources: ["https://learn.microsoft.com/en-us/azure/architecture/patterns/category/security", "https://cheatsheetseries.owasp.org/cheatsheets/Secure_Product_Design_Cheat_Sheet.html", "https://www.cisa.gov/securebydesign", "https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Security design patterns

| Pattern | Problem it solves | Example |
|---|---|---|
| Gatekeeper | Untrusted clients reaching trusted services directly | Validating reverse proxy/API gateway in front of the app tier |
| Valet key | Granting temporary direct access to a resource without proxying data | S3 presigned URL, Azure SAS with short expiry and minimal permissions |
| Federated identity | Apps managing their own passwords | OIDC/SAML to a central IdP |
| Sidecar / ambassador | Each service implementing TLS/auth differently | Service mesh proxy doing mTLS and authz |
| Broker / token exchange | Over-privileged long-lived tokens downstream | STS issuing short-lived, down-scoped tokens |
| Compartmentalisation | Single breach exposing everything | Per-tenant keys/accounts, cell-based architecture |
| Choke point | Too many paths to audit | All egress via one proxy/firewall |
| Fail-secure | Errors granting access | Authz exception -> deny, not allow |
| Secure defaults | Users must opt in to safety | Private buckets, MFA on by default |
| Complete mediation | Cached authz decisions going stale | Check authorisation on every request |
| Separation of duties | One identity can request and approve | Two-person approval on prod deploy/payments |

## Anti-patterns to flag in reviews
- Shared service account across apps or environments.
- Security decisions in the client (hidden fields, client-side role checks).
- "Internal network = trusted" (no auth between services).
- Long-lived static cloud keys in CI or on laptops.
- One admin plane for prod and non-prod.
- Secrets in environment variables committed to repos or baked into images.

## Using them
In design review, map each trust boundary crossing to a pattern; a crossing with no pattern is a
finding.

## Verify
- [ ] Each trust boundary in the design has a named control pattern.
- [ ] No listed anti-pattern present without accepted risk.
