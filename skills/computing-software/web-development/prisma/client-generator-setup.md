---
id: computing-software.web-development.prisma.client-generator-setup
name: client-generator-setup
category: computing-software
field: web-development
product: prisma
tags: [prisma-client-generator-setup, prisma, prisma-client-generator, importfileextension-tsx, prisma-client-js-deprecated]
level: practitioner
status: docs-checked
description: "Configure the prisma-client generator with required output, runtime, moduleFormat and extension options, fix the tsx internal/class.js error, and replace Prisma.validator."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-schema/overview/generators.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# The prisma-client generator

```prisma
generator client {
  provider = "prisma-client"
  output   = "../src/generated/prisma"
}
```

`prisma-client` is the default generator. It emits plain TypeScript into your own tree, so `output` is required (no generation into `node_modules`) and the files bundle like app code. Run `npx prisma generate`. Differences from `prisma-client-js`: no `.env` loading at runtime (use `dotenv` or set variables yourself), ESM or CommonJS via `moduleFormat`, no `Prisma.validator` (use TypeScript's `satisfies`).

Optional fields and defaults:
- `runtime`: `nodejs` default; also `deno`, `bun`, `workerd` (alias `cloudflare`), `vercel-edge` (alias `edge-light`), `react-native`.
- `moduleFormat`: `esm` or `cjs`, inferred from the environment.
- `generatedFileExtension`: `ts` default (`ts`, `mts`, `cts`).
- `importFileExtension`: inferred; `ts`, `mts`, `cts`, `js`, `mjs`, `cjs`, or empty.
- `engineType = "client"` appears in the docs example.

Trap: running under `tsx` and getting `Cannot find module './internal/class.js'`. Generated imports use `.js` (ESM convention) which `tsx` cannot map to `.ts` files. Set `importFileExtension = "ts"`.

`prisma-client-js` is deprecated; it needs `@prisma/client`, generates into `node_modules`, and takes `previewFeatures` and `binaryTargets` (default `"native"`).

## Checked

2026-11-03. Read in the Prisma docs repository (prisma-schema/overview/generators pages, orm/v7): prisma-client as default, required output, no .env loading, moduleFormat, runtime values and aliases, generatedFileExtension, importFileExtension, the tsx class.js fix, satisfies instead of Prisma.validator, prisma-client-js deprecation, previewFeatures and binaryTargets.

Method: documentation only; no commands were run.
