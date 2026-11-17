---
id: computing-software.web-development.trpc.initialize-trpc-once
name: initialize-trpc-once
category: computing-software
field: web-development
product: trpc
tags: [trpc, inittrpc, router, procedure, setup]
level: intro
status: docs-checked
description: "Create the tRPC instance with initTRPC exactly once per app and export router and publicProcedure from one file; multiple instances break mergeRouters."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/routers.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Initialize tRPC exactly once per application. The docs warn that multiple instances cause problems: for example `t.mergeRouters()` throws when the routers come from different instances that each set a transformer or error formatter. So create `t` in one file (conventionally `server/trpc.ts`) and import `router` and your procedures from it everywhere.

```ts
import { initTRPC } from '@trpc/server';

const t = initTRPC.create();

export const router = t.router;
export const publicProcedure = t.procedure;
```

Note that the file exports selected members of `t` (`router`, `publicProcedure`) rather than `t` itself. The docs say this establishes a set of procedures to use idiomatically in your codebase. The variable name `t` is arbitrary.

Chain builder methods before `create()` to configure the instance: `initTRPC.context<Context>().meta<Meta>().create({ ...runtime config })`. See `computing-software.web-development.trpc.runtime-configuration-options` for the options.

## Checked

2026-11-04: read in full against the tRPC docs repo (trpc/trpc, docs repo www/v11/docs/): server/routers.md (Initialize tRPC, Advanced usage). Every parameter name, default, error string and code sample left in this skill appears on those pages. Removed: the Self-check grep step, the 'incompatible types' failure-mode claim and the 'small vocabulary' gloss.

Method: documentation only; no commands were run.
