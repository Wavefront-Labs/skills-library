---
id: computing-software.web-development.vite.env-typescript-intellisense
name: env-typescript-intellisense
category: computing-software
field: web-development
product: vite
tags: [import-meta-env-types, vite-env-dts, strict-import-meta-env]
level: practitioner
status: docs-checked
description: "Type custom VITE_ variables by augmenting ImportMetaEnv in vite-env.d.ts, make unknown keys an error, and avoid imports that break the augmentation."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/env-and-mode.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`vite/client.d.ts` types `import.meta.env`. To get IntelliSense for your own `VITE_` variables, create `src/vite-env.d.ts`:

```ts
interface ViteTypeOptions {
  // By adding this line, you can make the type of ImportMetaEnv strict
  // to disallow unknown keys.
  // strictImportMetaEnv: unknown
}

interface ImportMetaEnv {
  readonly VITE_APP_TITLE: string
  // more env variables...
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
```

Uncomment `strictImportMetaEnv: unknown` to disallow unknown keys.

If the augmentation is ignored, make sure `vite-env.d.ts` has no `import` statements.

For DOM or WebWorker types, adjust `lib` in `tsconfig.json`, for example `"lib": ["WebWorker"]`.

## Checked

2026-11-07. Confirmed against the "IntelliSense for TypeScript" section of guide/env-and-mode.md (page fetched in full; this section and the `VITE_` prefix passages read line by line): `vite/client.d.ts`, `src/vite-env.d.ts`, the `ViteTypeOptions`, `ImportMetaEnv` and `ImportMeta` snippet with `strictImportMetaEnv`, the `lib` example with `WebWorker`, and the no-`import` warning. Removed the unconfirmed explanation that an import turns the file into a module (the page only says imports break the augmentation).

Method: documentation only; no commands were run.
