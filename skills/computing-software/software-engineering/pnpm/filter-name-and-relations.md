---
id: computing-software.software-engineering.pnpm.filter-name-and-relations
name: filter-name-and-relations
category: computing-software
field: software-engineering
product: pnpm
tags: [pnpm-filter, filter-package-name, filter-dependencies, filter-dependents, ellipsis-selector, chevron-selector]
level: practitioner
status: docs-checked
description: "Select workspace packages with pnpm --filter: names and globs, foo... dependencies, ...foo dependents, ^ to exclude the package itself, and the scope-optional name rule."
sources:
  - https://pnpm.io/filtering
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`pnpm --filter <selector> <command>` (also `-F`).

| Selector | Selects |
|---|---|
| `"@babel/core"`, `"@babel/*"`, `"*core"` | exact name / patterns |
| `foo...` | foo and all its dependencies |
| `"foo^..."` | only foo's dependencies |
| `...foo` | foo and all its dependents |
| `"...^foo"` | only foo's dependents |
| `"@babel/preset-*..."` | pattern as roots |

```sh
pnpm --filter foo... test
pnpm --filter "...^foo" test
```

- Scope is optional: `--filter=core` picks `@babel/core` if `core` is not found. If several scopes have the same name (`@babel/core`, `@types/core`), unscoped filtering picks nothing.
- Quote selectors containing `^` or `*` for your shell.
- Multiple `--filter` flags union their matches: `pnpm --filter ...foo --filter bar --filter baz... test`.
- `--filter-prod` is the same as `--filter` but omits `devDependencies` when expanding to dependency projects.
- `--fail-if-no-match` (or `failIfNoMatch`) exits non-zero when nothing matched; `--no-fail-if-no-match` overrides the setting.

## Checked

2026-11-04. Confirmed against pnpm.io/filtering: selector table, scope-optional rule, multiple filters, --filter-prod, --fail-if-no-match and failIfNoMatch. Removed: the generic closing Check line (not stated on the page).
Method: documentation only; no commands were run.
