---
id: computing-software.web-development.strapi.database-transactions
name: database-transactions
category: computing-software
field: web-development
product: strapi
tags: [strapi, database, transactions, rollback, commit, document-service]
level: advanced
status: docs-checked
description: "Wrap Strapi Document Service and db.query calls in strapi.db.transaction with rollback and commit hooks."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/database-transactions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Database transactions

Experimental. Use `strapi.db.transaction` with a callback.

```js
await strapi.db.transaction(async ({ trx, rollback, commit, onCommit, onRollback }) => {
  // your operations
});
```

The callback receives:
- `trx`: the transaction object.
- `rollback`, `commit`: manual control.
- `onCommit`, `onRollback`: register callbacks that run after that outcome.

## Behaviour
- Document Service, `strapi.db.query` and entityService calls made inside the callback use the transaction implicitly; you do not pass `trx`.
- Transactions can nest; the inner one follows the outer.
- If the callback throws, the transaction rolls back; otherwise it commits after the handler runs.
- Plain knex queries do not use the transaction implicitly: call `.transacting(trx)` on them.
- Avoid transactions for independent operations (performance penalties) and make sure every path commits or rolls back, otherwise an open transaction can lock or stall until the server restarts.

## Example shape
Create an article and a log entry so both succeed or neither does:

```js
await strapi.db.transaction(async () => {
  await strapi.documents('api::article.article').create({ data: { title: 'x' } });
  await strapi.documents('api::log.log').create({ data: { message: 'created' } });
});
```

(The content-type uids here are illustrative.) Related: `computing-software.web-development.strapi.document-service-write`.

## Checked

2026-11-04: checked against the Strapi docs page Database transactions (database-transactions). Confirmed: experimental status, handler properties, implicit use by Document Service, `strapi.db.query` and entityService, nesting, rollback on throw, onCommit and onRollback. Added from the page: commit on success, the knex `.transacting(trx)` requirement, and the locking and stalling cautions.

Method: documentation only; no commands were run.
