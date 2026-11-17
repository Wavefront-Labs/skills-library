---
id: computing-software.web-development.payload-cms.typescript-types
name: typescript-types
category: computing-software
field: web-development
product: payload-cms
tags: [typescript, generate-types, payload-types, interfacename]
level: intro
status: docs-checked
description: "Generate payload-types.ts with generate:types, customise outputFile and declare, and add custom schema."
sources:
  - https://payloadcms.com/docs/typescript/generating-types
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Generating TypeScript types

Goal: get types from your config.

```bash
pnpm payload generate:types
```

Options under `typescript`:

```ts
export default buildConfig({
  typescript: {
    declare: false,                                  // default true
    outputFile: path.resolve(dirname, './generated-types.ts'),
    schema: [({ jsonSchema }) => {
      jsonSchema.$defs.Test = { type: 'object', properties: {} }
      return jsonSchema
    }],
  },
})
```

With `declare` on (default) the generated file augments the module:

```ts
declare module 'payload' {
  export interface GeneratedTypes extends Config {}
}
```

so `payload.find` and friends infer collection types. With `declare: false` (useful when the types file is shared with projects that do not have Payload installed) add that `declare module` statement yourself, importing `Config` from the generated file.

`array`, `group` and named `tab` fields generate a top-level interface only when you set `interfaceName`; blocks always generate one and `interfaceName` overrides the name. Top-level names can collide, so scope them (for example `MetaGroup`). Set `typescript.generateInputTypes: true` for write-shaped `*Input` types. Re-run the command after schema changes. If Payload cannot find the config (for example it lives in `src`), set `PAYLOAD_CONFIG_PATH` in the npm script.

Verify: the output file (default `payload-types.ts` next to the config) exists and has an interface for each collection.

## Checked

2026-11-04. Read typescript/generating-types. Confirmed: the generate:types command, typescript.declare defaulting to true and the manual declare module statement when disabled, outputFile defaulting to payload-types.ts next to the config, typescript.schema functions receiving jsonSchema and returning it, interfaceName rules for array, group, named tab and block fields, the naming collision warning, generateInputTypes (opt-in), and PAYLOAD_CONFIG_PATH in an npm script. Removed: the claim that payload build also generates types (not on the page) and the slug-typo verify step.
Method: documentation only; no commands were run.
