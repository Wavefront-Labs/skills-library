---
id: computing-software.qa-testing-engineering.test-automation.authentication-and-session-management-testing
name: authentication-and-session-management-testing
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [session-management-testing, authentication-testing, security-testing, owasp-wstg, cookies, jwt]
level: advanced
status: draft
description: "Test authentication and session handling per OWASP WSTG: lockout, credential reset, cookie flags, session fixation, timeout, logout invalidation and JWT checks."
sources:
  - https://owasp.org/www-project-web-security-testing-guide/
  - https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
  - https://owasp.org/www-project-application-security-verification-standard/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Authentication and session management testing

**Goal:** confirm an attacker cannot guess, steal, fix or reuse a session, and that login, reset and logout behave safely. Maps to WSTG-ATHN and WSTG-SESS. Test only systems you are authorised to test.

## Authentication checks
- **Credential transport:** login form and API only over HTTPS; no credentials in URLs or logs.
- **Lockout / throttling:** 10+ wrong passwords: is there rate limiting or progressive delay? Is lockout per account and per IP, and does it enable denial of service against known usernames?
- **Enumeration:** login, signup and password-reset responses (body, status, timing) are identical for existing and unknown users.
- **Password reset:** token single-use, expires (minutes to an hour), long and random, bound to the account, invalidated after password change; reset link host not taken from the `Host` header.
- **MFA:** cannot skip the second step by browsing directly to a post-login URL; OTP brute force is limited.

## Session checks
- **Cookie flags:** `Secure`, `HttpOnly`, `SameSite=Lax` or `Strict`, narrow `Path`/`Domain`. Check in DevTools > Application > Cookies.
- **Session fixation:** note the session ID before login; it must change after login and after privilege change.
- **Idle and absolute timeout** enforced server-side: replay an old cookie with curl after the timeout.
- **Logout:** server invalidates the session; replaying the captured cookie afterwards returns 401/redirect.
- **Concurrent sessions** policy matches requirements; password change kills other sessions.
- **Session ID entropy:** collect a few hundred IDs (Burp Sequencer) and check randomness.

## JWT specifics
- Reject `alg: none` and algorithm switching (RS256 to HS256 signed with the public key).
- Expiry (`exp`) enforced; tokens revocable or short-lived with refresh rotation.
- No sensitive data in the payload (it is only base64).

```bash
curl -s -o /dev/null -w '%{http_code}\n' -H "Cookie: SESSION=$OLD" https://app.example/api/me   # expect 401 after logout
```

## Verify
Every check has evidence (request/response pair or screenshot), and post-logout and post-timeout replays both fail.
