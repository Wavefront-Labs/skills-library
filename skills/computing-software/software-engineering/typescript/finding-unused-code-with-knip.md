---
id: computing-software.software-engineering.typescript.finding-unused-code-with-knip
name: finding-unused-code-with-knip
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, knip, unused-exports, unused-dependencies, dead-code, monorepo, typescript-quality]
level: practitioner
status: verified
description: "Remove dead files, exports and dependencies in JS/TS projects with knip: entry configuration, framework plugins, workspaces, ignoring false positives, --fix and CI gating."
sources: ["https://knip.dev/overview/getting-started", "https://knip.dev/overview/configuration", "https://knip.dev/features/auto-fix"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Finding unused code with knip

**Goal:** a codebase with no orphaned files, unused exports or unnecessary
dependencies - and a CI check that keeps it that way.

## Run
```bash
npx knip                      # unused files, exports, types, deps, devDeps, unlisted deps, binaries
npx knip --production         # only production entry points; ignores tests/dev tooling (entries in knip.json need a `!` suffix, e.g. "src/main.ts!", or knip reports their dependencies as unused: tested)
npx knip --include files,dependencies
npx knip --fix --allow-remove-files   # remove unused exports/deps/files (review the diff!; tested: it deleted an orphan file and an unused dependency)
```

## Configure entries
knip builds a module graph from entry points; everything unreachable is unused. Most
frameworks are auto-detected via plugins (Next.js, Vite, Vitest, Jest, ESLint, Storybook,
GitHub Actions...). Add what it cannot infer (an `entry` file's own exports are not reported as unused by default; tested):
```json
// knip.json
{
  "$schema": "https://unpkg.com/knip@6/schema.json",   // knip 6.42 was current; the @5 schema URL also still resolved
  "entry": ["src/main.ts", "scripts/*.ts"],
  "project": ["src/**/*.ts", "scripts/**/*.ts"],
  "ignore": ["src/generated/**"],
  "ignoreDependencies": ["@types/node"],
  "ignoreExportsUsedInFile": true
}
```
Monorepos: `"workspaces": { "packages/*": { "entry": ["src/index.ts"] } }` - knip reads each
workspace's package.json and finds deps declared in the wrong workspace.

## Interpreting findings
- **Unused dependency**: listed in package.json, never imported (or only in a config knip
  doesn't understand - add the plugin/entry rather than ignoring).
- **Unlisted dependency**: imported but not declared (works by hoisting luck; breaks in
  pnpm/strict installs). Add it.
- **Unused export**: exported but imported nowhere. In libraries, public API exports must be
  reachable from the package entry (`exports`), so knip treats them as used.
- Dynamic imports with computed paths and reflection-based loading can't be traced - list them as entries.

## Rolling out
Start with `--include files,dependencies` (highest value, fewest false positives), fix, then
add exports and types. Use `--reporter compact` and gate in CI:
```json
"scripts": { "knip": "knip --max-issues 0" }
```
Alternatives: `ts-prune` (unmaintained; last npm release 2022), `depcheck` (deps only). Knip also hints when a config `ignore` pattern matches nothing, so prune dead entries.

## Verify
- [ ] `npx knip` exits 0 in CI.
- [ ] Removed dependencies confirmed by a clean `npm ci && npm run build && npm test`.
