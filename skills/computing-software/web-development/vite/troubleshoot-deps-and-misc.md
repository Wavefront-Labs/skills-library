---
id: computing-software.web-development.vite.troubleshoot-deps-and-misc
name: troubleshoot-deps-and-misc
category: computing-software
field: web-development
product: vite
tags: [linked-package-stale, cpu-profile, externalized-node-module, strict-mode-esm, cjs-default-import]
level: advanced
status: docs-checked
description: "Troubleshoot stale linked packages, CPU profiling, externalized Node modules, sloppy-mode code, cross-drive links on Windows and CJS default imports returning objects."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/troubleshooting.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
- Stale pre-bundled deps with a linked package: the cache key covers lockfile, patches and relevant config, so npm overrides are detected, but `npm link` is not. Run `vite --force` after linking or unlinking; overrides are recommended.
- Performance bottleneck: `vite --profile --open` or `vite build --profile`. In dev, after the page loads press `p` then `q` in the terminal. It writes `vite-profile-0.cpuprofile` (or `<name>.cpuprofile` with `--profile <name>`); upload to speedscope. `vite-plugin-inspect` shows plugin intermediate state.
- `Module "fs" has been externalized for browser compatibility`: Vite does not polyfill Node.js modules. Avoid them in browser code or polyfill manually.
- Strict mode: ESM is always strict, so sloppy-mode code fails (`With statements cannot be used with the "esm" output format`). For dependencies use `patch-package`, `yarn patch` or `pnpm patch`.
- Windows cross-drive links (`subst` drives, symlinks or junctions to another drive) may break Vite.
- A default import of a CJS module returns the `module.exports` object, not `module.exports.default` (errors like "foo is not a function"); see Rolldown's note on ambiguous default imports.
- Ad-blocker extensions can cause a white screen with no logged errors.

## Checked

2026-11-07. Re-read the Vite Troubleshooting guide (docs/guide/troubleshooting.md) in full. Confirmed the pre-bundled dependency cache key and npm link caveat with vite --force, the --profile workflow (p then q keys, .cpuprofile file names, speedscope, vite-plugin-inspect), the externalized-module warning, strict-mode errors and patch tools, Windows cross-drive links, the CJS default import note pointing to Rolldown, and the ad-blocker white screen. Nothing removed.

Method: documentation only; no commands were run.
