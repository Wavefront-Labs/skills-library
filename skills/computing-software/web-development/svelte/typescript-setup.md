---
id: computing-software.web-development.svelte.typescript-setup
name: typescript-setup
category: computing-software
field: web-development
product: svelte
tags: [script-lang-ts, type-only-features, vite-plugin-preprocess, tsconfig-verbatim-module-syntax, svelte-check]
level: practitioner
status: docs-checked
description: "Use TypeScript in Svelte: lang=ts supports type-only syntax, vitePreprocess({ script: true }) for enums and similar, and required tsconfig settings."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/07-misc/03-typescript.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
IDE extensions such as the Svelte VS Code extension catch errors in the editor, and `svelte-check` does the same on the command line (usable in CI).

Add `lang="ts"` to script tags. This allows type-only features, those that vanish when transpiling (annotations, interfaces). Not supported without a preprocessor:
- enums
- `private`, `protected` or `public` modifiers in constructor functions together with initializers
- features not yet at TC39 level 4 and so not implemented in Acorn, the parser used

Preprocessor: with SvelteKit or Vite, use `vitePreprocess` from `@sveltejs/vite-plugin-svelte` with the extra `{ script: true }`:

```ts
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

const config = {
  preprocess: vitePreprocess({ script: true })
};
export default config;
```

With Rollup (rollup-plugin-svelte) or Webpack (svelte-loader), install `typescript` and `svelte-preprocess` and add it to the plugin config. New projects are better off with SvelteKit or Vite.

tsconfig.json:
- `target` of at least `ES2015`, so classes are not compiled to functions.
- `verbatimModuleSyntax: true`, so imports are left as-is.
- `isolatedModules: true`, since the Svelte compiler and tools like Vite do not do the cross-file analysis some TypeScript features need.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Svelte TypeScript docs page: unsupported non-type-only features, `vitePreprocess({ script: true })`, Rollup/Webpack note, and the three tsconfig settings. Nothing removed.
