---
id: computing-software.software-engineering.pnpm.save-and-misc-settings
name: save-and-misc-settings
category: computing-software
field: software-engineering
product: pnpm
tags: [save-prefix, save-exact-setting, tag-setting, extend-node-path, optimistic-repeat-install, required-scripts, embed-readme, dedupe-direct-deps, macos-backup, update-notifier]
level: practitioner
status: docs-checked
description: "Use pnpm miscellaneous settings: savePrefix, saveExact, tag, extendNodePath and NODE_PATH, optimisticRepeatInstall, requiredScripts, dedupeDirectDeps, embedReadme, ci."
sources:
  - https://pnpm.io/settings/other
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
- `savePrefix` (`^`; also `~`, empty, `=`): `=` saves `=1.2.3` and `pnpm update` keeps it. Ignored when you give a range (`pnpm add foo@2`). `saveExact` saves no operator. `saveTypes` (v12.6.0) also saves available `@types/*` to `devDependencies`. `tag` (latest) is the dist-tag used when no version is given.
- `extendNodePath` (true): command shims in `node_modules/.bin` set `NODE_PATH` to the package's own dependencies directory and the hoisted `.pnpm/node_modules`, so tools using `import-local` (jest, eslint) resolve from the working directory. Essential with the global virtual store. Disable only if no tool resolves from the CWD and no global virtual store is used.
- `optimisticRepeatInstall` (true): fast content check of manifests, lockfile and patches; if nothing changed the install, including project `prepare` scripts, is skipped. Set false to run scripts each time.
- `requiredScripts`: scripts that every project selected by `pnpm -r run <script>` must have, else the run fails.
- `dedupeDirectDeps` (false): skip symlinking into subprojects what already sits in the workspace root `node_modules`.
- `embedReadme`, `deployAllFiles` (copy everything even with a `files` field), `preferSymlinkedExecutables` (POSIX, hoisted linker), `ignoreCompatibilityDb` (disable automatic patches from `@yarnpkg/extensions`), `useStderr`, `updateNotifier` (daily check, skipped in CI and offline).
- `ci`: true when CI detected: `frozenLockfile` defaults true with a lockfile, reporter is `append-only`, no update check. Ignored in project workspace files.
- `macosBackup.excludeModulesDir` / `excludeStoreDir` (v12.6.0, global config): mark directories for Time Machine exclusion.

## Checked

2026-11-04. Confirmed savePrefix, saveExact, saveTypes (v12.6.0), tag, extendNodePath, optimisticRepeatInstall, requiredScripts, dedupeDirectDeps, embedReadme, deployAllFiles, preferSymlinkedExecutables, ignoreCompatibilityDb, useStderr, updateNotifier, ci and macosBackup against pnpm.io/settings/other. Removed the unsourced closing Check line.

Method: documentation only; no commands were run.
