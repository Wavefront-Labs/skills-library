---
id: computing-software.web-development.bun.bun-build-cli
name: bun-build-cli
category: computing-software
field: web-development
product: bun
tags: [bun-build, build-api, bundler-target, bundler-naming]
level: practitioner
status: docs-checked
description: "Bundle with bun build or Bun.build: target, format, splitting, sourcemaps, externals, define, env prefix, naming, compile, return value and gotchas."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/bundler/index.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
const result = await Bun.build({
  entrypoints: ["./src/index.tsx"], outdir: "./dist",
  target: "browser", format: "esm", splitting: true, sourcemap: "linked",
  minify: true, external: ["react"],
  define: { "process.env.NODE_ENV": JSON.stringify("production") },
  env: "PUBLIC_*",
  naming: { entry: "[dir]/[name].[ext]", chunk: "[name]-[hash].[ext]", asset: "[name]-[hash].[ext]" },
});
```
```bash
bun build ./src/index.tsx --outdir ./dist --splitting --sourcemap=linked --minify \
  --external react --define 'process.env.NODE_ENV="production"' --env 'PUBLIC_*'
bun build ./cli.ts --compile --outfile mycli     # standalone executable
```

Defaults: target `browser`, format `esm`, no splitting, no sourcemap, `packages: "bundle"`. Result: `success`, `outputs` (BuildArtifact blobs), `logs`. Failure rejects with `AggregateError` unless `throw: false`.

Gotchas:
- Without `outdir` nothing is written; read `outputs`.
- `sourcemap: "linked"` needs `outdir`.
- `--check` (or `check: true`) type-checks; `dts: true` / `--dts` emits declarations, implies check, and cannot be used with `compile`.
- `cjs` and `iife` are experimental; `cjs` changes default target to `node`; top-level await is listed as an `esm` feature.
- A Bun shebang in an entry makes the default target `bun`.
- A string `naming` applies only to entry points.
- `define` values are JSON strings, identifiers or property paths; the CLI example quotes the value: `--define STRING='"value"'`.
- `env` accepts `"inline"`, `"disable"`, or a prefix ending in `*`.

## Checked

2026-11-04. Confirmed against bun docs bundler/index.mdx: Bun.build and CLI options for target, format, splitting, sourcemap values and linked-needs-outdir, packages default bundle, naming tokens and string-versus-object behaviour, define, env modes, check and dts notes, compile, return shape success/outputs/logs, AggregateError versus throw false, bun shebang target default, cjs default target node and experimental cjs/iife. Removed an unsourced shell-quoting claim and an inferred top-level-await requirement.

Method: documentation only; no commands were run.
