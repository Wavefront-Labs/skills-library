---
id: computing-software.software-engineering.pnpm.build-and-script-settings
name: build-and-script-settings
category: computing-software
field: software-engineering
product: pnpm
tags: [side-effects-cache, remote-cache, child-concurrency, verify-deps-before-run, node-options-setting, unsafe-perm, ignore-scripts-setting, side-effects-cache-exclude]
level: advanced
status: docs-checked
description: "Configure pnpm builds: ignoreScripts, childConcurrency, sideEffectsCache with remote and exclude, remoteCache trust, verifyDepsBeforeRun, nodeOptions, unsafePerm."
sources:
  - https://pnpm.io/settings/build
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
- `ignoreScripts` (false): skip scripts of the project and dependencies; does not stop `.pnpmfile.mjs`.
- `childConcurrency` (5): max build processes; zero or negative is subtracted from available parallelism, minimum 1.
- `sideEffectsCache` (true): caches the result of pre/post install hooks in the store. Object form: `read`, `write`, `remote`, `exclude`. Disable when scripts change files outside the package directory. `sideEffectsCacheReadonly` is the older spelling of `read: true, write: false`. Since v12.2.0 `--no-side-effects-cache` toggles only the local cache.
- `sideEffectsCache.exclude` (v12.14.0): packages never restored or saved, e.g. `- '@native/*'`, `- 'sharp@1.0.0 || 2.0.0'`.
- `sideEffectsCache.remote` (v12.0.0, proof of concept): reuse signed builds across machines. A package must also pass `allowBuilds`. Any cache failure falls back to a local build.
- `remoteCache` (v12.12.0): `org` may live anywhere; `url`, `team`, `trustedKeys`, `publish`, `privateKey`, `keyId`, `builderId` belong in global config or environment (`PNPM_REMOTE_CACHE_<FIELD>`). Setting them in `pnpm-workspace.yaml` fails with `ERR_PNPM_WORKSPACE_REMOTE_CACHE_TRUST`. Credentials need HTTPS or loopback.
- `verifyDepsBeforeRun` (default `install`): `warn`, `prompt`, `error`, `false` for `pnpm run` and `exec`. Filtered commands also cover dependent projects.
- `nodeOptions`: sets `NODE_OPTIONS` for scripts, e.g. `"${NODE_OPTIONS:- } --experimental-vm-modules"`.
- `unsafePerm` (false as root, else true): when false, scripts get `TMPDIR` in `node_modules/.tmp`.

## Checked

2026-11-04. Confirmed against pnpm.io/settings/build: defaults and semantics of ignoreScripts, childConcurrency, sideEffectsCache (object form, remote, exclude, v12.2.0 flag behaviour), remoteCache trust fields and error code, verifyDepsBeforeRun, nodeOptions, unsafePerm. Removed: the generic closing Check line (not stated on the page).
Method: documentation only; no commands were run.
