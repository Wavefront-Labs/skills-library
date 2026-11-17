---
id: computing-software.devops-ci-cd.nx.nx-release-groups
name: nx-release-groups
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, nx-release, release-groups, fixed, independent, monorepo]
level: advanced
status: docs-checked
description: "Define nx release groups with projects matchers, fixed vs independent projectsRelationship, per-group overrides, release tags, filters and processing order."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/guides/Nx%20Release/release-groups.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: release different project subsets with different rules from one workspace.

Without config there is an implicit `__default__` group of all releasable projects; top-level `release.projects` adjusts that group.

Define groups in `nx.json`:

```jsonc
{ "release": { "groups": {
  "backend":  { "projects": ["api", "auth-service"], "projectsRelationship": "fixed" },
  "frontend": { "projects": ["web-app", "mobile-app"], "projectsRelationship": "independent" }
} } }
```

`projects` matchers: names, globs (`packages/shared-*`), `tag:npm-public`, negation (`!ignore-me`). A project may belong to only one group (config validation errors otherwise).

`projectsRelationship`:
- `fixed` (default): one shared version; any bump versions the whole group; in-group dependencies always updated; each project gets a changelog entry.
- `independent`: each project versioned only when it has changes (or via `updateDependents`); changelog only for direct/indirect changes.

A group can override root `release` keys: `version` (e.g. `conventionalCommits`, `versionPrefix`, `updateDependents`, `groupPreVersionCommand`), `changelog` (`file`, `createRelease`, `renderer`), `releaseTag` (`pattern` such as `backend-{version}`, `requireSemver`), `versionPlans`, and docker settings.

Order: groups are processed topologically (dependencies before dependents), projects inside a group likewise; circular dependencies are tolerated but not recommended.

Filters:
```bash
nx release --groups=backend
nx release --projects=api,web-app
nx release --groups=frontend --dry-run
```
Gotcha: filtering a fixed group requires including every project in it.

Related: nx-release-update-dependents, nx-release-independent.

## Checked

2026-11-07. Confirmed against Release Groups: implicit __default__ group, group definition and project matchers, one group per project, fixed (default) and independent behaviour, per-group version, changelog, releaseTag, versionPlans and groupPreVersionCommand overrides, Docker configuration as a group option, topological processing, circular-dependency note, the --groups and --projects filters and the fixed-group filter caution. Removed: the invented dry-run Verify step.

Method: documentation only; no commands were run.
