---
id: computing-software.devops-ci-cd.nx.nx-module-boundary-ban-tags-and-allow
name: nx-module-boundary-ban-tags-and-allow
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, module-boundaries, notdependonlibswithtags, allow, tags, eslint]
level: practitioner
status: docs-checked
description: "Use notDependOnLibsWithTags to ban tagged dependencies through the whole tree, and the allow property to except specific imports from Nx module boundary rules."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/guides/Enforce%20Module%20Boundaries/ban-dependencies-with-tags.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/guides/Enforce%20Module%20Boundaries/tags-allow-list.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: two escape/inversion tools for `@nx/enforce-module-boundaries` constraints.

1. Ban instead of allow-list. A long `onlyDependOnLibsWithTags` list can be inverted with `notDependOnLibsWithTags`:

```jsonc
{ "sourceTag": "scope:client", "notDependOnLibsWithTags": ["scope:admin"] }
```
Any tag except `scope:admin` is accepted. Unlike `onlyDependOnLibsWithTags`, the ban follows the entire dependency tree, so a transitive dependency on a banned tag is also reported. Combine both on one constraint:

```jsonc
{
  "sourceTag": "type:react",
  "onlyDependOnLibsWithTags": ["type:react", "type:utils", "type:animation", "type:model"],
  "notDependOnLibsWithTags": ["type:angular"]
}
```
This keeps angular code from reaching react projects even indirectly.

2. Exceptions with `allow`. To deliberately break a tag rule for specific imports, the guide says each project can set an `allow` property in its project configuration, with import-path patterns:
- `'@myorg/mylib/testing'` allows importing exactly that path.
- `'@myorg/mylib/*'` allows `@myorg/mylib/a` but not `@myorg/mylib/a/b`.
- `'@myorg/mylib/**'` allows `a` and `a/b`.
- `'@myorg/**/testing'` allows `@myorg/mylib/testing` and `@myorg/nested/lib/testing`.

The lint rule examples also show an `allow: []` option beside `depConstraints`; the guide does not describe that option, so this skill makes no claim about it.

Related: nx-module-boundary-tag-dimensions.

## Checked

2026-11-07. Confirmed: notDependOnLibsWithTags and the allow guidance against the Ban dependencies with tags and Tags allow list pages. Removed: an invented Verify step, a version-dependent hedge, and a rule-level allow claim (the guide describes allow as a per-project property).

Method: documentation only; no commands were run.
