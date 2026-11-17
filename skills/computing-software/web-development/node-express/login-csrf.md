---
id: computing-software.web-development.node-express.login-csrf
name: login-csrf
category: computing-software
field: web-development
product: node-express
tags: [login-csrf, csrf, pre-session-token, oauth-state, session-fixation, security]
level: practitioner
status: docs-checked
description: "Defending against login CSRF, where an attacker signs the victim into the attacker's account: pre-session tokens, Origin/Fetch Metadata checks, OAuth state and session rotation."
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html#possible-csrf-vulnerabilities-in-login-forms
  - https://datatracker.ietf.org/doc/html/rfc9700#section-2.1
  - https://docs.djangoproject.com/en/stable/ref/csrf/
  - https://github.com/Psifi-Solutions/csrf-csrf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Login CSRF

## 1. The attack
An attacker's page auto-submits your login form with the **attacker's** credentials. The victim is now logged in as the attacker; anything they enter (card details, search history, uploaded documents, linked OAuth accounts) lands in an account the attacker controls.
Session CSRF defences often miss it because the victim has no session yet, so there is no session-bound token, and `SameSite` on the (not yet existing) session cookie does not apply.

## 2. Defences
1. **Pre-session token**: create an anonymous session (or signed double-submit cookie) when rendering the login form and require its CSRF token on the login POST. Django's CSRF documentation covers login CSRF and Rails enables forgery protection by default in new apps; custom Express/Fastify apps must do it explicitly (`csrf-csrf` implements the signed double submit cookie pattern, or use a synchronizer token in an anonymous session).
2. **Origin / Fetch Metadata check** on the login endpoint:
```js
app.post("/login", (req, res, next) => {
  const site = req.get("Sec-Fetch-Site");
  if (site && site !== "same-origin" && site !== "none") return res.sendStatus(403);
  const origin = req.get("Origin");
  if (origin && origin !== "https://app.example.com") return res.sendStatus(403);
  next();
}, loginHandler);
```
   OWASP: if neither header establishes a trusted source, reject unless another CSRF defence (such as a token) succeeds; missing headers and `Origin: null` are not evidence of same-origin. The snippet lets requests without `Origin` through, so keep the pre-session token as the primary defence.
3. **Rotate the session id** at login (`req.session.regenerate`, Rails `reset_session`) to prevent fixation.
4. Show who is logged in prominently; a victim notices "Logged in as attacker42".

## 3. OAuth / social login
Login CSRF on the callback links the attacker's provider account to the victim. Use an unguessable `state` bound to the browser session (and PKCE); reject callbacks whose `state` does not match.

## 4. Logout and signup
Signup CSRF has the same effect as login CSRF; protect it the same way. Logout CSRF is low impact but make logout POST-only.

## Verify
- [ ] Cross-site auto-submitting form to `/login` is rejected (403) while same-site login works.
- [ ] OAuth callback with a forged `state` fails.

## Checked

2026-10-25 against OWASP Cheat Sheet Series (OWASP/CheatSheetSeries, commit of 2026-10-24), Django, Rails and csrf-csrf docs and RFC 9700. Confirmed: the OWASP CSRF cheat sheet covers login CSRF, the Stanford paper and pre-sessions as the mitigation; Django CSRF documentation covers login CSRF; Rails enables default_protect_from_forgery for new apps and documents reset_session against fixation; csrf-csrf implements the signed double submit cookie pattern for Express; RFC 9700 section 2.1: clients MUST prevent CSRF, with state or PKCE.

Method: documentation only; no commands were run.
