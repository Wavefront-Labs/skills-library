---
id: computing-software.web-development.node-express.passkeys-and-webauthn
name: passkeys-and-webauthn
category: computing-software
field: web-development
product: node-express
tags: [authentication-failures, web-authentication, passkeys, webauthn, fido2, simplewebauthn, conditional-ui, phishing-resistant-mfa, discoverable-credentials]
level: practitioner
status: verified
description: "Implementing passkeys with WebAuthn: registration and authentication ceremonies, challenges, rpId/origin checks, conditional UI autofill and account recovery."
sources:
  - https://www.w3.org/TR/webauthn-3/
  - https://simplewebauthn.dev/docs/
  - https://web.dev/articles/passkey-form-autofill
  - https://passkeys.dev/docs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Passkeys and WebAuthn

**Goal:** phishing-resistant sign-in with passkeys, alongside or instead of passwords.

## 1. Registration (logged-in user adds a passkey)
Server (SimpleWebAuthn):
```js
const options = await generateRegistrationOptions({
  rpName: 'Example', rpID: 'example.com', userName: user.email, userID: isoUint8Array.fromUTF8String(user.id),
  attestationType: 'none',
  excludeCredentials: user.passkeys.map(p => ({ id: p.credentialId, transports: p.transports })),
  authenticatorSelection: { residentKey: 'required', userVerification: 'preferred' },
});
req.session.challenge = options.challenge;
```
Browser: `startRegistration({ optionsJSON })` -> POST response. Server `verifyRegistrationResponse({ response, expectedChallenge, expectedOrigin: 'https://example.com', expectedRPID: 'example.com' })`; store `credential.id`, `publicKey`, `counter`, `transports`, plus device type/backup flags.

Ran end to end with @simplewebauthn/server 14.0.3 and @simplewebauthn/browser 14.0.0 in Chrome (Playwright, CDP virtual authenticator, rpID `localhost`, `isoUint8Array` from `@simplewebauthn/server/helpers`): registration verified and returned `credential.id`, `publicKey`, `counter` (1) and `transports`, plus device type and backup flags; discoverable authentication (no `allowCredentials`) verified and the counter moved to 2.

## 2. Authentication with autofill (conditional UI)
```html
<input name="username" autocomplete="username webauthn">
```
```js
const opts = await (await fetch('/webauthn/auth-options')).json();   // no allowCredentials -> discoverable
const asse = await startAuthentication({ optionsJSON: opts, useBrowserAutofill: true });
```
Server: look up credential by `asse.id`, `verifyAuthenticationResponse` with stored public key, expected challenge/origin/rpID; update counter; **regenerate session**.

## 3. Rules that matter
- **Challenges**: random, single-use, short-lived, bound to the session; delete after verification.
- **rpID** = registrable domain (`example.com` works for `app.example.com`; spec: the RP ID must be a registrable domain suffix of or equal to the origin's effective domain); changing domains later orphans passkeys. Related Origin Requests (the client fetches `https://<rpID>/.well-known/webauthn`, per the spec) allow a few extra origins.
- `userVerification: 'preferred'` vs `'required'`: required if passkey alone (no password) must be two-factor.
- Authenticators without a signature counter report a constant zero (WebAuthn spec); don't reject non-incrementing zero counters. SimpleWebAuthn only enforces the counter check when the stored or the received counter is above 0, and the check rejected a replayed assertion in the run ("Response counter value 2 was lower than expected 2"), so for counterless passkeys single-use challenges are the replay defence. A wrong expected origin was rejected ("Unexpected authentication response origin ... expected ...").
- Attestation `none` unless you have enterprise device policy needs.

## 4. Account recovery and UX
Let users register multiple passkeys, show them in settings (name by AAGUID), and keep a recovery path (email + another factor). Offer "Create a passkey" after a password sign-in. Signal API (`PublicKeyCredential.signalUnknownCredential`) helps clean deleted passkeys from managers where supported.

## Verify
- [ ] Register and sign in on iOS Safari, Android Chrome, Windows Hello, and a password manager.
- [ ] Replayed assertion (same challenge) rejected; wrong origin rejected.
- [ ] Autofill offers passkeys in the username field.
