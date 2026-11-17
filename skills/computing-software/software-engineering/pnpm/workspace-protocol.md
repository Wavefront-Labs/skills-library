---
id: computing-software.software-engineering.pnpm.workspace-protocol
name: workspace-protocol
category: computing-software
field: software-engineering
product: pnpm
tags: [workspace-protocol, workspace-alias, workspace-relative-path, link-workspace-packages, save-workspace-protocol, publish-conversion]
level: practitioner
status: docs-checked
description: "Use the workspace: protocol: refuse registry fallback, aliases and relative paths, publish-time rewriting to real versions, linkWorkspacePackages and saveWorkspaceProtocol."
sources:
  - https://pnpm.io/workspaces
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
With `linkWorkspacePackages` (default false) set to true, a workspace package is linked only if its version satisfies the range; otherwise pnpm uses the registry, which is uncertain. `workspace:` refuses anything but a local package: `"foo": "workspace:2.0.0"` fails if only another version exists. With `linkWorkspacePackages: false`, only `workspace:` links. `deep` links into subdependencies; `true` links only direct declarations.

Forms:
- `"foo": "workspace:*"`
- alias: `"bar": "workspace:foo@*"` (published as `"npm:foo@1.0.0"`)
- path: `"foo": "workspace:../foo"`

On `pnpm pack` / `publish`, with all packages at 1.5.0:

| Declared | Published |
|---|---|
| `workspace:*` (or bare `workspace:`) | `1.5.0` |
| `workspace:~` | `~1.5.0` |
| `workspace:^` | `^1.5.0` |
| `workspace:^1.5.0` | `^1.5.0` |

`saveWorkspaceProtocol` (default `rolling`) controls what `pnpm add foo` writes: `false` gives `1.0.0`-style specs, `true` gives `workspace:1.0.0`, `rolling` gives `workspace:*`, `workspace:~` or `workspace:^` per `savePrefix`.

`preferWorkspacePackages` prefers local over a newer registry version; only useful without `saveWorkspaceProtocol`.

Check: the packed `package.json` has no `workspace:` left.

## Checked
2026-11-08. Read in full: pnpm Workspace page (docs/workspaces.md in the pnpm.io repo, same content as pnpm.io/workspaces). Confirmed: workspace: refusing registry fallback, alias and relative-path forms, publish-time rewriting table, linkWorkspacePackages (default false, true/deep), saveWorkspaceProtocol table, preferWorkspacePackages. Nothing removed.
Method: documentation only; no commands were run.
