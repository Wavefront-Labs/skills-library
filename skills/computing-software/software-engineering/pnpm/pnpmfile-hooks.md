---
id: computing-software.software-engineering.pnpm.pnpmfile-hooks
name: pnpmfile-hooks
category: computing-software
field: software-engineering
product: pnpm
tags: [pnpmfile, read-package-hook, update-config-hook, after-all-resolved, before-packing, pre-resolution, global-pnpmfile]
level: advanced
status: docs-checked
description: "Hook into pnpm installs with .pnpmfile.mjs: readPackage, updateConfig, preResolution, afterAllResolved, beforePacking, removed hooks, CLI precedence, location settings."
sources:
  - https://pnpm.io/pnpmfile
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Hooks go in `.pnpmfile.mjs` (or `.cjs`) next to the lockfile, exported as `hooks`.

```js
export const hooks = {
  readPackage(pkg, context) {
    if (pkg.name === 'foo') pkg.dependencies = { ...pkg.dependencies, bar: '^2.0.0' }
    context.log('patched foo')
    return pkg
  },
}
```

- `readPackage(pkg, context)`: mutates a dependency manifest before resolution, in memory only; the lockfile records the pnpmfile checksum and re-resolves when it changes. It cannot stop builds; use `allowBuilds`. To change files on disk use `pnpm patch`.
- `updateConfig(config)`: changes resolved settings (since v12.4.1 all sources, absent when unset). Returning `registriesByScope` replaces routing. Command-line values win (v12.8.0).
- `preResolution(options, logger)`: mutate `options.wantedLockfile` or `currentLockfile` in place; the return value is ignored.
- `afterAllResolved(lockfile, context)`: mutate the lockfile before it is written.
- `beforePacking(pkg, dir, context)`: change the tarball `package.json` only.
- Removed or deprecated: `importPackage` (removed v12.0.0), `filterLog` (deprecated v12.0.0), `hooks.fetchers` (removed v11.0.0).
- With `sharedWorkspaceLockfile: false`, each project runs its own pnpmfile, then the root one.
- Settings: `pnpmfile` (paths), `globalPnpmfile` (prefer local), `ignorePnpmfile`.

## Checked

2026-11-04. Confirmed against pnpm.io/pnpmfile: hook list and semantics, readPackage limitations, updateConfig (v12.4.1, v12.8.0, registriesByScope), preResolution, afterAllResolved, beforePacking, removed/deprecated hooks, per-project pnpmfile order, pnpmfile/globalPnpmfile/ignorePnpmfile settings. Removed: the generic closing Check line (not stated on the page).
Method: documentation only; no commands were run.
