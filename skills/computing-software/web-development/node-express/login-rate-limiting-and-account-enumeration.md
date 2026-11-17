---
id: computing-software.web-development.node-express.login-rate-limiting-and-account-enumeration
name: login-rate-limiting-and-account-enumeration
category: computing-software
field: web-development
product: node-express
tags: [authentication-failures, web-authentication, brute-force-protection, account-enumeration, credential-stuffing, login-throttling, captcha]
level: practitioner
status: verified
description: "Stopping brute force and credential stuffing with per-account and per-IP throttles, generic responses and equal timing to prevent account enumeration."
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html#protect-against-automated-attacks
  - https://owasp.org/www-community/attacks/Credential_stuffing
  - https://github.com/animir/node-rate-limiter-flexible
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Login rate limiting and account enumeration

**Goal:** password guessing and credential stuffing become impractical, and attackers can't learn which emails have accounts.

## 1. Two-dimensional throttling
```js
import { RateLimiterRedis } from 'rate-limiter-flexible';
const byIP = new RateLimiterRedis({ storeClient: redis, keyPrefix: 'login_ip', points: 100, duration: 3600 });
const byUserIP = new RateLimiterRedis({ storeClient: redis, keyPrefix: 'login_u_ip', points: 10, duration: 900, blockDuration: 900 });
app.post('/login', async (req, res) => {
  const key = `${req.body.email?.toLowerCase()}_${req.ip}`;
  try { await Promise.all([byIP.consume(req.ip), byUserIP.consume(key)]); }
  catch (r) { res.set('Retry-After', Math.ceil(r.msBeforeNext / 1000)); return res.status(429).send('Too many attempts. Try again later.'); }
  // … verify; on success: await byUserIP.delete(key)
});
```
- (Memory limiter used in the test below; `RateLimiterRedis` has the same `consume`/`delete` API.) Per account+IP stops focused guessing without letting attackers lock out a victim from everywhere (avoid hard account lockouts; use growing delays or CAPTCHA instead).
- Per IP (and per /24 or ASN) slows distributed stuffing; per-account global counters with a CAPTCHA step catch botnets using many IPs.
- Set `trust proxy` correctly or `req.ip` is your load balancer (everyone shares one bucket) or attacker-spoofed `X-Forwarded-For`.

## 2. Credential stuffing specifics
Breached-password checks at login (force reset), bot detection/CAPTCHA (Turnstile, reCAPTCHA) after anomalies, MFA, and monitoring login failure ratios.

## 3. No enumeration
- Same message for unknown email and wrong password: "Email or password is incorrect".
- Same timing: run the password hash verification against a dummy hash when the user doesn't exist (measured with scrypt: known user 30.5 ms, unknown user without the dummy hash 0.0 ms, unknown user with it 30.4 ms).
- Sign-up and password reset: "If an account exists, we've sent an email" - send a "someone tried to sign up with your email" message to existing accounts instead of erroring.
- Same HTTP status and response size; watch for differences in redirects/cookies.

## Verify
- [ ] 11th wrong attempt within 15 min for one account from one IP returns 429 with Retry-After.
- [ ] Response time for unknown vs known emails differs by < a few ms (measure 100 samples).
- [ ] Reset and sign-up pages give identical responses for existing/non-existing emails.

## Checked
Run on Windows with Node 20.20.2 and rate-limiter-flexible 11.2.3 using `RateLimiterMemory` (same API as the Redis variant): attempts 1-10 allowed, the 11th and 12th rejected with `msBeforeNext` giving `Retry-After` 900 s; `delete(key)` after a successful login lets the account+IP key through again; a different account from the same IP and the same account from another IP were not blocked; dummy-hash timing as quoted. Not run: `RateLimiterRedis` and a Redis server, `trust proxy` effects on `req.ip` (covered in the rate-limit-headers skill), CAPTCHA and MFA advice, sign-up and reset response equality, the 429 response from a real login route.
