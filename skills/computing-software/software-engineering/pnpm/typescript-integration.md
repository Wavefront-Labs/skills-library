---
id: computing-software.software-engineering.pnpm.typescript-integration
name: typescript-integration
category: computing-software
field: software-engineering
product: pnpm
tags: [typescript, preserve-symlinks, types-packages, missing-peer-types, types-fixer-plugin, duplicate-types-react]
level: practitioner
status: docs-checked
description: "Use TypeScript with pnpm: avoid preserveSymlinks, fix duplicate or missing @types packages with addMissingPeerTypes, packageExtensions or the types-fixer config dependency."
sources:
  - https://pnpm.io/typescript
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
pnpm works with TypeScript out of the box most of the time.

- Do not set `preserveSymlinks: true` in `tsconfig`; TypeScript then cannot resolve type dependencies through the linked `node_modules`. If you truly need it, set pnpm's `nodeLinker` to `hoisted`.
- Workspace problem: several versions of an `@types/` package (for example `@types/react`) when a library such as `antd` needs the types but does not list them as a peer. Fixes, any one of:

```yaml
# pnpm-workspace.yaml
addMissingPeerTypes: true
```
makes the matching `@types` package an optional peer of every package that peer-depends on a library (pnpm does not install a `@types` package nothing in the workspace depends on), or extend the one package:

```yaml
packageExtensions:
  antd:
    peerDependencies:
      '@types/react': '*'
```
or install the config dependency:

```sh
pnpm add @pnpm/plugin-types-fixer --config
```

- `saveTypes: true` (or `pnpm add --save-types express`) saves available `@types/*` into `devDependencies` when adding.
- With the global virtual store, `addMissingPeerTypes` is what lets types resolve next to the peer-depending package.

## Checked

2026-11-04. Confirmed the preserveSymlinks advice, addMissingPeerTypes, the packageExtensions example and the @pnpm/plugin-types-fixer command against pnpm.io/typescript, and saveTypes and the global virtual store note against pnpm.io/settings/other and pnpm.io/settings/peer-dependencies. Removed the unsourced closing Check line.

Method: documentation only; no commands were run.
