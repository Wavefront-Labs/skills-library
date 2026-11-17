---
id: computing-software.software-engineering.pnpm.filter-exclusion-order
name: filter-exclusion-order
category: computing-software
field: software-engineering
product: pnpm
tags: [filter-exclude, negated-filter, filter-order, multiple-filters, zsh-escape]
level: practitioner
status: docs-checked
description: "Exclude packages with pnpm --filter '!sel', escape ! in zsh, and rely on v12.7.0 left-to-right evaluation so a later inclusion can restore an excluded project."
sources:
  - https://pnpm.io/filtering
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Any selector becomes an exclusion with a leading `!`. In zsh and possibly other shells, escape it: `\!`.

```sh
pnpm --filter=!foo <cmd>                 # everything except foo
pnpm --filter='!./lib/**' <cmd>          # everything outside lib
pnpm --filter "!./packages/**" --filter @scope/core <cmd>
```

Rules:
- When the first selector is an exclusion, filtering starts from every project in the workspace.
- Otherwise a project is taken if it matches at least one inclusion selector, unless a later exclusion removes it.
- Since v12.7.0, selectors are evaluated in the order given, so a later inclusion can bring back a project an earlier exclusion removed (the third example selects `@scope/core` even though it lives under `packages/`).

## Checked

2026-11-04. Confirmed against pnpm.io/filtering: leading ! exclusion and zsh escaping, three examples, first-selector-exclusion rule, inclusion/exclusion multiplicity, v12.7.0 ordering. Removed: the unsupported line about combining exclusions with relation operators (the page only says any selector may be negated) and the generic closing Check line.
Method: documentation only; no commands were run.
