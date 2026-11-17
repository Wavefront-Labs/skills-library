---
id: computing-software.software-engineering.typescript.workspaces-monorepos
name: workspaces-monorepos
category: computing-software
field: software-engineering
product: typescript
tags: [npm, npm-workspaces, pnpm-workspaces, monorepo, workspace-protocol, turborepo, nx, project-references, internal-packages]
level: practitioner
status: verified
description: "Run a JS/TS monorepo with npm or pnpm workspaces: layout, workspace: dependencies, running scripts across packages, TypeScript references and task caching."
sources: ["https://docs.npmjs.com/cli/using-npm/workspaces", "https://pnpm.io/workspaces", "https://turborepo.com/docs", "https://www.typescriptlang.org/docs/handbook/project-references.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Workspaces monorepos (npm / pnpm)

**Goal:** several packages (apps + shared libs) in one repo, linked locally, built in
dependency order, with only changed packages rebuilt.

## Layout
```
package.json            # root: private, devDeps for tooling, workspaces list
pnpm-workspace.yaml     # pnpm only
apps/web/package.json
packages/ui/package.json
packages/config-ts/tsconfig.base.json
```
npm root package.json:
```json
{ "private": true, "workspaces": ["apps/*", "packages/*"] }
```
pnpm-workspace.yaml:
```yaml
packages: ["apps/*", "packages/*"]
```

## Depending on internal packages
```json
"dependencies": { "@acme/ui": "workspace:*" }      // pnpm / yarn / bun
"dependencies": { "@acme/ui": "*" }                // npm links any matching workspace
```
`workspace:*` guarantees the local copy; on pack/publish pnpm rewrites it to the real version (tested: `pnpm pack` wrote `"@acme/ui": "1.0.0"`). With npm, `"*"` resolved to the symlinked workspace (tested).

## Running scripts
```bash
npm run build --workspaces --if-present   # runs in workspace-path order (tested: web before ui), not dependency order
npm run test -w @acme/ui
pnpm -r build                     # topological order
pnpm --filter @acme/web... build  # web and its dependencies
pnpm --filter "...[origin/main]" test   # packages changed since main and their dependents
```

## Why pnpm is often preferred
Strict node_modules: a package can only import what it declares, catching phantom
dependencies that npm's hoisting hides until publish. Content-addressed store saves disk.

## TypeScript across packages
Either:
- **Internal packages consumed as source**: `"exports": { ".": "./src/index.ts" }` and
  let the app's bundler compile them (simplest; no build step for libs), or
- **Built packages with project references**: each lib has `composite: true`, root
  `tsconfig.json` lists `references`, build with `tsc -b`.
Don't mix both for the same package. (`tsc -b` with `composite` and `references` built both packages in order in a test.)

## Task caching
Turborepo (2.x, tested: `dependsOn: ["^build"]` built lib before app and a second run replayed the cached lib) or Nx cache task outputs keyed by inputs; declare `outputs` (`dist/**`) and
dependencies (`"dependsOn": ["^build"]`). Remote cache shares results with CI.

## Gotchas
- Version skew: two packages depending on different React versions produce duplicate
  React at runtime. Use pnpm `overrides` or catalogs (`catalog:`) to align. On pnpm 12.14 both worked from `pnpm-workspace.yaml`, but `"pnpm": { "overrides" }` in package.json was ignored (tested), so keep them in the yaml.
- Root-only devDeps (eslint, typescript) are fine; runtime deps must be declared in the
  package that imports them.

## Verify
- [ ] Fresh clone: one install command, then `build` succeeds from the root.
- [ ] Removing a dependency declaration breaks that package's build (strictness works).
