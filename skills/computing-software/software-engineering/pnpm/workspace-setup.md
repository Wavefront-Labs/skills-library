---
id: computing-software.software-engineering.pnpm.workspace-setup
name: workspace-setup
category: computing-software
field: software-engineering
product: pnpm
tags: [pnpm-workspaces, pnpm-workspace-yaml, monorepo, workspace-packages, workspaces-field, cyclic-workspace-dependencies]
level: intro
status: docs-checked
description: "Declare a pnpm workspace: pnpm-workspace.yaml packages globs, auto-conversion from the workspaces field (v12.7.0), root dependency checks, cycles and release tooling."
sources:
  - https://pnpm.io/workspaces
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A workspace needs `pnpm-workspace.yaml` in its root:

```yaml
packages:
  - packages/*
```

Conversion (v12.7.0): if a repo lists projects in the root `package.json` `workspaces` field and has no `pnpm-workspace.yaml`, `pnpm install` creates one with the same patterns and links the projects in that install. An existing file is never changed; nothing is created with `--ignore-workspace`. If the `workspaces` field later differs, pnpm warns, since only `pnpm-workspace.yaml` is read.

Other facts:
- Adding a dependency to the root fails unless you pass `-w` / `--ignore-workspace-root-check`, or set `ignoreWorkspaceRootCheck: true`.
- Cycles: scripts cannot be topologically ordered when workspace dependencies cycle. pnpm warns "There are cyclic workspace dependencies"; inspect `dependencies`, `optionalDependencies`, `devDependencies`. `disallowWorkspaceCycles: true` fails install; `ignoreWorkspaceCycles: true` silences warnings.
- Versioning/release: `pnpm change` and `pnpm version -r`, or external changesets and Rush.
- `failIfNoMatch: true` makes a filter that matches nothing exit non-zero.
- `includeWorkspaceRoot: true` includes the root in recursive commands.

Check: `pnpm install` links every listed project.

## Checked
2026-11-08. Read in full: pnpm Workspace page (docs/workspaces.md in the pnpm.io repo, same content as pnpm.io/workspaces). Confirmed: pnpm-workspace.yaml packages, v12.7.0 workspaces-field conversion rules, cycle warning text and settings, ignoreWorkspaceRootCheck, failIfNoMatch, includeWorkspaceRoot, release tooling. Nothing removed.
Method: documentation only; no commands were run.
