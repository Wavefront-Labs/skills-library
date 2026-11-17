---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-browser-based-apps
name: oauth-browser-based-apps
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-browser-based-apps, oauth-native-apps, spa, browser-based-apps, bff, backend-for-frontend, token-storage, cookies, identity-protocols]
level: advanced
status: docs-checked
description: "Secure SPA OAuth: code flow with PKCE, backend-for-frontend holding tokens, in-memory token trade-offs and cookie settings per the browser-based apps BCP."
sources:
  - https://www.rfc-editor.org/rfc/rfc10017
  - https://www.rfc-editor.org/rfc/rfc9700
  - https://www.rfc-editor.org/rfc/rfc9449
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Browser-based apps and the BFF pattern

Goal: pick an SPA architecture knowing the risk.

Architectures (RFC 10017, "OAuth 2.0 for Browser-Based Applications", Section 6, presented in decreasing order of security):
1. BFF (Section 6.1): the backend is the confidential OAuth client, keeps access and refresh tokens in a cookie-based session so no token reaches the browser, and forwards all requests to the resource server with the access token added. Cookies: the BFF MUST set HttpOnly, SHOULD set SameSite=Strict, SHOULD set the path to `/`, SHOULD NOT set the Domain attribute, and SHOULD use a `__Host-Http-` style name prefix.
2. Token-mediating backend (Section 6.2): a backend runs the OAuth flow as a confidential client and hands the access token to the application, which calls resource servers directly. Less secure than a BFF because the access token is exposed to the application.
3. Browser-based OAuth client (Section 6.3): the application runs the Authorization Code flow with PKCE itself.

Gotchas:
- Under XSS a BFF cannot be made to leak tokens, but the attacker can still send requests to the BFF from within the application origin; the RFC says attacks that make requests with the session cookie cannot be stopped at the application level.
- The BFF MUST implement a proper CSRF defence; SameSite=Strict is adequate only if the BFF is not same-site with other applications.
- Implicit grant: authorization servers MUST NOT issue access tokens in the authorization response, and browser-based clients MUST use the Authorization Code grant.
- Storing tokens in universally accessible storage such as Local Storage is easier for malicious JavaScript to read than isolated storage such as a Web Worker; refresh token rotation (RFC 9700 Section 4.14.2) and sender-constrained tokens (DPoP, RFC 9449) reduce but do not eliminate token theft.

Verify: inspect browser storage after login and confirm no tokens are readable by page JavaScript (BFF case).

## Checked

Date: 2026-11-02. Confirmed in RFC 10017 (the browser-based apps BCP, published as an RFC; Sections 6.1 to 6.3, 8, 7.2), RFC 9700 and RFC 9449 as cited above. Removed as not stated there: "access tokens in memory only" prescription, "no localStorage" as a hard rule, the Lax option and custom-header CSRF detail, the old "confirm current draft number" hedge, and the earlier RFC 8252 source (that is the native-apps BCP).

Method: documentation only; no commands were run.
