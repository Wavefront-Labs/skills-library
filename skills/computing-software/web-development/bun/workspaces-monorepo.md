---
id: computing-software.web-development.bun.workspaces-monorepo
name: workspaces-monorepo
category: computing-software
field: web-development
product: bun
tags: [bun-workspaces, workspace-protocol, negative-globs, self-contained-workspace]
level: practitioner
status: docs-checked
description: "Set up Bun workspaces: globs and exclusions, the workspace: protocol and how publish rewrites it, self-contained workspaces, and unnamed-package pitfalls."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/pm/workspaces.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```json
{
  "name": "my-project",
  "workspaces": ["packages/**", "!packages/**/test/**"],
  "devDependencies": { "example-package-in-monorepo": "workspace:*" }
}
```

Self-contained workspaces (root form, or `installConfig` in the workspace itself):

```json
{ "workspaces": { "packages": ["apps/*", "packages/*"], "selfContained": ["apps/desktop"] } }
```
```json
{ "name": "desktop", "installConfig": { "hoistingLimits": "workspaces" } }
```

Publish rewrites: `workspace:*` becomes the current version (`1.0.1`), `workspace:^` becomes `^1.0.1`, `workspace:~` becomes `~1.0.1`, an explicit version wins, a path reference publishes the directory's version.

Rules and gotchas:
- A workspace needs a `name`; unnamed matches are skipped (not linked, deps not installed) and warn if they declare dependencies.
- Shared dependencies are hoisted to the root `node_modules`; workspaces are linked, not fetched.
- A workspace may live outside the root (`../shared`).
- Self-contained mode copies deps as real files and has no effect with the isolated linker; the lockfile does not record it.
- Use catalogs to share versions.

## Checked

2026-11-04. Confirmed against bun docs pm/workspaces.mdx: workspaces globs and negative patterns, workspace: protocol and publish rewrites, unnamed-package skipping and warning, workspaces outside the root, hoisting, self-contained workspaces (selfContained and installConfig.hoistingLimits), isolated-linker no-op, lockfile not recording the setting, catalogs.

Method: documentation only; no commands were run.
