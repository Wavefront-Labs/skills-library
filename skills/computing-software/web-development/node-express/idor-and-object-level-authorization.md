---
id: computing-software.web-development.node-express.idor-and-object-level-authorization
name: idor-and-object-level-authorization
category: computing-software
field: web-development
product: node-express
tags: [broken-access-control, authorization, idor, object-level-authorization, bola, owasp-a01, tenant-isolation, scoped-queries]
level: practitioner
status: docs-checked
description: "Preventing IDOR/BOLA: scoping every query to the caller, ownership checks in one place, tenant isolation, and tests that try other users' ids."
sources:
  - https://owasp.org/Top10/2025/A01_2025-Broken_Access_Control/
  - https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html
  - https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IDOR and object-level authorization

**Goal:** a logged-in user can never read or change another user's/tenant's object by changing an id in the URL or body.

## 1. The bug
```js
app.get('/api/invoices/:id', requireLogin, async (req, res) => {
  res.json(await db.invoice.findUnique({ where: { id: req.params.id } }));   // any logged-in user, any invoice
});
```
Authentication (who you are) is checked; authorization for **this object** isn't. UUIDs don't fix it - ids leak via URLs, logs, emails and exports.

## 2. Scope the query to the principal
```js
app.get('/api/invoices/:id', requireLogin, async (req, res) => {
  const inv = await db.invoice.findFirst({ where: { id: req.params.id, accountId: req.user.accountId } });
  if (!inv) return res.sendStatus(404);      // 404, not 403: don't confirm existence
  res.json(inv);
});
```
Apply the same scoping to updates/deletes (`updateMany({ where: { id, accountId } })` and check the count), list endpoints, exports, file downloads and nested resources (`/projects/:p/tasks/:t` - verify the task belongs to the project **and** the project to the user).

## 3. Make it hard to forget
- Repository/data-access functions that **require** the principal: `invoices.forUser(user).get(id)`.
- Multi-tenant: Postgres row-level security (`SET app.tenant_id` per request + RLS policies) as a backstop; Prisma client extension / Django manager / Rails `default_scope` alternatives with care.
- Policy objects (CASL, Pundit, django-rules) for "can user X do action Y on object Z" checks beyond ownership.
- Don't trust ids in the body for ownership (`accountId` from `req.user`, never from `req.body`).

## 4. Indirect references
For downloads/shared links, use unguessable random tokens mapped server-side, with expiry.

## 5. Test it
Automated: for each endpoint, create objects as user A, call as user B, expect 404/403. For manual testing replay each request with a second user's session.

## Verify
- [ ] Cross-user test suite covers every route with an id parameter (read, update, delete, list filters).
- [ ] Logs show 404s for cross-tenant probes (and alert on bursts).
- [ ] No endpoint takes the owner/tenant id from the request body.

## Checked

2026-10-25 against OWASP Cheat Sheet Series (OWASP/CheatSheetSeries, commit of 2026-10-24) and the OWASP Top 10 2025 and API Security 2023 repositories. Confirmed: IDOR is a reference plus a missing object-level authorization check; scoping the query by owner (findByIdAndOwnerId style) is the recommended fix; random identifiers and UUIDs are only defence in depth, so UUIDs do not fix IDOR; OWASP Top 10 2025 A01 is Broken Access Control; API Security 2023 API1 is Broken Object Level Authorization.

Method: documentation only; no commands were run.
