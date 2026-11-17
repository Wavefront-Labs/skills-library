---
id: computing-software.software-engineering.pnpm.custom-resolvers-and-fetchers
name: custom-resolvers-and-fetchers
category: computing-software
field: software-engineering
product: pnpm
tags: [custom-resolver, custom-fetcher, can-resolve, should-refresh-resolution, delegate-envelope, custom-resolution-type, pnpmfile-finders]
level: sme
status: docs-checked
description: "Write pnpm custom resolvers and fetchers in .pnpmfile.cjs: canResolve and resolve, custom: resolution types, shouldRefreshResolution, fetch delegation and pnpm 12 limits."
sources:
  - https://pnpm.io/pnpmfile
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Export top-level `resolvers` and `fetchers` from `.pnpmfile.cjs`:

```js
const resolver = {
  canResolve: (w) => w.alias.startsWith('@company/'),
  resolve: async (w) => ({
    id: `${w.alias}@1.0.0`,
    resolution: { type: 'custom:cdn', url: 'https://cdn.example.com/x.tgz' },
  }),
}
const fetcher = {
  canFetch: (id, r) => r.type === 'custom:cdn',
  fetch: (cafs, r) => ({ delegate: { tarball: r.url, integrity: r.integrity } }),
}
module.exports = { resolvers: [resolver], fetchers: [fetcher] }
```

- `wantedDependency` has `alias` and `bareSpecifier`; `opts` has `lockfileDir`, `projectDir`, `preferredVersions`.
- Custom resolution types must start with `custom:` and need a matching custom fetcher.
- First resolver or fetcher returning true wins; custom resolvers run before built-ins.
- `shouldRefreshResolution(depPath, pkgSnapshot)` returning true forces full re-resolution (time-based invalidation). Skipped with a frozen lockfile.
- A fetch result is `filesIndex`, optional `manifest`, `requiresBuild`, `local`. Results from `localTarball`, `remoteTarball` or `directory` must come back unchanged; to alter files return `{ delegate }`, a single-step envelope with a complete fetchable resolution.
- pnpm 12: `fetchers` offers `localTarball`, `remoteTarball`, `directory`; `gitHostedTarball`, `git`, `binary` require the envelope.
- Keep `canResolve`, `canFetch` and `shouldRefreshResolution` cheap; they run for every dependency.
- `finders` exports feed `pnpm list` and `pnpm why` with `--find-by`.

## Checked

2026-11-04. Confirmed against pnpm.io/pnpmfile: top-level resolvers/fetchers exports, wantedDependency and opts fields, custom: type prefix, shouldRefreshResolution and frozen-lockfile skip, delegate envelope rules, pnpm 12 fetchers list, resolver ordering, cheap-check advice, finders. Removed: the generic closing Check line (not stated on the page).
Method: documentation only; no commands were run.
