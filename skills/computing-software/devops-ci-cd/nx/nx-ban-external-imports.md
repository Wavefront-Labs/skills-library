---
id: computing-software.devops-ci-cd.nx.nx-ban-external-imports
name: nx-ban-external-imports
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, module-boundaries, eslint, oxlint, bannedexternalimports, allowedexternalimports]
level: practitioner
status: docs-checked
description: "Restrict which npm packages tagged Nx projects may import with bannedExternalImports and allowedExternalImports in @nx/enforce-module-boundaries depConstraints."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/guides/Enforce%20Module%20Boundaries/ban-external-imports.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/features/enforce-module-boundaries.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stop projects importing the wrong third-party package (e.g. NestJS `Injectable` in a frontend, Angular's in a backend, or React in util libs).

Only available in the `@nx/enforce-module-boundaries` lint rule (ESLint or Oxlint); the Conformance rule has no equivalent. Add entries to the rule's `depConstraints`, keyed by a project tag (`sourceTag`).

ESLint flat config (`eslint.config.mjs`):

```javascript
'@nx/enforce-module-boundaries': ['error', {
  allow: [],
  depConstraints: [
    { sourceTag: 'frontend', bannedExternalImports: ['@nestjs/common'] },
    { sourceTag: 'backend',  bannedExternalImports: ['@angular/core'] },
    { sourceTag: 'type:util', bannedExternalImports: ['*react*'] },
  ],
}]
```

The same rule object works in legacy `.eslintrc.json`, and in `.oxlintrc.json` under `rules` (the `@nx/oxlint/boundaries-plugin` must already be registered under `jsPlugins`).

Wildcards: `react*` matches `react`, `react-dom`, `react-native`; `*react*` matches any package with react in its name.

Allow-list approach (more restrictive): `allowedExternalImports`.

```javascript
{ sourceTag: 'type:util', allowedExternalImports: ['date-fns'] },
{ sourceTag: 'type:ui', allowedExternalImports: ['@angular/*'], bannedExternalImports: ['@angular/common/http'] },
{ sourceTag: 'type:core', allowedExternalImports: [] }, // no external packages at all
```

Both options can be combined in one constraint (allow a family, ban one member). Tag projects first (`tags` in `project.json`, or `nx.tags` in `package.json`).

## Checked

2026-11-07. Confirmed: bannedExternalImports usage and the depConstraints shape against the Ban external imports and Enforce module boundaries pages (latter added to sources). Removed: an invented nx lint Verify step; reworded the tagging step to the page's tags/nx.tags forms.

Method: documentation only; no commands were run.
