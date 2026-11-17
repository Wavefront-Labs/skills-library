---
id: computing-software.web-development.strapi.typescript-new-project
name: typescript-new-project
category: computing-software
field: web-development
product: strapi
tags: [strapi, typescript, create-strapi, ts-generate-types, types]
level: intro
status: docs-checked
description: "Create a Strapi project in TypeScript and generate schema types with ts:generate-types."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/typescript.md
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/cli.md
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/installation/cli.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# TypeScript

New project:

```bash
npx create-strapi@latest my-project --typescript
# or
yarn create strapi my-project --typescript
```

`--ts`/`--typescript` initializes the project with TypeScript, which is the default. An existing JavaScript project can be converted using the separate conversion steps in the docs.

## Generated types
`strapi ts:generate-types` generates TypeScript typings for the project schemas (options include `--debug`/`-d`, `--silent`/`-s` and `--out-dir <path>`/`-o <path>`):

```bash
strapi ts:generate-types
```

Related: `computing-software.web-development.strapi.create-project-cli`, `computing-software.web-development.strapi.list-and-generate-commands`.

## Checked

2026-11-04: checked against the Strapi docs pages TypeScript, CLI (strapi ts:generate-types) and CLI installation (`--ts`/`--typescript` default). Confirmed: both create commands, the TypeScript default, the ts:generate-types command and its options. Removed: the advice to re-run after changing content-types, which no page states. Added the two pages that document the default and the command to sources.

Method: documentation only; no commands were run.
