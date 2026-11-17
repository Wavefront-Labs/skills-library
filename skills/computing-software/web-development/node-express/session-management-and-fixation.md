---
id: computing-software.web-development.node-express.session-management-and-fixation
name: session-management-and-fixation
category: computing-software
field: web-development
product: node-express
tags: [authentication-failures, web-authentication, session-management, session-fixation, session-rotation, idle-timeout, absolute-timeout, express-session, logout]
level: practitioner
status: verified
description: "Server-side session lifecycle: regenerating ids at login and privilege change, idle/absolute timeouts, real logout, session stores and listing/revoking sessions."
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
  - https://github.com/expressjs/session
  - https://github.com/OWASP/ASVS/blob/v4.0.3/4.0/en/0x12-V3-Session-management.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Session management and fixation

**Goal:** sessions start fresh at login, expire sensibly, die on logout, and users can see and revoke them.

## 1. Regenerate on login (fixation)
If the pre-login session id survives login, an attacker who planted that id (via a subdomain cookie, URL, or shared device) is now logged in as the victim.
```js
app.post('/login', async (req, res, next) => {
  const user = await verifyCredentials(req.body);
  if (!user) return res.status(401).render('login', { error: 'Email or password is incorrect' });
  req.session.regenerate((err) => {                 // new id, old session destroyed
    if (err) return next(err);
    req.session.userId = user.id; req.session.createdAt = Date.now();
    req.session.save((err) => (err ? next(err) : res.redirect(303, '/')));
  });
});
```
Ran on express-session 1.19.0: the session id changed after `regenerate`, the old session was gone from the store, and `userId` was set on the new one. Also regenerate on privilege changes (sudo mode, role change, MFA completion). Django `login()` and Rails `reset_session` do this; call `reset_session` yourself in Rails custom auth.

## 2. Timeouts
- **Idle**: 15-30 min for sensitive apps, longer for low-risk; implement with `rolling: true` + `cookie.maxAge`, or track `lastSeen` server-side.
- **Absolute**: e.g. 8-24 h regardless of activity - check `createdAt` on each request.
- Re-authenticate for sensitive actions (change email/password, payouts) even inside a valid session.

## 3. Logout that works
```js
app.post('/logout', (req, res) => req.session.destroy(() => { res.clearCookie('__Host-sid', { path: '/' }); res.redirect(303, '/login'); }));
```
Use POST (with CSRF protection), destroy server-side state (ran: after `destroy` the replayed old cookie got an empty anonymous session, so your route must return 401 itself; the `__Host-` prefix also requires `cookie.secure: true`, `path: '/'` and no `domain` in browsers); with JWT-only sessions there's nothing to destroy - keep a denylist or short expiry + refresh token revocation.

## 4. Store
`express-session` default MemoryStore leaks and doesn't scale - use Redis (`connect-redis`) or DB. Session ids: ≥128 bits from a CSPRNG (the libraries do this). Set a strong `secret` from the environment; rotate by passing an array `[new, old]` (ran: a cookie signed with the old secret still resolved the session, one signed with an unknown secret did not; `rolling: true` re-sent the cookie on each response).

## 5. Session inventory
Store sessions per user (device, IP, last seen) so users can see "active sessions" and revoke; revoke all on password change/reset.

## Verify
- [ ] Session cookie value differs before and after login.
- [ ] After logout, replaying the old cookie returns 401.
- [ ] Session older than the absolute timeout is rejected even if active.
