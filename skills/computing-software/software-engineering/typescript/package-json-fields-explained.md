---
id: computing-software.software-engineering.typescript.package-json-fields-explained
name: package-json-fields-explained
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, package-json-fields, engines-field, sideeffects, type-module, files-field, npm]
level: practitioner
status: verified
description: "Get package.json fields right: name/version, type, main vs module vs exports, types, files, engines, sideEffects, bin, private, packageManager and publishConfig."
sources: ["https://docs.npmjs.com/cli/v10/configuring-npm/package-json", "https://nodejs.org/api/packages.html", "https://webpack.js.org/guides/tree-shaking/#mark-the-file-as-side-effect-free", "https://nodejs.org/api/corepack.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# package.json fields explained

**Goal:** a manifest that installs, resolves, tree-shakes and publishes exactly as
intended.

## Identity and type
```json
{
  "name": "@acme/csv",
  "version": "2.1.0",
  "type": "module",
  "private": true
}
```
- `type: "module"` makes `.js` files ESM; `.cjs`/`.mjs` override per file.
- `private: true` blocks accidental `npm publish` (apps, monorepo roots).

## Entry points
```json
{
  "exports": {
    ".": { "types": "./dist/index.d.ts", "import": "./dist/index.js", "require": "./dist/index.cjs" },
    "./package.json": "./package.json"
  },
  "main": "./dist/index.cjs",
  "types": "./dist/index.d.ts"
}
```
- `exports` (when present; added in Node 12.7.0 per the Node docs) is authoritative and modern bundlers/TS (with
  `moduleResolution: NodeNext/Bundler`): unlisted subpaths become **unimportable** - adding
  `exports` to an existing package is a breaking change.
- `types` condition first inside each block. `main`/`types` remain for legacy tools.
- `module` is a bundler-only convention, ignored by Node.

## What gets published
`files: ["dist"]` whitelists contents (package.json, README, LICENSE always included; tested with `npm pack --dry-run`). `.npmignore` is the blacklist alternative and replaces the `.gitignore` fallback: tested, a `.env` listed in `.gitignore` was packed once a `.npmignore` existed, so it is easier to leak secrets.

## Runtime requirements
```json
"engines": { "node": ">=20.11" },
"packageManager": "pnpm@9.12.0"
```
`engines` warns by default (`EBADENGINE` warning); `engine-strict=true` in `.npmrc` makes it an install error (both tested).
`packageManager` pins the tool via Corepack.

## Bundler hints
`"sideEffects": false` (or a list like `["*.css", "./src/polyfills.js"]`) tells bundlers unused
modules can be dropped entirely (tested with esbuild: bare `import "lib"` of a `sideEffects: false` package was dropped). Lying here deletes polyfills/CSS imports in consumers' builds.

## CLIs
```json
"bin": { "acme-csv": "./dist/cli.js" }
```
The file needs `#!/usr/bin/env node`; npm creates shims (including Windows `.cmd`).

## Publishing config
```json
"publishConfig": { "access": "public", "provenance": true, "registry": "https://registry.npmjs.org/" }
```
Scoped packages are private by default on publish without `access: public`.

## Dependencies recap
`dependencies` (runtime), `devDependencies` (build/test), `peerDependencies` (host provides,
e.g. react), `optionalDependencies` (install failure tolerated), `overrides` (force transitive
versions, root only).

## Verify
- [ ] `npm pack --dry-run` lists only intended files; `publint` and `arethetypeswrong` pass.
- [ ] Apps and monorepo roots have `"private": true`.
