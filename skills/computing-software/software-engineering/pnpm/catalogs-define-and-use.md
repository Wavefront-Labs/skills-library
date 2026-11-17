---
id: computing-software.software-engineering.pnpm.catalogs-define-and-use
name: catalogs-define-and-use
category: computing-software
field: software-engineering
product: pnpm
tags: [catalogs, catalog-protocol, default-catalog, named-catalogs, catalog-shorthand, shared-versions]
level: practitioner
status: docs-checked
description: "Define version ranges once in pnpm-workspace.yaml (catalog, catalogs) and reference them with catalog: or catalog:name in package.json and overrides; know the benefits and errors."
sources:
  - https://pnpm.io/catalogs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```yaml
# pnpm-workspace.yaml
catalog:                # the default catalog
  react: ^18.3.1
catalogs:               # named catalogs
  react17: { react: ^17.0.2 }
```

```json
{ "dependencies": { "react": "catalog:", "other": "catalog:react17" } }
```

- `catalog:` is shorthand for `catalog:default`. The default can also be written `catalogs.default`; defining both fails with "The 'default' catalog was defined multiple times".
- Usable in `dependencies`, `devDependencies`, `peerDependencies`, `optionalDependencies`, `overrides` in `pnpm-workspace.yaml`, and `pnx` specifiers (`pnx shx@catalog:`).
- Benefits: one version per dependency, a one-line upgrade, fewer `package.json` merge conflicts.
- A default plus named catalogs suits piecemeal migration.
- Migrate an existing workspace with the codemod: `pnx codemod pnpm/catalog`.

Errors: `ERR_PNPM_CATALOG_ENTRY_NOT_FOUND_FOR_SPEC` (no entry for the dependency) and `ERR_PNPM_CATALOG_ENTRY_INVALID_RECURSIVE_DEFINITION` (an entry is itself a `catalog:` reference).

## Checked

2026-11-04. Confirmed against pnpm.io/catalogs: default and named catalogs, catalog: shorthand, duplicate-default error, usable fields, advantages, codemod, both error codes. Removed: the generic closing Check line (not stated on the page).
Method: documentation only; no commands were run.
