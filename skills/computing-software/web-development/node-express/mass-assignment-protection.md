---
id: computing-software.web-development.node-express.mass-assignment-protection
name: mass-assignment-protection
category: computing-software
field: web-development
product: node-express
tags: [broken-access-control, authorization, mass-assignment, over-posting, allowlist-fields, strong-parameters, dto, prisma]
level: practitioner
status: verified
description: "Stopping mass assignment/over-posting: allowlisting writable fields per role with schemas, ORM pitfalls in Express, Rails strong params and Django forms."
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html
  - https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/
  - https://guides.rubyonrails.org/action_controller_overview.html#strong-parameters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mass assignment protection

**Goal:** clients can only set the fields you intend; `{"role":"admin"}` or `{"balance":1e9}` in a request body is ignored or rejected.

## 1. The bug
```js
app.patch('/api/me', requireLogin, async (req, res) => {
  await db.user.update({ where: { id: req.user.id }, data: req.body });   // client controls every column
});
```
Same with `Object.assign(user, req.body)`, Mongoose `new Model(req.body)`, Sequelize `update(req.body)`.

## 2. Allowlist with a schema
```js
import { z } from 'zod';
const UpdateMe = z.object({ name: z.string().min(1).max(100), timezone: z.string().max(64) }).strict();   // .strict() rejects unknown keys
app.patch('/api/me', requireLogin, async (req, res) => {
  const parsed = UpdateMe.safeParse(req.body);
  if (!parsed.success) return res.status(400).json(parsed.error.flatten());
  await db.user.update({ where: { id: req.user.id }, data: parsed.data });
  res.sendStatus(204);
});
```
Different schemas per role (`AdminUpdateUser` may include `role`). Rejecting unknown keys (vs silently stripping) surfaces client bugs and probes. Run with zod 4: `.strict()` gives `{"formErrors":["Unrecognized key: \"role\""]}` from `flatten()`; the cheat sheet recommends DTOs or field allowlists over blocklists.

## 3. Framework equivalents
- **Rails**: `params.require(:user).permit(:name, :timezone)` - never `permit!`. `config.action_controller.action_on_unpermitted_parameters = :raise` makes unpermitted params raise `ActionController::UnpermittedParameters` (default is `:log` in development and test, `false` elsewhere).
- **Django**: `ModelForm` with explicit `fields = [...]` (never `'__all__'` for user-facing forms); DRF serializers with explicit `fields` and `read_only_fields`.
- **Mongoose** (tested on mongoose 9 with no database): `select: false` only hides a field on reads, writes still go through (`findOneAndUpdate({}, { pw })` keeps `pw`). `immutable: true` blocks changes to a saved document (`doc.set`) and strips the key from `updateOne` casts, but `new Model(req.body)` can still set it at creation. Pick fields anyway.

## 4. Response side (excessive data exposure)
The mirror bug: returning whole ORM objects leaks `passwordHash`, `resetToken`, internal flags. Serialize through an explicit output schema/`select`.

## Verify
- [ ] Test: PATCH with `role`, `isAdmin`, `accountId`, `createdAt` - request rejected or fields unchanged.
- [ ] Grep for `data: req.body`, `Object.assign(.*req.body`, `permit!`, `fields = '__all__'` returns nothing.
- [ ] API responses contain no secret columns.
