---
id: computing-software.web-development.appwrite.appwrite-cli-type-generation
name: appwrite-cli-type-generation
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, cli, type-generation, typescript, databases]
level: practitioner
status: docs-checked
description: "Generate typed models from your table schema with appwrite types and a typed SDK with appwrite generate."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/databases/type-generation/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/tooling/command-line/generate/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: type safety for tables.

Type definitions:
1. Install and initialize the CLI, then run `appwrite pull tables` to pull tables from your project. The types page says the CLI reads the schema from your project's `appwrite.json`; the CLI installation page names the config file `appwrite.config.json`, so check which your CLI version writes.
2. Run `appwrite types [options] <output-directory>`, for example `appwrite types --language ts ./types`. `--language` / `-l` choices: `ts`, `js`, `php`, `kotlin`, `swift`, `java`, `dart`, `auto`; `auto` is the default if the option is skipped.
3. `--strict` / `-s` enables strict type generation: all columns follow language conventions, even if that causes mismatches with the schema defined in your Appwrite console.

Typed SDK: `appwrite generate` detects your project's language and writes to a `generated/appwrite/` directory. Options: `-o, --output <directory>` (default `generated`), `-l, --language <language>` (supported: `typescript`), `--server <mode>` (`auto`, `true`, `false`; default `auto`). Generated files: `types.ts` (types from the schema), `databases.ts` (typed helpers), `index.ts` (entry point), `constants.ts` (endpoint and project ID; update these before use).

Usage: `import { databases } from "./generated/appwrite"`, then for example `databases.use("main").use("customers")`, with `create`, `get`, `list`, `update`, `delete`, and `createMany`, `updateMany`, `deleteMany` helpers. `list` takes a typed query builder: `queries: (q) => [q.equal("name", "x"), q.limit(10)]`.

Gotcha: regenerate after schema changes; the types come from the pulled schema, so pull tables first.

## Checked

2026-11-04. Confirmed against the Appwrite docs pages Type generation (databases/type-generation), Generate SDK (tooling/command-line/generate) and CLI Commands: `appwrite pull tables`, `appwrite types` options and choices, `--strict` meaning, `appwrite generate` options, defaults, output folder and file list, and the helper names. Removed: the advice about committing generated output or regenerating in CI, and the compile-failure Verify step, which no page states.
Method: documentation only; no commands were run.
