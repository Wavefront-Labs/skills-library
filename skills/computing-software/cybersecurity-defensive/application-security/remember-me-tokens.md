---
id: computing-software.cybersecurity-defensive.application-security.remember-me-tokens
name: remember-me-tokens
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [remember-me-tokens, persistent-login, split-token, session-management, cookie-security]
level: practitioner
status: docs-checked
description: "Implement remember-me persistent login safely: split selector/validator tokens, hashed storage, rotation on use, theft detection, scoped privileges and revocation."
sources: ["https://paragonie.com/blog/2015/04/secure-authentication-php-with-long-term-persistence", "https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html", "https://docs.spring.io/spring-security/reference/servlet/authentication/rememberme.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Remember-me tokens

A remember-me cookie is a long-lived credential that recreates a session without a password. Treat it like a
password-equivalent.

## Design: split token (selector + validator)
- On opt-in login, generate a public `selector` (lookup identifier) and a secret `validator`. OWASP describes this identifier/secret-verifier split: the cookie carries both, the server stores the lookup identifier and the full SHA-256 hash of the verifier.
- Generate the validator with a CSPRNG using at least 128 bits of entropy (OWASP prefers 160 bits or more).
- Store in DB: `selector`, hash of `validator`, user ID, expiry, device/user-agent label, created time.
- Cookie value: `selector:validator`, with `Secure` and `HttpOnly` set and a `SameSite` attribute; the `__Host-` prefix (Secure, no Domain, Path=/) is recommended by OWASP.
- On a request without a session: look up by selector, compare the hash of the presented validator with the stored hash using
  a constant-time compare, check expiry, then create a new session.
The split means a DB leak does not reveal usable tokens.

## Rotation and theft detection
- Rotate the validator on each use (issue a new cookie, update the hash). If an old validator for a known
  selector is presented, treat it as possible theft: revoke all of the user's remember-me tokens and alert.
- Spring Security offers `PersistentTokenBasedRememberMeServices` (persistent token approach) and `TokenBasedRememberMeServices` (simple hash-based token approach); prefer the persistent one, which keeps server-side state you can revoke.

## Limit what it grants
- Sessions restored from remember-me should be marked as such; require re-authentication (password or MFA) for
  sensitive actions: changing email/password, payment details, admin functions.
- Do not let remember-me satisfy MFA for high-risk apps, or bind it to a device that completed MFA.

## Revocation
- Logout deletes the token row and cookie.
- Password change, password reset, MFA reset and "log out all devices" delete all rows for the user.
- Show users a list of remembered devices with revoke buttons.
- Cleanup job removes expired rows.

## Avoid
Storing user ID or username in the cookie as the credential, unhashed tokens in DB, never-expiring tokens,
reusing the session ID as the remember-me token.

## Verify
DB contains only hashes; replaying a rotated-out cookie revokes all tokens for that user; password reset kills
remembered logins; sensitive actions prompt for re-authentication.

## Checked

2026-10-28. Confirmed: OWASP Session Management Cheat Sheet (identifier/secret-verifier split, SHA-256 hash of the verifier, 128-bit minimum, `__Host-` prefix); Spring Security remember-me page (both service classes exist and correspond to the persistent and simple hash-based approaches); Paragon Initiative article (selector plus hashed validator design). Removed: byte lengths, 30-day expiry and `Max-Age` figure, the `SameSite=Lax` and `Path` values, the claim about what the older Spring class embeds, and the series/token wording, none of which appear in those pages.
Method: documentation only; no commands were run.
