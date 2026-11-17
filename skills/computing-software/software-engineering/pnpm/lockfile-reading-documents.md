---
id: computing-software.software-engineering.pnpm.lockfile-reading-documents
name: lockfile-reading-documents
category: computing-software
field: software-engineering
product: pnpm
tags: [pnpm-lock-yaml, boot-document, multi-document-yaml, config-dependencies-lockfile, lockfile-version, scanner-pitfall]
level: sme
status: docs-checked
description: "Parse pnpm-lock.yaml correctly: one or two YAML documents, boot document versus project lockfile, which to read for graphs versus scanners, and the silent-pass scanner trap."
sources:
  - https://pnpm.io/lockfile
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`pnpm-lock.yaml` is one or two YAML documents:
- Boot document (first, when present): `configDependencies` and `packageManagerDependencies` plus their `packages` and `snapshots`.
- Project lockfile (last, always): `importers`, `packages`, `snapshots`.

Both carry the same `lockfileVersion` (schema of entries, not document count). A file starting with `---` has a boot document. It is written when the project has config dependencies, or pnpm records its resolved version (when `devEngines.packageManager` is declared or pnpm 12+ is pinned via `packageManager`; `pmOnFail: ignore` turns it off). It is also called the env document (`ERR_PNPM_ENV_LOCKFILE_CORRUPTED`) and sits first so commands read a few kilobytes to decide the pnpm version.

Use a multi-document loader:

```js
import { loadAll } from 'js-yaml'
const last = loadAll(text).at(-1)           // project dependency graph
const all = loadAll(text)                   // scanners/SBOM: read every document
```

Do not merge documents: both use the `.` importer key. Config dependencies appear only in the boot document.

Trap: a single-document reader returns the boot document, an importer with no `dependencies`, so a scanner reports "no vulnerabilities" and the CI gate passes. Test scanners on a two-document lockfile. `pnpm audit` handles both shapes.

A frozen install fails with `ERR_PNPM_FROZEN_LOCKFILE_WITH_OUTDATED_LOCKFILE` if the pinned pnpm version is stale.

## Checked

2026-11-04. Confirmed against pnpm.io/lockfile: boot and project documents, shared lockfileVersion, when the boot document is written, env document error code, multi-document loading, no-merge rule, single-document scanner trap, frozen-install error code. Removed: the generic closing Check line (not stated on the page).
Method: documentation only; no commands were run.
