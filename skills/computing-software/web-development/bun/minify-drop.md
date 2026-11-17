---
id: computing-software.web-development.bun.minify-drop
name: minify-drop
category: computing-software
field: web-development
product: bun
tags: [minify, drop-console, dead-code-elimination, keep-names]
level: practitioner
status: docs-checked
description: "Minify Bun bundles selectively: whitespace, syntax and identifier modes, --production, keep-names, dropping console or debugger calls, and pure annotations."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/bundler/minifier.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
await Bun.build({
  entrypoints: ["./src/index.ts"], outdir: "./dist",
  minify: { whitespace: true, syntax: true, identifiers: true, keepNames: true },
});
```
```bash
bun build ./src/index.ts --outdir dist --minify
bun build ./src/index.ts --outdir dist --minify-syntax --keep-names
bun build ./src/index.ts --outdir dist --production
bun build ./src/index.ts --outdir dist --drop=console --drop=debugger --drop=assert
```

- `--minify` = whitespace + syntax + identifiers. `--production` also sets `process.env.NODE_ENV` to production and enables production JSX.
- Syntax mode rewrites to shorter forms, folds constants and removes dead code: `if (false)`, code after `return`, `while (false)`, empty blocks.
- `/*@__PURE__*/` is always respected; an unused `const x = /*@__PURE__*/ expensive();` is removed.
- `--drop=console` turns each `console.*` call into `void 0` (`x = console.error("e")` becomes `x=void 0`). `--drop=assert` removes `assert(...)` and `assert.equal(...)`.

Gotchas:
- Identifier minification keeps keywords, globals, named exports, `exports` and `module`.
- Identifier minification makes error messages harder to read; combine it with `--keep-names` for better stack traces (it preserves `.name` on functions and classes).
- Only `/*!` license comments survive.
- `--minify-syntax` alone gives smaller output while keeping readable identifiers for debugging.

## Checked

2026-11-04. Confirmed against bun docs bundler/minifier.mdx: --minify modes, --production extras, granular flags, JS minify object including keepNames, syntax-mode rewrites and dead code removal examples, always-active pure annotations, identifier preservation list, license-comment retention, drop=debugger/console/custom-name behaviour including x=void 0, keep-names semantics. Reworded two gotchas to the page's own wording.

Method: documentation only; no commands were run.
