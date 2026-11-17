---
id: computing-software.web-development.node-express.password-reset-flows
name: password-reset-flows
category: computing-software
field: web-development
product: node-express
tags: [authentication-failures, web-authentication, password-reset, reset-tokens, forgot-password, token-expiry, host-header-injection]
level: practitioner
status: docs-checked
description: "Secure forgot-password flows: random single-use hashed tokens, short expiry, no enumeration, host-header-safe links, session revocation and notifications."
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html
  - https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/07-Input_Validation_Testing/17-Testing_for_Host_Header_Injection
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Password reset flows

**Goal:** a reset link can only be used by the mailbox owner, once, soon - and the flow leaks nothing about which accounts exist.

## 1. Request step
```js
app.post('/password/forgot', limiter, async (req, res) => {
  const user = await findUserByEmail(req.body.email);
  if (user) {
    const token = crypto.randomBytes(32).toString('base64url');
    await db.resetToken.create({ data: { userId: user.id, tokenHash: sha256(token), expiresAt: new Date(Date.now() + 30*60e3) } });
    await sendMail(user.email, `${APP_ORIGIN}/password/reset?token=${token}`);   // APP_ORIGIN from config
  }
  res.render('forgot-sent');   // same response whether or not the user exists
});
```
- Token: long and random from a CSPRNG (the example uses 32 bytes), single use; store only its **hash** so a DB leak does not yield usable links.
- Short expiry (the example uses 30 minutes); invalidate older tokens when a new one is issued.
- Build links from configured `APP_ORIGIN`, **never from the `Host` header** (reset poisoning sends the token to an attacker's domain).
- Rate-limit per email and per IP.

## 2. Reset step
- GET shows the form only if the token hash exists and isn't expired/used; put the token in the form body, and set `Referrer-Policy: no-referrer` on the page (the token is in the URL; third-party resources would get it via Referer).
- POST: verify again, set the new password (same strength rules as sign-up), **mark token used**, delete other tokens, **revoke all existing sessions** and remember-me/refresh tokens, then redirect to login (OWASP advises against logging the user in automatically).
- If MFA is enabled, still require the second factor after reset (otherwise reset bypasses MFA).

## 3. Notify
Email "Your password was changed" with a "this wasn't me" link to support/lock flow.

## 4. Don't
Sending the old or new password by email, and links that log the user in without setting a password.

## Verify
- [ ] Token works once; second use fails; expired token fails.
- [ ] Request with `Host: evil.example` still emails a link to the real origin.
- [ ] After reset, the old session cookie on another browser is rejected.

## Checked

2026-10-25 against OWASP Cheat Sheet Series (OWASP/CheatSheetSeries, commit of 2026-10-24). Confirmed: reset URLs must not rely on the Host header (hard-coded or validated against trusted domains) and must use HTTPS; the reset page sets Referrer-Policy no-referrer and the token endpoint needs rate limiting; tokens must be generated with a secure random algorithm, be sufficiently long, stored securely, single use and expire; OWASP advises not logging the user in automatically after reset and invalidating existing sessions (user choice or automatic).

Method: documentation only; no commands were run.
