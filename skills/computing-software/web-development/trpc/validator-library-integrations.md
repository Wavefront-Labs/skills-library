---
id: computing-software.web-development.trpc.validator-library-integrations
name: validator-library-integrations
category: computing-software
field: web-development
product: trpc
tags: [trpc, validator, standard-schema, valibot, arktype]
level: practitioner
status: docs-checked
description: "How to plug Zod, Yup, Superstruct, Valibot, ArkType, Effect, Sury, scale-ts, Typia and TypeBox into .input() and .output(), per the v11 validator page."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/validators.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
tRPC works with libraries that implement Standard Schema, plus special-cased ones. The validators page shows each library used in `.input()` and `.output()`:

- Zod (default recommendation): `.input(z.object({ name: z.string() }))`.
- Yup: `yup.object({ name: yup.string().required() })`.
- Superstruct: `object({ name: string() })`.
- Valibot: `v.object({ name: v.string() })`.
- ArkType: `type({ name: 'string' })`.
- Effect: wrap the schema, `Schema.standardSchemaV1(Schema.Struct({ name: Schema.String }))`.
- Sury: `S.schema({ name: S.string })`.
- scale-ts: `$.object($.field('name', $.str))`.
- Typia: `typia.createAssert<IBbsArticle.IStore>()` for input and output.
- TypeBox: wrapped with an adapter, `wrap(Type.Object({ name: Type.String() }))` from `@typeschema/typebox`.
- @robolex/sure: wrapped in an `err(...)` helper that throws the failure result.

Zod is the docs' default recommendation: it has a strong ecosystem, and the docs call it a great choice if you have no opinion. A runtypes example is commented out in the page source as broken, so do not rely on it.

The page says conforming to Standard Schema is recommended for new validator libraries; the supported parsing interfaces live in `parser.ts` in the `@trpc/server` package.

## Checked

2026-11-07. Read in full from a clone of github.com/trpc/trpc (main, commit fe64009), www/v11/docs/server/validators.md (read in full, all library examples compared with the skill bullets): Zod, Yup, Superstruct, scale-ts, Typia, ArkType, Effect, Valibot, Sury, @robolex/sure and TypeBox, and the "Contributing your own Validator Library" section.

Removed or corrected: the unsourced advice to pick one library and to prefer Standard Schema "so no adapter is needed", the claim that Zod has the largest ecosystem, and the invented Verify step.

Method: documentation only; no commands were run.
