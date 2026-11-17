---
id: computing-software.web-development.node-express.rbac-and-server-side-authorization
name: rbac-and-server-side-authorization
category: computing-software
field: web-development
product: node-express
tags: [broken-access-control, authorization, rbac, deny-by-default, permissions, abac, policy-middleware, function-level-authorization]
level: practitioner
status: docs-checked
description: "Enforcing role/permission checks server-side with deny-by-default middleware, permission (not role) checks, and tests for every route."
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
  - https://owasp.org/Top10/2025/A01_2025-Broken_Access_Control/
  - https://owasp.org/API-Security/editions/2023/en/0xa5-broken-function-level-authorization/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RBAC and server-side authorization

**Goal:** every route has an explicit authorization rule, missing rules fail closed, and hiding a button in the UI is never the control.

## 1. Model permissions, assign via roles
```js
const ROLE_PERMS = {
  viewer: ['invoice:read'],
  member: ['invoice:read', 'invoice:create'],
  admin:  ['invoice:read', 'invoice:create', 'invoice:delete', 'user:manage'],
};
const can = (user, perm) => (ROLE_PERMS[user?.role] ?? []).includes(perm);
```
Code checks **permissions**, not role names (`can(user,'invoice:delete')`, not `user.role === 'admin'`), so adding a role doesn't mean touching every route.

## 2. Deny by default
```js
const authz = (perm) => (req, res, next) => (can(req.user, perm) ? next() : res.sendStatus(req.user ? 403 : 401));
const router = express.Router();
router.get('/invoices', authz('invoice:read'), list);
router.delete('/invoices/:id', authz('invoice:delete'), remove);
app.use('/api', requireLogin, router);
// Fail closed: a startup/test check that every route in router.stack has an authz middleware
```
Put authentication at the router level so new routes can't be public by accident, and make "public" an explicit opt-out.

## 3. Combine with object rules
Permission says *what kind of action*; object-level checks say *on which records* (owner, same tenant, assigned project). Both are needed. Libraries: CASL (JS), Oso/Cerbos (policy engines), Pundit (Rails), django-rules / DRF permission classes.

## 4. Pitfalls
- Admin APIs reachable by non-admins because only the admin UI was hidden.
- Method confusion: `GET` protected but `POST`/`PUT` on the same path not; HEAD/OPTIONS overrides (`X-HTTP-Method-Override`).
- Role read from a client-editable JWT claim without verifying the signature, or from a cookie the client sets.
- Caching authorization in the session for hours after a role is revoked.

## Verify
- [ ] Matrix test: each role x each route, expected 2xx/403.
- [ ] Route inventory check fails CI when a route lacks an authz rule.
- [ ] Revoking a role takes effect on the next request.

## Checked

2026-10-25 against OWASP Cheat Sheet Series (OWASP/CheatSheetSeries, commit of 2026-10-24) and the OWASP Top 10 2025 and API Security 2023 repositories. Confirmed: Deny by Default: the application must always make an access decision even when no rule matches; Validate the Permissions on Every Request, preferably through global application-wide configuration; Enforce Least Privileges horizontally and vertically; RBAC and ABAC trade-offs; OWASP Top 10 2025 A01 and API Security 2023 API5 (broken function level authorization) exist.

Method: documentation only; no commands were run.
