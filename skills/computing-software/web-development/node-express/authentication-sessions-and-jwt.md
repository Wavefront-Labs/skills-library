---
id: computing-software.web-development.node-express.authentication-sessions-and-jwt
name: authentication-sessions-and-jwt
category: computing-software
field: web-development
product: node-express
tags: [express, node, authentication, jwt, sessions, bcrypt, argon2, refresh-token, cookies, passport, security, web-development, jwt-validation, refresh-token-rotation]
level: advanced
status: verified
description: "Express authentication: sessions vs JWT tradeoffs, bcrypt/argon2 password hashing, refresh-token rotation, and cookie flags that actually matter."
sources:
  - https://expressjs.com/en/resources/middleware/session.html
  - https://www.npmjs.com/package/jsonwebtoken
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Express authentication — sessions vs JWT, and the mistakes in both

**Goal:** pick the right auth model for the deployment shape, and avoid the
specific mistakes that make each one insecure.

## 1. Sessions vs JWT — this is a deployment decision, not a taste choice
- **Sessions** (`express-session` + a store like `connect-redis`): server holds
  state, can revoke instantly (delete the session row), cookie just holds an opaque
  id. Needs a shared store across instances (sticky sessions or shared Redis) —
  doesn't work with pure in-memory store behind a load balancer.
- **JWT**: stateless, scales horizontally with no shared store, but you cannot
  revoke a single token before it expires (no server-side record of it existing)
  unless you add a denylist, which reintroduces the state you were avoiding.
Default to sessions for a traditional server-rendered or same-origin SPA app;
reach for JWT mainly when the API is consumed by distinct services/mobile with no
shared session store, and only once you've accepted the revocation tradeoff.

## 2. Password hashing — bcrypt/argon2, never SHA-anything
```js
const hash = await bcrypt.hash(password, 12);   // cost factor 12, tune to a few hundred ms on your hardware; cost 10/12/14 took about 50/190/760 ms on one dev machine (bcrypt 6.0.0)
const ok = await bcrypt.compare(password, hash);
```
Argon2id is the current best choice if available (`argon2` package; default hash header `$argon2id$v=19$m=65536,p=4,t=3` on argon2 0.45.1) — resistant to
GPU cracking in a way bcrypt partially is and SHA-256/MD5 are not at all. Never
roll your own salting; the library handles salt generation and storage inside the
hash string. Cost factor must be re-tuned over time as hardware gets faster.

## 3. JWT specifics that get apps breached
- **Always verify, never just decode.** `jwt.decode()` reads the payload with zero
  signature check — any client can forge a token that "decodes" fine. Use
  `jwt.verify(token, secret)` on every request.
- **Pin the algorithm.** `jwt.verify(token, key, { algorithms: ['HS256'] })` — if you
  don't pin it, a classic attack swaps `alg: RS256` for `alg: none` or resigns with
  the public key as an HMAC secret, and a permissive verify accepts it. `jsonwebtoken` 9.0.3 rejects both even unpinned (ran: "jwt signature is required" and "invalid algorithm"), but older versions and other libraries may not, so pin anyway.
- **Short-lived access tokens + refresh rotation.** Access token expires in
  5-15 minutes; a separate refresh token (httpOnly cookie, longer-lived) gets a new
  access token. Rotate the refresh token on every use and invalidate the old one —
  detects theft (a reused old refresh token means someone else has it).
- Don't put anything sensitive in the payload — it's base64, not encrypted; anyone
  can read it.

## 4. Cookie flags that actually matter
```js
res.cookie('refreshToken', token, {
  httpOnly: true,   // JS cannot read it — mitigates XSS token theft
  secure: true,     // HTTPS only
  sameSite: 'strict', // or 'lax' if cross-site navigation needs to carry it
  path: '/auth/refresh',
});
```
`httpOnly` is the one most apps forget on tokens stored for later JS use — storing
a JWT in `localStorage` for an SPA to read defeats XSS protection entirely; prefer
an httpOnly cookie even for the access token where the architecture allows it.

## 5. Middleware shape
```js
async function requireAuth(req, res, next) {
  const token = req.cookies.accessToken;
  if (!token) return res.status(401).json({ error: 'unauthenticated' });
  try {
    req.user = jwt.verify(token, process.env.JWT_SECRET, { algorithms: ['HS256'] });
    next();
  } catch {
    return res.status(401).json({ error: 'invalid token' });
  }
}
```
Keep authorization (role/permission checks) as a separate middleware after
`requireAuth` — don't conflate "who are you" with "are you allowed."

## Verify
- [ ] Passwords hashed with bcrypt (cost ≥ 10) or argon2id — never a fast general-purpose hash.
- [ ] `jwt.verify` with pinned `algorithms`, never bare `jwt.decode`, gates protected routes.
- [ ] Refresh tokens rotate on use and are stored httpOnly + secure + sameSite.
- [ ] Access tokens expire short (minutes); no sensitive data sits in the JWT payload.
- [ ] Session store (if used) is shared across all app instances, not in-memory default.
