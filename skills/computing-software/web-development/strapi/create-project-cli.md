---
id: computing-software.web-development.strapi.create-project-cli
name: create-project-cli
category: computing-software
field: web-development
product: strapi
tags: [strapi, create-strapi, installation, scaffold, cli, npx]
level: intro
status: docs-checked
description: "Create a new Strapi project with npx create-strapi@latest or pnpm create strapi, and what the prompts ask."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/installation/cli.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Create a Strapi project from the CLI

Run in a terminal:

```bash
npx create-strapi@latest
```

With pnpm:

```bash
pnpm create strapi
```

`npx create-strapi-app@latest` still works and gives the same experience. `npm create strapi@latest` also works (note the dash difference: `npx create-strapi` vs `npm create strapi`).

## Prompts
1. Login/Signup or Skip. Login gives a 30-day trial of the Growth plan; Skip falls back to the CMS Free plan.
2. A few questions. Pressing Enter takes the default. Most default to Yes; the example structure and data question defaults to No.
3. If you answer no to the default SQLite database, the CLI asks for database type, name, host, port, username, password and SSL.

A supported database is required. Skip all questions with flags (see `computing-software.web-development.strapi.cli-install-options`).

Without a `--use-npm`, `--use-pnpm` or `--use-yarn` flag, dependencies are installed with the package manager that ran the create command.

## Checked

Checked 2026-11-04 against the Strapi Installing from CLI page (creating a project, prompts, options and notes). Reworded the self-check question into the stated rule.

Method: documentation only; no commands were run.
