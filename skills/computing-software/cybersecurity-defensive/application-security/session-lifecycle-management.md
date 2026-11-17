---
id: computing-software.cybersecurity-defensive.application-security.session-lifecycle-management
name: session-lifecycle-management
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [session-management, session-fixation, session-timeout, session-revocation, logout, session-id-regeneration]
level: advanced
status: docs-checked
description: "Manage web session lifecycle: regenerate IDs at login and privilege change, enforce idle and absolute timeouts, real server-side logout and revoke sessions on password reset."
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html", "https://pages.nist.gov/800-63-4/sp800-63b.html", "https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Session lifecycle (fixation, timeout, revocation)

**Goal:** a session identifier is unpredictable, changes when trust changes, expires, and dies everywhere when it should.

## Creation
- IDs from the framework's CSPRNG with at least 64 bits of entropy (OWASP Session Management Cheat Sheet).

## Fixation defence
OWASP: the session ID must be renewed or regenerated after any privilege level change within the session (login, privilege elevation such as MFA step-up, role change).
- Use your framework's own regenerate/renew call and test that the cookie value differs before and after login; do not copy pre-authentication session data across unreviewed.

## Timeouts
- OWASP: values depend on how critical the application is. Common idle timeouts are 2-5 minutes for high-value applications and 15-30 minutes for low-risk ones; an absolute timeout for an office-worker application could be 4-8 hours.
- NIST SP 800-63-4 section 5 lists recommended reauthentication intervals per assurance level (for example AAL2: 24 hours overall, 1 hour inactivity; AAL3: 12 hours overall, 15 minutes inactivity).
- Enforce on the server; invalidate the session on both client and server when it expires.

## Termination
- Logout invalidates the server-side session (for example `HttpSession.invalidate()` in J2EE; OWASP calls server-side invalidation mandatory) and clears the cookie.
- Password change/reset and MFA reset revoke the user's other sessions (OWASP Forgot Password cheat sheet: invalidate existing sessions after a reset).
- Admin and incident tooling can kill all sessions for an account.
- Stateless JWT sessions need a deny-list or short lifetimes plus refresh revocation to achieve the same.

## Gotchas
- Regenerating the ID but copying an attacker-planted pre-auth session's data across without review.
- Load balancers with sticky sessions and in-memory stores lose logout state across nodes; use a shared store.
- Concurrent session limits without notification confuse users; log and alert on new device sessions instead.

## Verify
- [ ] Session cookie value differs before and after login.
- [ ] Old cookie replayed after logout returns unauthenticated.
- [ ] After password reset, a session on another browser is terminated.

## Checked

2026-10-28. Confirmed in the OWASP Session Management Cheat Sheet: 64-bit entropy minimum, renewal after privilege change, idle and absolute timeout ranges, server-side invalidation. Confirmed in NIST SP 800-63-4 63B: the reauthentication table. Removed: per-framework regenerate calls (`changeSessionId`, `cycle_key`, `SignInAsync`), the old AAL2 30-minute and 12-hour figures (they did not match the revision 4 table), the unconfirmed URL-parameter rule and the "sign out other devices" feature claim. Sources replaced with real URLs.
Method: documentation only; no commands were run.
