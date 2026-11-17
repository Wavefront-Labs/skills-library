---
id: computing-software.web-development.prisma.migrate-shadow-database-permissions
name: migrate-shadow-database-permissions
category: computing-software
field: web-development
product: prisma
tags: [prisma-migrate-shadow-database-permissions, prisma, createdb-privilege, mysql-grant-shadow, partial-revokes]
level: advanced
status: docs-checked
description: "Database user privileges the shadow database needs per provider, including the MySQL GRANT on prisma_migrate_shadow_db% and the partial_revokes caveat."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-migrate/understanding-prisma-migrate/shadow-database.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Shadow database privileges by provider

To create and drop the shadow database, the user in your datasource needs permission to create databases:

- SQLite: no special requirements.
- MySQL or MariaDB: `CREATE`, `ALTER`, `DROP`, `INDEX` and `REFERENCES` on shadow databases.
- PostgreSQL: superuser, or the `CREATEDB` privilege.
- SQL Server: site admin, or the `SERVER` securable.

Automatically created MySQL shadow databases are named `prisma_migrate_shadow_db_<id>`. Grant on that pattern rather than on `*.*`:

```
GRANT CREATE, ALTER, DROP, INDEX, REFERENCES ON `prisma_migrate_shadow_db%`.* TO 'user'@'%';
```

`INDEX` is needed because generated migrations use standalone `CREATE INDEX` and `DROP INDEX`, which `CREATE` and `ALTER` alone do not allow. With a dedicated database from `shadowDatabaseUrl`, grant the same privileges on that database by name.

Caveat: wildcard database names in `GRANT` are deprecated in MySQL 8.0.35, and when `partial_revokes` is enabled MySQL treats `%` literally so the pattern grant stops matching. On such servers use a dedicated `shadowDatabaseUrl` database and grant by name. MariaDB supports the wildcard without these caveats.

The error `A migration failed when applied to the shadow database ... permission denied to create database` signals missing privilege. Options: update privileges locally, configure a manual shadow database (see `prisma-migrate-shadow-database`), or, when only prototyping on a host that forbids it, run `prisma db push` instead of `migrate dev`. Production needs no shadow database changes.

## Checked
2026-11-03. Confirmed by reading the Prisma ORM v7 docs pages for the topic of this skill (Prisma Migrate getting started, mental model, development and production, baselining, customizing migrations, prototyping, troubleshooting, patching and hotfixing, generating down migrations, squashing, seeding, native types, unsupported features, native functions and extensions, limitations and known issues, and the Prisma Config reference). Commands, flags, error text, privilege lists, defaults and version notes were matched to those pages. Removed: unsupported detail about the exact SQL Server and MySQL lock mechanisms (migrate-deploy-production) and an inferred sentence about v6 experimental keys (config-removed-options).
Method: documentation only; no commands were run.
