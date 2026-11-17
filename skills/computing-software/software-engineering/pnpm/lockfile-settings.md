---
id: computing-software.software-engineering.pnpm.lockfile-settings
name: lockfile-settings
category: computing-software
field: software-engineering
product: pnpm
tags: [lockfile-setting, lockfile-dir, exclude-links-from-lockfile, lockfile-include-tarball-url, symlinked-lockfile, include-resolution-settings, peers-suffix-max-length, lockfile-config-mismatch]
level: advanced
status: docs-checked
description: "Configure pnpm-lock.yaml: lockfile, lockfileDir, frozenLockfile defaults, excludeLinksFromLockfile, tarball URLs, symlinked lockfiles, includeResolutionSettings."
sources:
  - https://pnpm.io/settings/store
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
- `lockfile` (true): `false` neither reads nor writes `pnpm-lock.yaml`.
- `lockfileDir`: where the lockfile lives; default is the workspace root with a shared lockfile, else the project. `--lockfile-dir` for one command, not with `--global`.
- `frozenLockfile`: default false, but true in CI when a lockfile exists; fails if the lockfile needs updating or is missing. `preferFrozenLockfile` (true) does a headless install when the lockfile satisfies `package.json`.
- `excludeLinksFromLockfile`: leave `link:` dependencies out; `workspace:` ones stay.
- `lockfileIncludeTarballUrl`: add the full tarball URL to every entry.
- `symlinkedLockfileTargetDirs` (v12.16.0): when `pnpm-lock.yaml` is a symlink, pnpm writes through it only if the target lies in a listed directory (absolute or `~/`). Global config or `PNPM_CONFIG_SYMLINKED_LOCKFILE_TARGET_DIRS='["/path/to/src"]'` only; ignored in the workspace file.
- `lockfile.includeResolutionSettings` (v12.10.0): records `autoDedupe`, `dedupeInjectedDeps`, `dedupePeerDependents`, `linkWorkspacePackages` in the lockfile `settings`, so a mismatch re-resolves and `--frozen-lockfile` fails with `ERR_PNPM_LOCKFILE_CONFIG_MISMATCH`. Enable only when everyone is on v12.10.0 or later. Needs local resolution, so a non-frozen install fails with `pnprServer`.
- `peersSuffixMaxLength` (1000): longer peer-ID suffixes in dependency keys become hashes.

Related: `computing-software.software-engineering.pnpm.lockfile-integrity-and-revisions` covers `integrityTarget`, and `...git-branch-lockfiles` the branch settings.

## Checked

2026-11-04. Confirmed against pnpm.io/settings/store: lockfile, lockfileDir, frozenLockfile, preferFrozenLockfile, excludeLinksFromLockfile, lockfileIncludeTarballUrl, symlinkedLockfileTargetDirs (v12.16.0), lockfile.includeResolutionSettings (v12.10.0) and its error code, peersSuffixMaxLength. Removed: the generic closing Check line (a frozen-lockfile pass claim not on the page).
Method: documentation only; no commands were run.
