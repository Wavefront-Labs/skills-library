---
id: computing-software.web-development.node-express.passport-js-authentication
name: passport-js-authentication
category: computing-software
field: web-development
product: node-express
tags: [passport-js, express-authentication, passport-strategies, oauth, sessions]
level: practitioner
status: verified
description: "Authenticating Express apps with Passport.js: local and OAuth strategies, sessions with serializeUser, express-session store security, JWT strategy for APIs, and common pitfalls."
sources:
  - https://www.passportjs.org/concepts/authentication/
  - https://www.passportjs.org/packages/passport-local/
  - https://github.com/expressjs/session
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Passport.js authentication

Passport is authentication middleware with a large catalogue of strategies (see passportjs.org). It verifies credentials and attaches `req.user`; sessions, password hashing, CSRF and authorisation are your job.

## 1. Sessions and local strategy
```js
import session from "express-session";
import { RedisStore } from "connect-redis";
import passport from "passport";
import { Strategy as LocalStrategy } from "passport-local";

app.set("trust proxy", 1);
app.use(session({
  store: new RedisStore({ client: redis }), secret: process.env.SESSION_SECRET, name: "sid",
  resave: false, saveUninitialized: false,
  cookie: { httpOnly: true, secure: true, sameSite: "lax", maxAge: 1000 * 60 * 60 * 24 * 7 },
}));
app.use(passport.session());                 // passport 0.6+: no passport.initialize() needed

passport.use(new LocalStrategy({ usernameField: "email" }, async (email, password, done) => {
  try {
    const user = await users.findByEmail(email.toLowerCase());
    const ok = user && await argon2.verify(user.passwordHash, password);
    return ok ? done(null, user) : done(null, false, { message: "Incorrect email or password." });
  } catch (e) { return done(e); }
}));
passport.serializeUser((user, done) => done(null, user.id));               // store only the id
passport.deserializeUser(async (id, done) => { try { done(null, await users.findById(id)); } catch (e) { done(e); } });

app.post("/login", passport.authenticate("local", { failureRedirect: "/login", failureMessage: true }),
  (req, res) => res.redirect("/dashboard"));
app.post("/logout", (req, res, next) => req.logout(err => err ? next(err) : res.redirect("/")));
```
- Passport 0.6+ regenerates the session on login (`req.login`) to prevent fixation; `req.logout` is async and requires a callback (CHANGELOG 0.6.0). Ran on passport 0.7.0 with express-session 1.19.0 and `passport-local` 1.0.0, without `passport.initialize()`: the session id changed at login, `req.isAuthenticated()` gated `/me`, the old cookie got 401 after logout, a wrong password redirected to `/login`. `passport-jwt` with pinned `RS256`, issuer and audience returned 401 for a wrong issuer, wrong audience and an HS256 token signed with the public key. `connect-redis` exports `RedisStore` (constructed without a server; store behaviour itself not run). `openid-client` v6 exposes `openid-client/passport`; `passport-google-oauth20` and `passport-github2` exist on npm.
- The default `MemoryStore` leaks memory and doesn't work across instances - use Redis/Postgres stores.
- Same error for unknown email and wrong password; rate-limit the login route.
- Add CSRF protection for cookie-session forms.

## 2. OAuth / OIDC
`passport-google-oauth20`, `passport-github2`, or `openid-client`'s Passport strategy for any OIDC provider (supports PKCE, state, nonce). Link external identities to local accounts by provider + subject id, not by email alone (unverified emails enable account takeover).

## 3. APIs with JWT
```js
import { Strategy as JwtStrategy, ExtractJwt } from "passport-jwt";
passport.use(new JwtStrategy({ jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(), secretOrKey: publicKey,
  algorithms: ["RS256"], issuer: "https://auth.example.com", audience: "api" }, (payload, done) => done(null, { id: payload.sub })));
app.use("/api", passport.authenticate("jwt", { session: false }));
```
Pin `algorithms`, check `iss`/`aud`, keep access tokens short-lived.

## 4. Protecting routes
```js
const requireAuth = (req, res, next) => req.isAuthenticated() ? next() : res.status(401).json({ error: "unauthenticated" });
```
Authorisation (roles, ownership) is separate - check after authentication.

## Verify
- [ ] Session regenerated on login and destroyed on logout; session store shared across instances; cookies Secure/HttpOnly/SameSite; JWT strategy rejects wrong algorithm, issuer and audience.
