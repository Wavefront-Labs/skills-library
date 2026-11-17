---
id: computing-software.devops-ci-cd.nx.nx-module-boundary-tag-dimensions
name: nx-module-boundary-tag-dimensions
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, module-boundaries, tags, depconstraints, allsourcetags, eslint]
level: practitioner
status: docs-checked
description: "Layer scope and type tags and write onlyDependOnLibsWithTags depConstraints, including allSourceTags to combine several source tags in one Nx boundary rule."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/guides/Enforce%20Module%20Boundaries/tag-multiple-dimensions.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: constrain dependencies on more than one axis (e.g. `scope` and `type`) with `@nx/enforce-module-boundaries`.

Tag each project with one tag per dimension in `project.json`:

```json
{ "tags": ["scope:client", "type:app"] }
```
Typical set: `scope:client|admin|shared`, `type:app|feature|ui|util`. An e2e project can carry the same tags as its app plus `"implicitDependencies": ["client"]`.

Rules for the type dimension: app depends on feature, ui, util (not other apps); feature on ui, util; ui on ui, util; util only on util. Express them as `depConstraints` (same shape in ESLint flat config, legacy `.eslintrc.json`, and `.oxlintrc.json`):

```javascript
depConstraints: [
  { sourceTag: 'scope:shared', onlyDependOnLibsWithTags: ['scope:shared'] },
  { sourceTag: 'scope:admin',  onlyDependOnLibsWithTags: ['scope:shared', 'scope:admin'] },
  { sourceTag: 'scope:client', onlyDependOnLibsWithTags: ['scope:shared', 'scope:client'] },
  { sourceTag: 'type:app',     onlyDependOnLibsWithTags: ['type:feature', 'type:ui', 'type:util'] },
  { sourceTag: 'type:feature', onlyDependOnLibsWithTags: ['type:ui', 'type:util'] },
  { sourceTag: 'type:ui',      onlyDependOnLibsWithTags: ['type:ui', 'type:util'] },
  { sourceTag: 'type:util',    onlyDependOnLibsWithTags: ['type:util'] },
]
```
Combine tags with `allSourceTags`: every tag in the array must be present for the constraint to apply, avoiding ad-hoc one-off tags:

```javascript
{ allSourceTags: ['scope:admin', 'type:ui'], onlyDependOnLibsWithTags: ['type:util'], bannedExternalImports: ['*router*'] }
```

Warning: the guide says constraint complexity rises exponentially with more tags; draw a diagram and plan the boundaries first.

Related: nx-ban-external-imports, nx-module-boundary-ban-tags-and-allow.

## Checked

2026-11-07. Confirmed: multi-dimension tagging and constraint examples against the Tag multiple dimensions page. Removed: an unconfirmed "must satisfy every constraint" sentence, wording on growth (now the page's "exponentially"), and an invented Verify step.

Method: documentation only; no commands were run.
