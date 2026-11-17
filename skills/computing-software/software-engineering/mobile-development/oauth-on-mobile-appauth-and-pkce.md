---
id: computing-software.software-engineering.mobile-development.oauth-on-mobile-appauth-and-pkce
name: oauth-on-mobile-appauth-and-pkce
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, appauth, pkce, oauth2, openid-connect, custom-tabs, rfc8252]
level: advanced
status: docs-checked
description: "Implement OAuth 2.0 sign-in in native apps per RFC 8252: external browser, PKCE, redirect URI types, state, and what AppAuth Android and iOS provide."
sources: ["https://datatracker.ietf.org/doc/html/rfc8252", "https://datatracker.ietf.org/doc/html/rfc7636", "https://github.com/openid/AppAuth-Android", "https://github.com/openid/AppAuth-iOS"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OAuth on mobile (AppAuth / PKCE)

**Goal:** sign users in with an OAuth 2.0 provider from a native app: external browser, no embedded
web view, no reliance on a client secret, codes protected by PKCE.

## Rules from RFC 8252
- Use an external user-agent (typically the system browser), not an embedded user-agent such as a
  web view. Native apps MUST NOT use embedded user-agents for authorization requests: the app can
  access the user's full authentication state and credentials, and the user cannot verify what they
  are typing into. The external browser also shares authentication state, giving single sign-on.
- Native apps are public clients and cannot be assumed to keep a secret. A shared secret in an app
  that many users install is not a confidential secret, since one user can extract it. Servers should
  treat such clients as public.
- PKCE (RFC 7636) is required for native app public clients, and authorization servers MUST support
  it. Servers should reject authorization requests from native apps that omit it.
- The implicit flow cannot be protected by PKCE, so RFC 8252 advises against it (and access tokens
  from it cannot be refreshed).
- Use `state` and reject responses without a matching value.

## Redirect URI options
- **Claimed https URI** (App Links / Universal Links): apps SHOULD use these over other types; the OS
  opens them in the app, and they are less susceptible to hijacking by another app.
- **Private-use URI scheme**: must be based on a domain name you control in reverse notation
  (`com.example.app:/oauth2redirect/example-provider`, a single slash after the scheme). Servers
  should reject schemes without a period. Another app can claim the same scheme, which is exactly the
  attack PKCE mitigates.
- **Loopback IP** (`http://127.0.0.1:{port}/path`): for apps that can open a loopback port, mainly
  desktop. The authorization server must allow any port at request time.

## PKCE (RFC 7636)
- `code_verifier`: high-entropy random string of unreserved characters, 43 to 128 characters long.
- `code_challenge` for `S256` is `BASE64URL-ENCODE(SHA256(ASCII(code_verifier)))`. If the client can
  use `S256` it MUST; `plain` is only permitted if S256 is unsupported.
- Send the challenge and method in the authorization request and the verifier in the token request;
  the server transforms the verifier and compares it.

## AppAuth
- **Android**: follows RFC 8252 using Custom Tabs; WebView is explicitly not supported. Supports PKCE.
  `AuthorizationServiceConfiguration.fetchFromIssuer` discovers endpoints. Set the manifest placeholder
  `appAuthRedirectScheme` (for example `com.example.app`). `AuthState` is serialised with
  `jsonSerializeString()` for persistence, and `performActionWithFreshTokens` refreshes the access
  token as needed before an action.
- **iOS**: supports iOS 15 and above, authenticating through ASWebAuthenticationSession; UIWebView and
  WKWebView are not supported. Custom scheme and https redirects both work, but https redirects
  need iOS 17.4+, an Associated Domains entitlement using the `webcredentials` service for the
  redirect host, and an AASA file listing the app under `webcredentials`; an `applinks` association
  alone is not enough. `OIDAuthState.authState(byPresenting:presenting:)` performs the code exchange,
  protected by PKCE if the server supports it.

## Verify
- [ ] Login opens the system browser or Custom Tab; no web view.
- [ ] The authorization request includes `code_challenge_method=S256` and `state`.
- [ ] The redirect URI is a claimed https URI or a reverse-domain private-use scheme.

## Checked
Read RFC 8252, RFC 7636 and the AppAuth-Android and AppAuth-iOS READMEs as downloaded text. Removed as unconfirmed: Kotlin and Swift code samples, Apple ASWebAuthenticationSession documentation claims (unreadable host), token storage advice (Keychain, Keystore), refresh-token rotation, RFC 7009 revocation, backend-for-frontend, DPoP and attestation, and the claim that Google blocks web view OAuth.
Method: docs-checked 2026-11-09 against RFC 8252, RFC 7636 and the two AppAuth READMEs.
