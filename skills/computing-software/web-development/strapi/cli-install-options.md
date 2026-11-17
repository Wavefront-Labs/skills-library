---
id: computing-software.web-development.strapi.cli-install-options
name: cli-install-options
category: computing-software
field: web-development
product: strapi
tags: [strapi, create-strapi, non-interactive, dbclient, flags, template]
level: practitioner
status: docs-checked
description: "Flags for create-strapi: --non-interactive, --ts/--js, --dbclient and friends, --template, and the incompatible combinations."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/installation/cli.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# create-strapi installation options

| Option | Effect |
|---|---|
| `--ts` / `--js` | TypeScript (default) or JavaScript |
| `--use-npm`, `--use-pnpm`, `--use-yarn` | Force the package manager |
| `--install` / `--no-install` | Install dependencies or not |
| `--git-init` / `--no-git-init` | Initialize git or not |
| `--example` / `--no-example` | Add example data or not |
| `--skip-cloud` | Skip the Strapi login step |
| `--non-interactive` | Skip all prompts and use defaults (TypeScript, install, git, SQLite, no example). Requires the `<directory>` argument |
| `--skip-db` | Skip database prompts, use SQLite |
| `--template <template-name-or-url>` | Create from a template |
| `--dbclient` | `sqlite` (default), `postgres` or `mysql` |
| `--dbhost --dbport --dbname --dbusername --dbpassword` | Database connection |
| `--dbssl=true` | Use SSL (off by default) |
| `--dbfile` | SQLite file path |

`--quickstart` is deprecated in Strapi 5; use `--non-interactive`. Unlike `--non-interactive` it still asks for Strapi Cloud login unless `--skip-cloud` is also passed. `--no-run` (only meaningful with `--quickstart`) stops the app starting after creation. `--enable-ab-tests` and `--no-enable-ab-tests` are accepted but have no effect.

Without a `--use-*` flag, dependencies are installed with the package manager that ran the create command. `npx create-strapi-app@latest` still works and is equivalent to `npx create-strapi@latest`; `npm create strapi@latest` also works.

## Rules
- For a non-SQLite database pass all of `--dbclient`, `--dbhost`, `--dbport`, `--dbname`, `--dbusername`, `--dbpassword`; otherwise the command stops and lists the missing ones.
- Errors: `--ts` with `--js`; `--ts`/`--js` with `--template`; `--example` with `--template`; more than one `--use-*`; `--quickstart` or `--non-interactive` without a `<directory>` argument.
- `npx create-strapi@experimental` creates from the latest experimental release (released Tuesday to Saturday at midnight GMT per the docs); not recommended for production.

## Checked
Confirmed 2026-11-08 against the Strapi CLI installation page (read in full): the options table, notes and error combinations. Added the missing `--quickstart` error case, `--no-run`, package manager default and command variants. Nothing removed.
Method: docs-only read of cited pages, 2026-11-08
