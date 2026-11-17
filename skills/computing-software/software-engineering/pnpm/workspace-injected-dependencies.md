---
id: computing-software.software-engineering.pnpm.workspace-injected-dependencies
name: workspace-injected-dependencies
category: computing-software
field: software-engineering
product: pnpm
tags: [inject-workspace-packages, injected-dependencies, dedupe-injected-deps, sync-injected-deps-after-scripts, hard-link-workspace, shared-workspace-lockfile]
level: advanced
status: docs-checked
description: "Hard-link pnpm workspace deps instead of symlinking with injectWorkspacePackages, dependenciesMeta injected and dedupeInjectedDeps."
sources:
  - https://pnpm.io/workspaces
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Settings in `pnpm-workspace.yaml`:

- `injectWorkspacePackages` (default false): hard-link all local workspace dependencies instead of symlinking. Per dependency, use `dependenciesMeta[].injected` in `package.json`.
- `dedupeInjectedDeps` (default true): symlink an injected dependency whenever possible. If the dependent and the injected package reference the same peer dependencies, no physical copy is needed. Multiple graphs are used only when peers mismatch.
- `syncInjectedDepsAfterScripts` (list of script names): injected deps are hard-link collections that do not follow source changes, a problem for packages that must be built (e.g. TypeScript). After any listed script runs in a workspace package, pnpm resyncs the injected copies. While it runs, copies are refreshed as separate files so a watcher sees each write, which suits watch-mode builds.

```yaml
injectWorkspacePackages: true
syncInjectedDepsAfterScripts:
  - build
```

Lockfile: `sharedWorkspaceLockfile` (default true) creates one `pnpm-lock.yaml` at the root. Benefits: every dependency is a singleton, faster installs, fewer review changes. Each project still gets symlinks only for its declared dependencies.

Check: after a build in the source package, the injected copy contains the new files.

## Checked
2026-11-08. Read in full: pnpm Workspace page (docs/workspaces.md in the pnpm.io repo, same content as pnpm.io/workspaces). Confirmed: injectWorkspacePackages, dedupeInjectedDeps, syncInjectedDepsAfterScripts (including watch-mode note), sharedWorkspaceLockfile and its advantages. Nothing removed.
Method: documentation only; no commands were run.
