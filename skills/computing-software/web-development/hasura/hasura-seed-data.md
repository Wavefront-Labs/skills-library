---
id: computing-software.web-development.hasura.hasura-seed-data
name: hasura-seed-data
category: computing-software
field: web-development
product: hasura
tags: [hasura, cli, seeds, sample-data, postgres]
level: intro
status: docs-checked
description: "Create and apply Hasura seed files with hasura seed create and hasura seed apply to load reference or sample data into a database."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/migrations-metadata-seeds/manage-seeds.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: add initial seed data, such as a testing user or the values of a table exposed as GraphQL enums.

Create a seed file from data already in a table:

```bash
hasura seed create myAuthorsSeed --from-table author
```
Select the database when prompted. The CLI logs the new file, for example `seeds/default/1656499378904_myAuthorsSeed.sql`, which holds plain SQL such as `INSERT INTO public.author (id, name) VALUES ('1', 'Woolf');` preceded by `SET check_function_bodies = false;`.

To seed a table with hand-written SQL, leave off `--from-table`: Hasura opens an editor, and on save and quit creates the seed file in `/seeds/default`.

Apply a seed file:

```bash
hasura seed apply --file 1656499378904_myNewAuthorsSeed.sql
```
Without `--database-name` the CLI prompts for the database. On success it logs `INFO Seeds planted`.

## Checked
2026-11-07. Read in full the single cited page (manage-seeds.mdx; GitHub file view, no snippet files).
Confirmed: every command, prompt and log line above.
Removed: `--database-name` on `seed create` (not shown for create), "empty SQL file in `seeds/<DB>/`" (page: an editor opens), "without `--file` all seed files run", the Console export claim, `hasura deploy --with-seeds`, the "not tracked in migrations table / use ON CONFLICT" gotcha, and the invented Verify step. Thin skill: the page is short; the CLI reference pages for seed commands were not cited.
Method: documentation only; no commands were run.
