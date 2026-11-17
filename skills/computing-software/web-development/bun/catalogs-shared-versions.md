---
id: computing-software.web-development.bun.catalogs-shared-versions
name: catalogs-shared-versions
category: computing-software
field: web-development
product: bun
tags: [catalogs, catalog-protocol, monorepo-versions, workspaces-catalog]
level: practitioner
status: docs-checked
description: "Share dependency versions across a monorepo with default and named catalogs, the catalog: protocol, bun add --catalog, and what happens at publish time."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/pm/catalogs.mdx
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/pm/cli/add.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Root `package.json`:

```json
"workspaces": {
  "packages": ["packages/*"],
  "catalog": { "react": "^19.0.0", "react-dom": "^19.0.0" },
  "catalogs": { "testing": { "jest": "30.0.0" } }
}
```

Workspace package: `"react": "catalog:"`, `"jest": "catalog:testing"`.

- `catalog` (singular) is the default; `catalog:default` equals `catalog:`.
- Update by changing the root catalog, then `bun install`.
- `bun add react --catalog` / `--catalog=testing` (use `=`, not a space) adds to the catalog and writes the reference. Passing a version (`react@19 --catalog`) replaces the catalog entry for every package using it.
- `catalog:` works in dependencies, devDependencies, optionalDependencies, peerDependencies and as an `overrides` value.

Gotchas:
- A package in both `catalog` and `catalogs.default` is an error; unknown references fail to resolve.
- `catalog:` is valid only in the root and workspace `package.json` files. `bun publish` and `bun pm pack` replace it with the real range.

## Checked

2026-11-04. Confirmed against bun docs pm/catalogs.mdx and pm/cli/add.mdx: catalog and catalogs fields, catalog:default, bun add --catalog rules, reference locations, default-catalog conflict, publish-time replacement.

Method: documentation only; no commands were run.
