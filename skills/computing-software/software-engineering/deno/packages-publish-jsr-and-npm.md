---
id: computing-software.software-engineering.deno.packages-publish-jsr-and-npm
name: packages-publish-jsr-and-npm
category: computing-software
field: software-engineering
product: deno
tags: [packages, publishing, jsr, deno-publish, deno-pack, bump-version, conventional-commits]
level: advanced
status: docs-checked
description: "Choose a registry, publish to JSR with deno publish, build npm tarballs with deno pack, and automate workspace releases with deno bump-version."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/packages/publishing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Registries: JSR is recommended for Deno-first packages (TypeScript accepted directly, docs generated from JSDoc, serves Deno, Node.js and others). npm suits Node.js consumers. deno.land/x is legacy; prefer JSR for new packages.

JSR config; the name is always scoped, and you create the scope on jsr.io on first publish:

```json title="deno.json"
{
  "name": "@scope/my-package",
  "version": "1.0.0",
  "exports": "./mod.ts"
}
```

```sh
deno publish --dry-run   # verify the file list and metadata
deno publish             # opens jsr.io to authenticate, then publishes
```

`deno publish` type-checks and verifies exports don't rely on anything outside the package.

npm: `deno pack` (Deno 2.8+) transpiles TypeScript, generates type declarations and the `package.json` npm expects. For fine-grained control use dnt.

```sh
deno pack
npm publish ./package.tgz
```

In a workspace, `deno publish` publishes every member with a name and version, in dependency order.

`deno bump-version` bumps the version field between releases. At a workspace root with no increment it derives each member's bump from Conventional Commits since the last release, rewrites `jsr:` constraints in the root import map, and prepends a changelog entry to `Releases.md`. The std library uses `deno bump-version --import-map import_map.json` in a CI workflow that opens a release PR.

## Checked

2026-11-04. Confirmed against the Deno Publishing packages page: registry guidance, JSR config, publish commands, `deno pack` from Deno 2.8, dnt, workspace publishing, bump-version behaviour. Removed the `deno bump-version patch` example, which the page does not show.

Method: documentation only; no commands were run.
