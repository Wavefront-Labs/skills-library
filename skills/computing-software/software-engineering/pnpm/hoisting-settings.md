---
id: computing-software.software-engineering.pnpm.hoisting-settings
name: hoisting-settings
category: computing-software
field: software-engineering
product: pnpm
tags: [hoist, hoist-pattern, public-hoist-pattern, hoist-workspace-packages, shamefully-hoist-setting, hoisting-limits, external-dependencies, phantom-dependencies]
level: practitioner
status: docs-checked
description: "Control pnpm hoisting: hoistPattern, publicHoistPattern, hoistWorkspacePackages, shamefullyHoist, hoistingLimits for the hoisted linker, externalDependencies, negation."
sources:
  - https://pnpm.io/settings/node-modules
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```yaml
hoistPattern:
  - "*eslint*"
  - "*types*"
  - "!@types/react"
publicHoistPattern:
  - "*plugin*"
```

- `hoist` (true): hoist all dependencies to `node_modules/.pnpm/node_modules`, so unlisted dependencies are reachable by packages inside `node_modules`.
- `hoistPattern` (default `['*']`): which packages go there. Narrow it to just the packages with phantom dependencies (recommended). `!` excludes.
- `publicHoistPattern` (default `[]`): hoist matches to the root `node_modules`, so application code sees them too. Use for flawed pluggable tools.
- `shamefullyHoist: true` equals `publicHoistPattern: ['*']`.
- `hoistWorkspacePackages` (true): workspace projects are candidates, matched by `package.json` name. `publicHoistPattern` is checked first. A same-named direct dependency wins; the root project is never hoisted. If both patterns are empty (or `hoist: false`), nothing is hoisted. Example: `publicHoistPattern: ["*eslint*"]` exposes a workspace `eslint-plugin-acme` at the root.
- `hoistingLimits` (with `nodeLinker: hoisted`): `none` (default), `workspaces`, `dependencies`; mirrors Yarn's `nmHoistingLimits`.
- `externalDependencies`: with the hoisted linker, names left for another tool to link at the top level.

## Checked

2026-11-04. Confirmed against pnpm.io/settings/node-modules: hoist, hoistPattern, publicHoistPattern, shamefullyHoist, hoistWorkspacePackages rules and eslint-plugin example, hoistingLimits values, externalDependencies. Removed: the generic closing Check line (not stated on the page).
Method: documentation only; no commands were run.
