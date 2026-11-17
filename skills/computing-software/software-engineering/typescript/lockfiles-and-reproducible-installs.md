---
id: computing-software.software-engineering.typescript.lockfiles-and-reproducible-installs
name: lockfiles-and-reproducible-installs
category: computing-software
field: software-engineering
product: typescript
tags: [npm, package-json, npm-ci, package-lock, pnpm-lock, yarn-lock, frozen-lockfile, reproducible-builds, corepack, packagemanager-field]
level: practitioner
status: verified
description: "Make JavaScript installs reproducible: commit lockfiles, use npm ci / --frozen-lockfile in CI, pin the package manager with corepack, and resolve lockfile conflicts."
sources: ["https://docs.npmjs.com/cli/commands/npm-ci", "https://docs.npmjs.com/cli/configuring-npm/package-lock-json", "https://pnpm.io/cli/install#--frozen-lockfile", "https://nodejs.org/api/corepack.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lockfiles and reproducible installs

**Goal:** every developer and CI run installs the exact same dependency tree, and CI
fails loudly when package.json and the lockfile disagree.

## Rules
1. Commit the lockfile (`package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `bun.lock`)
   for apps AND libraries (libraries' lockfiles are ignored by consumers but keep your CI stable).
2. One package manager per repo. Delete stray lockfiles from others.
3. Pin the manager version in package.json:
   ```json
   { "packageManager": "pnpm@9.12.0" }
   ```
   With corepack (`corepack enable`), running `pnpm` uses exactly that version. Note
   corepack is no longer bundled from Node 25; install it with `npm i -g corepack`.
4. Pin Node too: `"engines": { "node": ">=20.11 <21" }` plus `.nvmrc` / `.node-version`.

## CI install commands
| Manager | CI command | Behaviour |
|---|---|---|
| npm | `npm ci` | deletes node_modules, installs exactly the lockfile, errors if out of sync with package.json |
| pnpm | `pnpm install --frozen-lockfile` | default when `CI=true` (tested on pnpm 12.14: out-of-sync lockfile fails) |
| yarn berry | `yarn install --immutable` | |
| bun | `bun install --frozen-lockfile` | errors "lockfile had changes, but lockfile is frozen" (tested on bun 1.4.3) |
Never `npm install` in CI; it may rewrite the lockfile and drift.

## Updating
- `npm install pkg@^2.3` updates package.json and the lockfile together; commit both.
- `npm update` / `pnpm update` moves within ranges; review the lockfile diff.
- Renovate/Dependabot keep this flowing with small PRs.

## Lockfile merge conflicts
Do not hand-merge. Take either side, then regenerate:
```bash
git checkout --theirs package-lock.json   # or --ours
npm install                               # re-resolves against merged package.json
```
pnpm can resolve `pnpm-lock.yaml` conflicts itself: run `pnpm install` and review the result (pnpm docs warn it may not pick the right head).

## Gotchas
- `npm ci` errors when package.json and the lockfile disagree (tested: "lock file's is-odd@2.0.0 does not satisfy is-odd@3.0.1") and removes an existing `node_modules` first.
- Private registries: `.npmrc` with `${NPM_TOKEN}` env interpolation; never commit tokens.

## Verify
- [ ] CI uses `npm ci` (or frozen equivalent) and caches the package manager store, not node_modules.
- [ ] `git status` is clean after a CI install.
