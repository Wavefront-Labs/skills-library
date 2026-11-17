---
id: computing-software.software-engineering.deno.workspaces-catalog-and-npm-compat
name: workspaces-catalog-and-npm-compat
category: computing-software
field: software-engineering
product: deno
tags: [workspaces, catalog, catalogs, workspace-protocol, pnpm, npm-workspaces]
level: sme
status: docs-checked
description: "Pin one npm version across a Deno workspace with catalog: and named catalogs, plus workspace: protocol and npm/pnpm workspace compatibility."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/fundamentals/workspaces.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`catalog:` (Deno 2.8; usable in a member deno.json `imports` since 2.9) lets the root declare one version and members reference it by name.

```jsonc title="deno.json"
{
  "workspace": ["./packages/a", "./packages/b"],
  "catalog": { "react": "^18.3.0", "chalk": "^5.3.0" }
}
```
```json title="packages/a/package.json"
{ "dependencies": { "react": "catalog:" } }
```

Named catalogs use `catalogs`, selected with `catalog:react19`; `catalog:` equals `catalog:default`.

```jsonc
{ "catalogs": { "react18": { "react": "^18.3.0" }, "react19": { "react": "^19.0.0" } } }
```

Rules: npm-only (an entry always resolves to `npm:`; manage `jsr:` through `imports`); root-only (defining in a member gives a diagnostic); a missing name is a resolution error. Catalogs may live in the root `package.json`, which wins entirely over deno.json when both define them.

Workspace protocol in package.json: `"another-workspace-package": "workspace:*"` (also `workspace:~`, `workspace:^`).

npm `"workspaces": ["packages/*"]` works as is. A `pnpm-workspace.yaml` must become `{ "workspace": ["packages/*"] }` in deno.json.

## Checked

2026-11-04: confirmed against the Deno docs Workspaces and monorepos page: catalog versions (2.8, imports since 2.9), named catalogs and default equivalence, restrictions, package.json catalogs winning, workspace protocol specifiers, npm and pnpm compatibility.

Method: documentation only; no commands were run.
