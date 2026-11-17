---
id: computing-software.software-engineering.pnpm.filter-directory-and-changed
name: filter-directory-and-changed
category: computing-software
field: software-engineering
product: pnpm
tags: [filter-directory, filter-since, changed-packages, merge-base, test-pattern, changed-files-ignore-pattern, legacy-dir-filtering]
level: advanced
status: docs-checked
description: "Filter workspaces by directory glob and git changes: ./glob and {glob} selectors, [since] merge-base behaviour, --test-pattern, --changed-files-ignore-pattern, legacyDirFiltering."
sources:
  - https://pnpm.io/filtering
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Directory selectors, relative to the working directory:

```sh
pnpm --filter "./packages/**" <cmd>
pnpm --filter "{packages/**}[origin/master]..." <cmd>
pnpm --filter "@babel/*{components/**}" <cmd>
```

`*` and `?` match within a path segment, `**` crosses segments, `[ab]` is a class; none match a name starting with a dot (`packages/*` skips `packages/.cache`). `{packages/*}` selects one level only; `legacyDirFiltering: true` restores matching every project in the subtree. pnpm-generated workspace-root selectors are always globs.

Changed since: `--filter "[origin/master]"`, prefixed or suffixed with `...` for dependents or dependencies: `pnpm --filter "...[origin/master]" test`.
- Since v12.7.0 the comparison is against the merge base with `<since>`; uncommitted changes are included. In a shallow clone without the merge base, pnpm compares against `<since>` directly.
- Requires Git 2.24 or newer.
- A project also counts as changed when a catalog version it uses changes in `pnpm-workspace.yaml`, or when files were moved out of it (rename detection).

`--test-pattern="test/*"` (setting `testPattern`): changes only in tests do not pull in dependents. `--changed-files-ignore-pattern="**/README.md"` (setting `changedFilesIgnorePattern`) ignores matching changed files.

## Checked

2026-11-04. Confirmed against pnpm.io/filtering: directory selectors and glob rules, dot-prefixed names, legacyDirFiltering, generated workspace-root selectors, [since] selector with v12.7.0 merge-base behaviour, Git 2.24 requirement, catalog and rename cases, test-pattern, changed-files-ignore-pattern. Removed: the generic closing Check line (not stated on the page).
Method: documentation only; no commands were run.
