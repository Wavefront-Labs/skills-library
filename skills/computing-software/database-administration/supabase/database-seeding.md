---
id: computing-software.database-administration.supabase.database-seeding
name: database-seeding
category: computing-software
field: database-administration
product: supabase
tags: [seeding, seed-sql, db-seed, sql-paths, snaplet]
level: intro
status: docs-checked
description: "Seed a Supabase local database with seed.sql and [db.seed] sql_paths globs, ordering rules, and optional Snaplet Seed generation."
sources:
  - https://supabase.com/docs/guides/local-development/seeding-your-database
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: load repeatable sample data after migrations.

Seed files run the first time you `supabase start` and on every `supabase db reset`, after all migrations finish. Keep them to data inserts only; the page's best practice is "only include data insertions in your seed files". With no configuration the CLI reads `supabase/seed.sql`.

Several files in `supabase/config.toml`:

```toml
[db.seed]
enabled = true
sql_paths = ['./countries.sql', './cities.sql']
# or a glob: sql_paths = ['./seeds/*.sql']
```

Ordering and paths:
- Files run in the listed order; glob matches run in lexicographic order.
- Paths are relative to the `supabase` folder, so `./countries.sql` is `supabase/countries.sql`.
- A file matched by several patterns seeds once.
- A pattern matching no files logs a warning.

Snaplet Seed (`@snaplet/seed`) is optional and community-maintained with only occasional fixes. It needs Node.js and npm.

```bash
npm init -y
npx @snaplet/seed init
npx @snaplet/seed sync
npx tsx seed.ts > supabase/seed.sql
```

During `init`, choose `node-postgres` if your ORM is unsupported or absent. Re-run `sync` whenever the schema changes. `init` generates `seed.config.ts` and an example `seed.ts`; the config has an `adapter` and `select` (for only the `public` schema: `['!*', 'public.*']`). LLM-enhanced data needs `OPENAI_API_KEY` or `GROQ_API_KEY` in `.env`, then `sync` and generate again.

## Checked

2026-11-04: Read the Seeding your database guide in full. Confirmed when seeds run, the default `supabase/seed.sql`, `sql_paths` ordering, globs, dedupe and warning, and the Snaplet Seed commands and status. Removed the claim that `dryRun: true` "previews", which the page does not state (it only appears in the example script).
Method: documentation only; no commands were run.
