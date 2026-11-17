---
id: computing-software.devops-ci-cd.nx.nx-module-boundaries
name: nx-module-boundaries
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, module-boundaries, tags, depconstraints, eslint, oxlint, conformance]
level: practitioner
status: docs-checked
description: "Enforce Nx architecture rules with project tags and depConstraints in ESLint, Oxlint or Conformance; tag formats: exact, glob, regex, wildcard."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/features/enforce-module-boundaries.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stop projects importing from places your architecture forbids.

1. Tag projects. `project.json`: `"tags": ["scope:client"]`. `package.json`: `"nx": { "tags": ["scope:client"] }`.

2. Pick an enforcer (all share the tag model):

ESLint (JS/TS), after `nx add @nx/eslint-plugin @nx/devkit`; flat config rule:
```js
'@nx/enforce-module-boundaries': ['error', {
  allow: [],
  depConstraints: [
    { sourceTag: 'scope:shared', onlyDependOnLibsWithTags: ['scope:shared'] },
    { sourceTag: 'scope:admin',  onlyDependOnLibsWithTags: ['scope:shared', 'scope:admin'] },
    { sourceTag: 'scope:client', onlyDependOnLibsWithTags: ['scope:shared', 'scope:client'] }
  ]
}]
```
Legacy `.eslintrc.json`: same rule inside the `overrides` block for `*.ts,*.tsx,*.js,*.jsx`.

Oxlint (experimental; JS plugin API not covered by Oxlint semver): `nx add @nx/oxlint`, then in `.oxlintrc.json` set `"jsPlugins": ["@nx/oxlint/boundaries-plugin"]` and the same `@nx/enforce-module-boundaries` rule entry.

Conformance (any language, Enterprise): `nx add @nx/conformance`, then in `nx.json`:
```json
{ "conformance": { "rules": [ { "rule": "@nx/conformance/enforce-project-boundaries",
  "options": { "depConstraints": [
    { "sourceTag": "scope:client", "onlyDependOnProjectsWithTags": ["scope:shared", "scope:client"] } ] } } ] } }
```
Note the key is `onlyDependOnProjectsWithTags` here, not `...LibsWithTags`. CI: `npx nx conformance:check`.

Semantics: an untagged project may depend on nothing unless a `*` constraint allows it.

Tag formats in `sourceTag` and the allowed lists:
- `*` allows all (including untagged): `{ "sourceTag": "*", "onlyDependOnLibsWithTags": ["*"] }`
- exact string: `"scope:util"`
- regex, wrapped in slashes: `"/^scope.*/"`
- glob, only basic `*`: `"scope:*"`; use regex for anything fancier.

A violation lint error reads like: a project tagged "scope:admin" can only depend on projects tagged "scope:shared" or "scope:admin".

## Checked

2026-11-07. Confirmed: depConstraints, tag matching and the enforce-module-boundaries setup against the Enforce module boundaries page. Removed: an invented Verify step. Thin: one overview page.

Method: documentation only; no commands were run.
