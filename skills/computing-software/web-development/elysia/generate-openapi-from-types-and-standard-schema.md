---
id: computing-software.web-development.elysia.generate-openapi-from-types-and-standard-schema
name: generate-openapi-from-types-and-standard-schema
category: computing-software
field: web-development
product: elysia
tags: [openapi, from-types, type-gen, mapjsonschema, zod, valibot, effect]
level: advanced
status: docs-checked
description: "Enable OpenAPI type generation with fromTypes, fix production and monorepo path problems, and map Zod, Valibot or Effect schemas with mapJsonSchema."
sources:
  - https://elysiajs.com/patterns/openapi.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: get richer OpenAPI docs from TypeScript types, and make non-TypeBox schemas appear in the spec.

## OpenAPI from types

Optional but recommended. By default the plugin uses runtime schemas; `fromTypes` also reads the types of an exported instance. The runtime schema wins when both exist.

1. Export the instance (root file defaults to `src/index.ts`).
2. Give `references` a generator with a path from the project root.

```ts
import { openapi, fromTypes } from '@elysia/openapi'

export const app = new Elysia()
  .use(openapi({ references: fromTypes() }))
  .get('/', { test: 'hello' as const })
```

### Production

When you compile to a binary or bundle, point at a pre-generated declaration file:

```ts
fromTypes(process.env.NODE_ENV === 'production' ? 'dist/index.d.ts' : 'src/index.ts')
```

### Troubleshooting

- Explicit types may not resolve; wrap them with `type Prettify<T> = { [K in keyof T]: T[K] } & {}` and return `Prettify<User>`. Implicit types work best.
- Guessing the project root is unreliable (especially monorepos): `fromTypes('src/index.ts', { projectRoot: path.join('..', import.meta.dir) })`.
- With several tsconfig files, choose one relative to the root: `fromTypes('src/index.ts', { tsconfigPath: 'tsconfig.dts.json' })`.

## Standard Schema libraries

Elysia uses each schema's native JSON Schema conversion when it exists. Otherwise supply `mapJsonSchema` keyed by library:

```ts
// Zod 4
openapi({ mapJsonSchema: { zod: z.toJSONSchema } })
// Zod 3
import { zodToJsonSchema } from 'zod-to-json-schema'
openapi({ mapJsonSchema: { zod: zodToJsonSchema } })
// Valibot
import { toJsonSchema } from '@valibot/to-json-schema'
openapi({ mapJsonSchema: { valibot: toJsonSchema } })
// Effect
import { JSONSchema } from 'effect'
openapi({ mapJsonSchema: { effect: JSONSchema.make } })
```

## Gotchas

- Zod (per the page) has no `toJSONSchema` method on the schema, hence the mapper; Zod 4 passes `z.toJSONSchema`, Zod 3 needs the `zod-to-json-schema` package, Valibot needs `@valibot/to-json-schema`.
- The page uses both the named `import { openapi }` and the default `import openapi` forms.

## Checked

2026-11-07. Read in full: patterns/openapi. Confirmed "OpenAPI from types" (default `src/index.ts`, exported instance, `fromTypes()`, runtime schema takes precedence), the production `dist/index.d.ts` pattern, the three troubleshooting caveats (`Prettify`, `projectRoot`, `tsconfigPath`), and the `mapJsonSchema` examples for Zod 4, Zod 3, Valibot and Effect. Nothing removed.

Method: documentation only; no commands were run.
