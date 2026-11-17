---
id: computing-software.web-development.node-express.magic-links-and-email-otp
name: magic-links-and-email-otp
category: computing-software
field: web-development
product: node-express
tags: [magic-link-login, email-otp, passwordless, one-time-code, authentication]
level: practitioner
status: docs-checked
description: "Passwordless login via email links or one-time codes: token generation, single use and expiry, rate limiting, generic responses and the one-time-code input hint."
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/autocomplete#one-time-code
  - https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Magic links and email OTP

The OWASP Forgot Password cheat sheet describes URL tokens and PINs for password reset. The same identifier rules carry over to passwordless login links and codes, which this skill applies by analogy.

## 1. Token handling
```js
const token = crypto.randomBytes(32).toString("base64url");
await db.loginTokens.insert({ userId, tokenHash: sha256(token), expiresAt: Date.now() + 15 * 60_000, usedAt: null });
sendEmail(user.email, `https://app.example.com/auth/magic?token=${token}`);
```
Rules the cheat sheet gives for every reset token or code:
- Generated with a cryptographically secure random number generator.
- Long enough to resist brute force.
- Linked to one user in the database.
- Single use: invalidated once used, and expiring after an appropriate period.
- Stored securely (the sketch above stores a SHA-256 hash, not the raw token).

Build the link from a hard-coded or allow-listed domain, never from the request Host header (host header injection), and use HTTPS. Rate limit attempts so tokens cannot be brute forced from the URL. The cheat sheet suggests a `no-referrer` Referrer Policy on the landing page to avoid referrer leakage.

Make "used" atomic, for example `UPDATE ... WHERE token_hash = $1 AND used_at IS NULL AND expires_at > now() RETURNING user_id`. The 15 minute lifetime above is an example value, not a figure from the sources.

## 2. One-time codes
- The cheat sheet describes PINs of 6 to 12 digits, sent over a side channel such as SMS, entered with the username; the PIN yields a limited session. Spaces in the displayed code make it easier to read and type.
- Input hint: `<input inputmode="numeric" autocomplete="one-time-code">`. MDN defines `one-time-code` as a one-time password used as an additional factor in sign-in, usually received by SMS, email or an authenticator app.

## 3. Flow safety
- Return the same generic message whether or not the account exists (the cheat sheet's example: "If that email address is in our database, we will send you an email"), and make response time consistent so timing does not reveal which accounts exist.
- After a successful recovery, invalidate existing sessions and outstanding recovery links or codes so an attacker's access is not restored by them.
- Do not automatically log the user in after a password reset (this advice is for reset flows; the same caution applies to session handling code you add).

## Verify
- [ ] Reusing a link fails and an expired link fails.
- [ ] The response and timing for an unknown email match those for a known one.

## Checked

Token rules, URL token and PIN guidance, generic-response and timing advice, session invalidation after recovery, and the `one-time-code` autocomplete value were confirmed on the OWASP Forgot Password cheat sheet and the MDN autocomplete page. The OWASP Authentication cheat sheet was searched for passwordless guidance and supplied only the generic-message rule. Removed as unconfirmed by any page read: email-scanner prefetch behaviour, attempt caps and code lengths beyond the PIN range, WebOTP, tab binding, deliverability (SPF, DKIM, DMARC) and the passkey advice.

Method: docs-checked 2026-11-09 against OWASP Forgot Password cheat sheet (raw markdown read from the general practices through PINs sections), OWASP Authentication cheat sheet (searched, not read in full) and MDN autocomplete attribute page (one-time-code entry read).
