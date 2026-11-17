---
id: computing-software.cybersecurity-defensive.identity-protocols.oidc-issuer-discovery-webfinger
name: oidc-issuer-discovery-webfinger
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oidc-issuer-discovery-webfinger, oidc-discovery, webfinger, issuer-discovery, rel, resource, acct, identity-protocols]
level: advanced
status: docs-checked
description: "Locate the OP for an identifier with WebFinger rel=http://openid.net/specs/connect/1.0/issuer, and the SSRF and privacy limits of doing it."
sources:
  - https://openid.net/specs/openid-connect-discovery-1_0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Issuer discovery via WebFinger

Goal: support dynamic OP discovery from a user-typed identifier.

Method: normalise the input: with no scheme, `userinfo@host` becomes `acct:userinfo@host` and anything else gets `https://`; an explicit scheme is kept; any fragment is stripped. Then GET `https://{host}/.well-known/webfinger?resource=<URL-encoded>&rel=http%3A%2F%2Fopenid.net%2Fspecs%2Fconnect%2F1.0%2Fissuer`. The JRD response (`application/jrd+json`) has `links` entries with `rel` `http://openid.net/specs/connect/1.0/issuer` and `href` giving the issuer. Fetch the provider configuration from that issuer next.

Gotchas:
- Only dynamic issuer discovery needs it; the issuer can also be learned by other means.
- The `issuer` value in the OP's configuration document must be identical to the issuer WebFinger returned.
- A site that uses an e-mail address as a local account name can be addressed with an `acct:` URI such as `acct:joe%40example.com@example.org`.

Verify: call against a test OP and confirm the issuer matches the `issuer` field of its discovery document.

## Checked
2026-11-02. Confirmed against OpenID Connect Discovery 1.0 sections 2, 2.1, 2.2, 3. Removed: SSRF controls, the "enterprise RPs should skip it" advice and the e-mail-domain privacy note, which the spec does not state. Fixed "JWRD" to JRD.
Method: documentation only; no commands were run.
