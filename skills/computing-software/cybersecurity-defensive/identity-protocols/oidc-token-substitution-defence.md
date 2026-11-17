---
id: computing-software.cybersecurity-defensive.identity-protocols.oidc-token-substitution-defence
name: oidc-token-substitution-defence
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oidc-token-substitution-defence, oidc-security-considerations, token-substitution, audience, id-token-misuse, confused-deputy, at_hash, identity-protocols]
level: advanced
status: docs-checked
description: "Prevent ID token and access token substitution: audience checks, at_hash, sub matching with UserInfo, and never using ID tokens as API credentials."
sources:
  - https://openid.net/specs/openid-connect-core-1_0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Token substitution and ID token misuse

Goal: ensure tokens are used only where intended.

Method:
- Validate `aud` of every ID Token: it must contain your `client_id`, and be rejected if it lists additional audiences you do not trust.
- Compare `sub` from UserInfo with `sub` in the ID Token; if they do not match, the UserInfo values must not be used.
- Use `c_hash` to detect authorization-code substitution and `at_hash` to detect access-token substitution.
- Core says the implicit flow is not designed to mitigate token substitution, and that using it for delegated authentication needs additional mechanisms to determine the tokens were issued for the client.
- In the HTTP binding, token responses are bound to requests by TLS-protected message order.

Gotchas:
- A token swapped between sessions (a "cut and paste" attack) is easy when the token is available to the browser.
- Social login SDKs that return ID Tokens to the client: the backend must still validate them as above (`iss`, `aud`, signature, expiry).

Verify: submit an ID token issued to another client and confirm rejection.

## Checked
2026-11-02. Confirmed against OpenID Connect Core 1.0 sections 3.1.3.7, 5.3.2 and 16.11. Removed: "APIs accept only their own audience / never ID tokens", "accept an ID token only for the flow instance that produced it" and the mobile-app backend narrative, which Core does not state.
Method: documentation only; no commands were run.
