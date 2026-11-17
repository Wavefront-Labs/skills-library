---
id: computing-software.web-development.fastify.database-plugins-and-migrations
name: database-plugins-and-migrations
category: computing-software
field: web-development
product: fastify
tags: [fastify, database, plugins, postgres, migrations]
level: practitioner
status: docs-checked
description: "Use official DB plugins, write your own wrapped in fastify-plugin with an onClose hook, and run migrations with Postgrator."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Database.md
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Plugins-Guide.md
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Write-Plugin.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Official plugins register a decorated client on the instance:

```js
fastify.register(require('@fastify/postgres'), { connectionString: 'postgres://postgres@localhost/postgres' })
fastify.get('/user/:id', function (req, reply) {
  fastify.pg.query('SELECT id, username FROM users WHERE id=$1', [req.params.id], (err, result) => {
    reply.send(err || result)
  })
})
```

Others: `@fastify/mysql` (`fastify.mysql`, `connectionString`), `@fastify/redis` (`fastify.redis`; pass `closeClient: true` with `client` to close it on shutdown), `@fastify/mongodb` (`fastify.mongo`; `forceClose: true` closes the connection on stop).

Writing your own (Knex example): decorate once and clean up on close.

```js
function knexPlugin (fastify, options, done) {
  if (!fastify.knex) {
    const knex = require('knex')(options)
    fastify.decorate('knex', knex)
    fastify.addHook('onClose', (fastify, done) => {
      if (fastify.knex === knex) fastify.knex.destroy(done)
    })
  }
  done()
}
module.exports = fp(knexPlugin, { name: 'fastify-knex-example' })
```

Migrations: Postgrator with files named `[version].[action].[optional-description].sql` (`001.do.create-users-table.sql`; action is `do` or `undo`), config `migrationPattern`, `driver: 'pg'`, `schemaTable: 'migrations'`, `currentSchema: 'public'`, `execQuery`. For MongoDB use `migrate-mongo`.

Plugin quality (Write-Plugin guide): a plugin without tests, or without good documentation, is not accepted to the ecosystem list; an example file is recommended.

Gotcha: `@fastify/redis` does not close its client on shutdown by default.

## Checked

2026-11-04. Every remaining claim, parameter name, default and example was read against the Fastify documentation sources (Database.md, Plugins-Guide.md, Write-Plugin.md) and confirmed. Removed or corrected: the migration file pattern now uses [optional-description] as the page does; the ecosystem-list requirement is now stated as the Write-Plugin guide words it (tests and documentation required, example recommended); the invented Verify step.

Method: documentation only; no commands were run.
