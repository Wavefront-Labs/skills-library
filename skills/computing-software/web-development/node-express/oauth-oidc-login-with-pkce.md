---
id: computing-software.web-development.node-express.oauth-oidc-login-with-pkce
name: oauth-oidc-login-with-pkce
category: computing-software
field: web-development
product: node-express
tags: [authentication-failures, web-authentication, oauth-pkce, openid-connect, oidc, authorization-code-flow, state-parameter, nonce, social-login]
level: practitioner
status: docs-checked
description: "Adding OIDC/OAuth 2 login with authorization code + PKCE: state and nonce, ID token validation, account linking pitfalls and where to keep tokens."
sources:
  - https://datatracker.ietf.org/doc/html/rfc9700
  - https://openid.net/specs/openid-connect-core-1_0.html
  - https://datatracker.ietf.org/doc/html/rfc7636
  - https://github.com/panva/openid-client
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OAuth/OIDC login with PKCE

**Goal:** "Sign in with Google/Microsoft/your IdP" that resists CSRF, code injection and account takeover via linking.

## 1. Flow: authorization code + PKCE (RFC 9700: mandatory for public clients, recommended for confidential clients)
```js
import * as client from 'openid-client';
const config = await client.discovery(new URL('https://accounts.google.com'), CLIENT_ID, CLIENT_SECRET);
app.get('/auth/login', async (req, res) => {
  const code_verifier = client.randomPKCECodeVerifier();
  const state = client.randomState(), nonce = client.randomNonce();
  Object.assign(req.session, { code_verifier, state, nonce });
  res.redirect(client.buildAuthorizationUrl(config, {
    redirect_uri: 'https://app.example.com/auth/callback', scope: 'openid email profile',
    code_challenge: await client.calculatePKCECodeChallenge(code_verifier), code_challenge_method: 'S256', state, nonce,
  }).href);
});
app.get('/auth/callback', async (req, res) => {
  const tokens = await client.authorizationCodeGrant(config, new URL(req.originalUrl, 'https://app.example.com'),
    { pkceCodeVerifier: req.session.code_verifier, expectedState: req.session.state, expectedNonce: req.session.nonce });
  const claims = tokens.claims();      // ID token claims (iss, sub, aud, nonce, ...)
  // find-or-create user by (issuer, sub) -> regenerate session
});
```
RFC 9700: clients SHOULD NOT use the implicit grant, and the resource owner password credentials grant MUST NOT be used. Use a maintained library; don't hand-verify JWTs.

## 2. Identity key
Key users by **`iss` + `sub`**, not email. OIDC Core 5.7: `iss` plus `sub` is the only guaranteed unique identifier; email must not be used as one.

## 3. Account linking pitfalls
Auto-linking an OIDC login to an existing local account by matching email = account takeover if the IdP email isn't verified (check `email_verified: true`) or the IdP can assert emails it has not verified. Safer: require the user to log in to the existing account first, then link.

## 4. Tokens
For login you only need the ID token's claims; create your own session cookie. Keep IdP access/refresh tokens server-side (encrypted) only if you call the provider's APIs. SPAs: use a backend-for-frontend instead of storing tokens in localStorage.

## 5. Config hygiene
Exact `redirect_uri` registration, separate clients per environment, rotate client secrets, handle `error=access_denied` callbacks gracefully.

## Verify
- [ ] Callback with wrong/missing `state` fails; replaying a code fails.
- [ ] ID token with wrong `aud` or expired is rejected (library tests).
- [ ] Logging in with an unverified-email IdP account doesn't attach to an existing local user.

## Checked

2026-10-25 against RFC 9700, OpenID Connect Core 1.0 and the openid-client v6 docs (panva/openid-client, 2026-10-12). Confirmed: RFC 9700: PKCE is MUST for public clients and RECOMMENDED for confidential clients; clients MUST prevent CSRF; implicit grant SHOULD NOT and password grant MUST NOT be used; openid-client functions discovery, randomPKCECodeVerifier, calculatePKCECodeChallenge, randomState, randomNonce, buildAuthorizationUrl, authorizationCodeGrant with pkceCodeVerifier, expectedState and expectedNonce, and tokens.claims(); OIDC Core section 5.7: iss plus sub is the only guaranteed unique identifier and email must not be used as one; OIDC Core section 5.1: email_verified true means the OP took steps to ensure the address was controlled by the user.

Method: documentation only; no commands were run.
