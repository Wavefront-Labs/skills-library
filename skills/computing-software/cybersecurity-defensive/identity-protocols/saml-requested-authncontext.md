---
id: computing-software.cybersecurity-defensive.identity-protocols.saml-requested-authncontext
name: saml-requested-authncontext
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [saml-requested-authncontext, saml-authn-request-response, requestedauthncontext, authncontextclassref, comparison, loa, mfa, identity-protocols]
level: advanced
status: docs-checked
description: "Ask for a level of assurance with RequestedAuthnContext, choose the comparison attribute, and verify the AuthnContextClassRef the IdP actually returns."
sources:
  - https://docs.oasis-open.org/security/saml/v2.0/saml-core-2.0-os.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RequestedAuthnContext and AuthnContextClassRef

Goal: signal required authentication strength and verify it was met.

Method: add `samlp:RequestedAuthnContext Comparison="exact|minimum|maximum|better"` with one or more `saml:AuthnContextClassRef` (or `AuthnContextDeclRef`) URIs; the class definitions are in the separate SAML authentication context specification, and IdPs may support their own classes (check each IdP's documentation). Default comparison is `exact`. The references are an ordered set, the first being most preferred.

Gotchas:
- Check what the IdP actually did: read `AuthnStatement/AuthnContext` in the assertion and enforce it (practice).
- `exact` needs an exact match of one requested context; `minimum` is at least as strong as one; `better` is stronger than any one; `maximum` is as strong as possible without exceeding one. Strength is as deemed by the responder.
- If none of the requested contexts can be satisfied the IdP must return second-level status `NoAuthnContext`.

Verify: test a user without MFA and confirm the SP rejects the weaker context.

## Checked
Method: 2026-11-09 documentation only; no commands were run. Converted SAML V2.0 Core to text and read the RequestedAuthnContext definition (Comparison values and default, ordered references, NoAuthnContext). Removed the specific class URIs and the Entra claims (not in the cited page; the Entra URL did not resolve).
