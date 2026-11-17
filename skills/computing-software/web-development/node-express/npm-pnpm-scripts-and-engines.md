---
id: computing-software.web-development.node-express.npm-pnpm-scripts-and-engines
name: npm-pnpm-scripts-and-engines
category: computing-software
field: web-development
product: node-express
tags: [npm-scripts, package-json-engines, pnpm, corepack, package-managers]
level: practitioner
status: verified
description: "Managing Node projects with npm and pnpm: package.json scripts and lifecycle hooks, engines and packageManager fields, Corepack, workspaces, overrides, and CI install hygiene."
sources:
  - https://docs.npmjs.com/cli/v11/using-npm/scripts
  - https://docs.npmjs.com/cli/v11/configuring-npm/package-json#engines
  - https://pnpm.io/motivation
  - https://nodejs.org/api/corepack.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# npm / pnpm, package.json scripts and engines

## 1. Scripts
```json
{
  "scripts": {
    "dev": "node --watch --env-file=.env src/server.js",
    "build": "tsc -p tsconfig.build.json",
    "start": "node dist/server.js",
    "test": "node --test",
    "lint": "eslint .",
    "check": "npm run lint && npm run typecheck && npm test",
    "prepare": "husky"
  }
}
```
- `npm run <name>` adds `node_modules/.bin` to PATH; `npm test`/`npm start` are shortcuts.
- `pre<name>`/`post<name>` hooks run automatically in npm (ran on npm 11.21.1) and in pnpm 10 (`enablePrePostScripts` defaults to true per the pnpm docs; ran on 10.34.7). Prefer explicit chaining for clarity.
- Pass args after `--`: `npm test -- --test-name-pattern=auth` (ran: 1 of 2 tests selected; `node --test`, `--watch` and `--env-file=.env` all worked on Node 24).
- Cross-platform: avoid `rm -rf`/`export` in scripts; use `node -e`, `rimraf`, or `cross-env` for Windows contributors.
- `npm run` with no arguments lists scripts.

## 2. engines and packageManager
```json
{
  "engines": { "node": ">=22.12 <25" },
  "packageManager": "pnpm@10.18.0"
}
```
- `engines` warns by default (ran: npm 11 printed `EBADENGINE`); enforce with `.npmrc` `engine-strict=true` (ran in npm: `npm install` then failed with `EBADENGINE`) or the same setting in pnpm config (not run).
- `packageManager` + Corepack pins the exact package manager version per repo (`corepack enable`; ran with the `corepack` npm package 0.34.7: `packageManager: pnpm@10.18.0` made `corepack pnpm -v` print 10.18.0). The Node docs say Corepack is no longer distributed starting with Node.js v25, so install it explicitly (`npm i -g corepack`) where missing.

## 3. npm vs pnpm
- pnpm uses a content-addressed store and symlinked `node_modules`: faster installs, less disk, and **strict** dependency resolution (packages can't import undeclared deps - catches phantom dependencies). Some tools assuming a flat `node_modules` need `node-linker=hoisted` or `public-hoist-pattern`.
- Both support workspaces (`"workspaces"` / `pnpm-workspace.yaml`), filtering (`npm -w pkg`, `pnpm --filter pkg`), and `overrides` (npm) / `pnpm.overrides` to force transitive versions for security fixes.

## 4. CI hygiene
- `npm ci` / `pnpm install --frozen-lockfile`: fail if the lockfile is out of sync; never `npm install` in CI.
- Cache the package manager store (actions/setup-node `cache: npm|pnpm`).
- `--ignore-scripts` for installs of untrusted dependency trees; pnpm 10 blocks dependency lifecycle scripts by default (ran: `Ignored build scripts: dep ... Run "pnpm approve-builds"`). The allow-list setting has been renamed between releases (`onlyBuiltDependencies` in 10.x, `allowBuilds` in the current docs); a `pnpm.onlyBuiltDependencies` entry in package.json did not lift the block for a `file:` dependency on 10.34.7, so use `pnpm approve-builds` and check the docs for your version.
- Commit exactly one lockfile.

## Verify
- [ ] Fresh clone + `corepack enable` + frozen install works; engine mismatch fails fast; scripts run on Windows and Linux; one lockfile committed.
