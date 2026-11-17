---
id: computing-software.cybersecurity-defensive.application-security.password-reset-security
name: password-reset-security
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [password-reset-security, forgot-password, reset-tokens, account-recovery, host-header-injection]
level: practitioner
status: docs-checked
description: "Build a secure password reset flow: uniform responses, single-use expiring hashed tokens, host header safety, session invalidation, MFA interplay and notifications."
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html", "https://pages.nist.gov/800-63-4/sp800-63b.html", "https://portswigger.net/web-security/host-header/exploiting/password-reset-poisoning"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Password reset flow security

Password reset is an authentication bypass by design; it must be at least as strong as login.

## Request step
- Same response, same timing for existing and non-existing accounts: "If an account exists, we've sent an
  email". Send email asynchronously so timing does not leak existence.
- Rate limit per account and per IP; CAPTCHA after anomalies.
- Do not reveal the email address or phone number on screen beyond a masked hint if needed.

## The token
- Generated with a cryptographically safe algorithm and long enough to resist brute force (OWASP Forgot Password cheat sheet); URL-safe.
- **Store it securely**: store a hash of the token server-side, bound to the user, with a short expiry.
- **Single use**: invalidate on use and when a new token is issued or the password changes by other means.
- Send in a link to a fixed, configured base URL. **Never build the link from the request `Host` header** or other request-supplied host values (password reset poisoning sends the victim's token to the attacker's host).
- The reset page response uses `Referrer-Policy: no-referrer` and loads no third-party resources; after
  validating, move the token out of the URL (POST or session) to avoid leakage in history and logs.

## Reset step
- Require the new password twice; apply the normal password policy (length, breached-password check).
- If the user has MFA, require the second factor as part of reset (otherwise email compromise bypasses MFA),
  or route to a stronger recovery process.
- After reset: invalidate existing sessions (OWASP: ask the user or invalidate automatically), plus remember-me and refresh tokens, and do not log the user in automatically (OWASP: have them log in through the usual mechanism).
- Notify the user by email that the password changed, with a link to report it was not them.

## Avoid
- Security questions (OWASP: ASVS requirement 6.4.2 excludes knowledge-based authentication).
- Sending the new or old password by email.
- Short numeric codes without strict attempt limits and short expiry.
- Tokens derived from user data or timestamps.

## Verify
Reset with an unknown email gives an identical response; a token works once and expires; changing the `Host`
header does not alter the emailed link; old sessions are logged out after reset.

## Checked

2026-10-28. Confirmed in the OWASP Forgot Password Cheat Sheet: uniform response and timing, rate limiting, single-use expiring tokens, `no-referrer` Referrer Policy on the reset page, password typed twice, notification email without the password, no automatic login, session invalidation option; PortSwigger: Host-header password reset poisoning; OWASP Authentication Cheat Sheet: no security questions (ASVS 6.4.2). Removed: the `secrets.token_urlsafe(32)` call, the 128-bit, SHA-256 and 15-60 minute figures, `X-Forwarded-Host`, the NIST attribution for security questions and the 6-digit code detail, which were not found in the fetched pages.
Method: documentation only; no commands were run.
