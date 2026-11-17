---
id: computing-software.software-engineering.pnpm.catalogs-workspace-and-local-entries
name: catalogs-workspace-and-local-entries
category: computing-software
field: software-engineering
product: pnpm
tags: [catalog-workspace-range, catalog-file-protocol, catalog-link-protocol, catalog-save, catalog-publish, catalog-mode]
level: advanced
status: docs-checked
description: "Use workspace:, file: and link: entries in catalogs (v12.2.0 and v12.6.0), add deps with --save-catalog, and how catalog: is replaced on publish."
sources:
  - https://pnpm.io/catalogs
  - https://pnpm.io/cli/update
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Workspace range in a catalog (v12.2.0):

```yaml
catalog:
  '@example/utils': workspace:^
```

A dependency `"@example/utils": "catalog:"` expands to `workspace:^` and links the project. On publish it ships as the real version (e.g. `"^1.4.0"` when the package is at 1.4.0).

Local entries (v12.6.0): `file:` and `link:` are allowed; relative paths are measured from the directory holding `pnpm-workspace.yaml`.

```yaml
catalog:
  my-lib: link:./packages/my-lib
  my-tarball: file:./tarballs/foo.tgz
```

Adding: `pnpm add --save-catalog <pkg>` writes the range to the default catalog and `catalog:` to `package.json`; `--save-catalog-name <name>` targets a named catalog. The `catalogMode` setting controls whether `pnpm add` uses the default catalog without the flag (see the settings reference).

Publishing: `pnpm publish` / `pnpm pack` replace `catalog:` (like `workspace:`), so `"react": "catalog:react18"` becomes `"^18.3.1"` and consumers on any package manager can use it.

Updating: `pnpm update` edits the catalog entry, not `package.json` (see `computing-software.software-engineering.pnpm.update-dependencies`).

## Checked

2026-11-04. Confirmed against pnpm.io/catalogs and pnpm.io/cli/update: workspace: range entries (v12.2.0), file:/link: entries (v12.6.0), --save-catalog(-name), catalogMode, publish and pack replacement, and that pnpm update edits the catalog entry. Removed: the generic closing Check line (not stated on the page).
Method: documentation only; no commands were run.
