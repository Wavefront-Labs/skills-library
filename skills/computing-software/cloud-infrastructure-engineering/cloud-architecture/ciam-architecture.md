---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.ciam-architecture
name: ciam-architecture
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, identity-architecture, ciam, customer-identity, oidc, passkeys, b2c]
level: practitioner
status: draft
description: "Architect customer identity (CIAM): IdP choice, OIDC flows per client type, social and passkey login, MFA, consent, account recovery, fraud controls and scale."
sources: ["https://pages.nist.gov/800-63-4/", "https://datatracker.ietf.org/doc/html/rfc9700", "https://learn.microsoft.com/entra/external-id/", "https://docs.aws.amazon.com/cognito/latest/developerguide/what-is-amazon-cognito.html", "https://fidoalliance.org/passkeys/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Customer identity (CIAM) architecture

## Steps
1. **Pick the platform**: managed CIAM (Entra External ID, Cognito, Identity Platform, Auth0,
   Okta CIC) vs self-hosted (Keycloak). Criteria: MAU pricing, branding control, regions/data
   residency, federation needs, extensibility hooks, SLA.
2. **Flows per client** (OAuth 2.0 Security BCP, RFC 9700): authorization code + PKCE for SPAs
   and mobile apps; no implicit flow; backend-for-frontend holding tokens for browser apps where
   feasible; client credentials only for machine clients.
3. **Authenticators**: passkeys (WebAuthn) as the strongest phishable-resistant option, social
   login, email/password with breached-password checks; MFA step-up for risky actions.
4. **Account lifecycle**: registration with email/phone verification, progressive profiling,
   account linking (social + local), recovery that is not weaker than login, deletion (GDPR).
5. **Consent and privacy**: record consent per purpose and version; minimal claims in tokens.
6. **Fraud and abuse**: bot protection on sign-up/login, credential-stuffing rate limits,
   impossible-travel and device risk signals.
7. **Tokens and sessions**: short-lived access tokens, rotating refresh tokens, revocation;
   validate issuer/audience in APIs.
8. **Scale and availability**: login is on the critical path; check provider rate limits and
   plan for peak events.

## Gotchas
- Account recovery via SMS-only undoes passkey strength.
- Storing tokens in localStorage exposes them to XSS.

## Verify
- [ ] Every client uses code + PKCE; implicit disabled.
- [ ] Recovery, deletion and consent flows tested.
