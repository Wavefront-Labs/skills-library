---
id: computing-software.web-development.vite.client-types
name: client-types
category: computing-software
field: web-development
product: vite
tags: [vite-client-types, asset-type-shims, svg-module-override]
level: practitioner
status: docs-checked
description: "Add vite/client types for asset imports, import.meta.env and import.meta.hot via tsconfig types or a triple-slash directive, and override defaults like *.svg."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/features.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Vite's default types cover its Node.js API. For client code add `vite/client`:

```json
{ "compilerOptions": { "types": ["vite/client", "some-other-global-lib"] } }
```

If `compilerOptions.types` is set, only those packages enter the global scope (recommended since TS 5.9). Alternative: a `vite-env.d.ts` with `/// <reference types="vite/client" />`.

It shims: asset imports (such as `.svg`), the `import.meta.env` constants, and the HMR API on `import.meta.hot`.

Override a default by putting your typings in a file that is referenced before `vite/client`:

```ts
declare module '*.svg' {
  const content: React.FC<React.SVGProps<SVGElement>>
  export default content
}
```

With `types`, add that file to `include` in `tsconfig.json`. With triple-slash directives, reference your override file first, then `vite/client`.

## Checked

Date: 2026-11-07. Read the Client Types section of features.md (features.md read in full): `vite/client` in `compilerOptions.types`, the TS 5.9 recommendation, the triple-slash alternative, the three shims, and the `*.svg` override example with `include` and reference ordering. All matched; nothing trimmed.

Method: documentation only; no commands were run.
