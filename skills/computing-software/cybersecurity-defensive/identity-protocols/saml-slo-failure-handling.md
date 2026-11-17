---
id: computing-software.cybersecurity-defensive.identity-protocols.saml-slo-failure-handling
name: saml-slo-failure-handling
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [saml-slo-failure-handling, saml-single-logout, slo, partial-logout, session-timeout, fallback, identity-protocols]
level: advanced
status: draft
description: "Decide what to do when SAML SLO fails or is unsupported: local logout, short session lifetimes, and communicating partial logout to users."
sources:
  - https://docs.oasis-open.org/security/saml/v2.0/saml-profiles-2.0-os.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SLO failure modes and local logout policy

Goal: make logout predictable when federation cannot do it.

Method:
- Always destroy the local session first, then attempt SLO.
- Treat `PartialLogout` as logout with a warning page listing apps still open.
- Where an SP lacks SLO endpoints, rely on short session lifetimes and re-authentication for sensitive actions.
- Prefer OIDC back-channel logout where the SP supports both; see the OpenID logout topics.

Gotchas:
- Redirect-chain SLO fails if any SP shows an error page or blocks framing/cookies.
- Third-party cookie blocking breaks iframe-based logout propagation.
- Logging out of the IdP does not end SP sessions that never receive a message.

Verify: block one SP's SLO endpoint in a test and confirm the user still ends up logged out of the others with a clear message.
