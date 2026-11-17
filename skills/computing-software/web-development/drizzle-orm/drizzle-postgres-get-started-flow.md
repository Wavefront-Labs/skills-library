---
id: computing-software.web-development.drizzle-orm.drizzle-postgres-get-started-flow
name: drizzle-postgres-get-started-flow
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, getting-started, node-postgres, existing-database, introspection]
level: intro
status: docs-checked
description: "Follow Drizzle's PostgreSQL get-started flows for a new database or an existing one, with node-postgres, dotenv and tsx."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/get-started/postgresql-new.mdx
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/get-started/postgresql-existing.mdx
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/connect-overview.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: a working first query against PostgreSQL, in either of the two documented flows.

Native PostgreSQL support is through the node-postgres and postgres.js drivers; the docs use node-postgres. Prerequisites listed: dotenv (environment variables), tsx (run TypeScript), node-postgres with its `@types/pg` dev types. The connect-overview page lists more PostgreSQL providers: PlanetScale Postgres, Neon, Vercel Postgres, Prisma Postgres, Supabase, Xata, PGLite, Nile, Bun SQL, Effect Postgres, Netlify Database, Appwrite Postgres, AWS Data API Postgres and the Drizzle HTTP proxy.

New database, 8 steps: 1 install node-postgres; 2 set up connection variables (a PostgreSQL-in-Docker guide exists if you have no database yet); 3 connect Drizzle ORM to the database; 4 create a table; 5 set up the Drizzle config file; 6 apply changes to the database; 7 seed and query the database; 8 run the `index.ts` file.

Existing database, 11 steps: 1 install node-postgres; 2 set up connection variables; 3 set up the Drizzle config file; 4 introspect your database; 5 transfer the code to your actual schema file; 6 connect Drizzle ORM to the database; 7 query the database; 8 run the `index.ts` file; then optional 9 update your table schema, 10 apply changes to the database, 11 query the database with the new field.

See `drizzle-kit-pull-introspect` and `drizzle-kit-push-schema` for the introspect and apply commands.

## Checked

2026-11-04: every command, option, default and code identifier above was compared with the cited documentation pages (postgresql-new.mdx, postgresql-existing.mdx, connect-overview.mdx) read in full.

Removed because the pages do not confirm them: unsourced advice, "Verify" steps and behavioural claims.

Method: documentation only; no commands were run.
