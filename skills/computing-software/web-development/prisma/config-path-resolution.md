---
id: computing-software.web-development.prisma.config-path-resolution
name: config-path-resolution
category: computing-software
field: web-development
product: prisma
tags: [prisma-config-path-resolution, prisma, config-flag, npx-prisma-subdirectory, monorepo-prisma-config]
level: practitioner
status: docs-checked
description: "Fix the Could not find Prisma Schema error when running prisma from a subdirectory by understanding config discovery, relative path rules, --config and monorepos."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/reference/prisma-config-reference.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# How the CLI finds and resolves the config

Paths inside the config (`schema`, `migrations`) are resolved relative to the config file, not to the current directory. Separately, the CLI has to find the config file itself.

- `pnpm prisma ...` with a local install finds the config from the project root or any subdirectory.
- `npx prisma ...` or `bunx prisma ...` finds it only when run from the project root, where `package.json` declares Prisma. From `src/`, `npx prisma validate` fails with "Error: Could not find Prisma Schema...". Fix with `--config`:

```
npx prisma validate --config ../prisma.config.ts
```

- Custom location: `prisma validate --config ./path/to/myconfig.ts`.
- Global installs (`npm i -g prisma`) may not find the config or the `prisma/config` module. Prefer a local install, or use `prisma/config` locally and pass `--config`.
- Monorepos: Prisma in the workspace root lets `pnpm prisma` detect the config from subdirectories; Prisma in a subpackage such as `./packages/db` means run commands from that package or deeper.

## Checked
2026-11-03. Confirmed by reading the Prisma ORM v7 docs pages for the topic of this skill (Prisma Migrate getting started, mental model, development and production, baselining, customizing migrations, prototyping, troubleshooting, patching and hotfixing, generating down migrations, squashing, seeding, native types, unsupported features, native functions and extensions, limitations and known issues, and the Prisma Config reference). Commands, flags, error text, privilege lists, defaults and version notes were matched to those pages. Removed: unsupported detail about the exact SQL Server and MySQL lock mechanisms (migrate-deploy-production) and an inferred sentence about v6 experimental keys (config-removed-options).
Method: documentation only; no commands were run.
