---
id: computing-software.devops-ci-cd.nx.nx-release-update-dependents
name: nx-release-update-dependents
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, nx-release, updatedependents, preid, prerelease, dependencies]
level: advanced
status: docs-checked
description: "Configure whether nx release bumps dependents when a dependency is versioned: updateDependents always/auto/never and applyPreidToDependents for prereleases."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/guides/Nx%20Release/update-dependents.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: decide what happens to `project-a` when its dependency `project-b` is versioned independently.

Option `release.version.updateDependents`:
- `"always"` (default since v22): update dependents regardless of release group or `--projects`/`--groups` filters.
- `"auto"` (the old default): only dependents in the same release group and not filtered out.
- `"never"`: no automatic dependent updates.

When triggered, Nx rewrites the dependency reference in the manifest and bumps the dependent with a side-effectful patch: `project-b` 2.0.0 -> 2.1.0 makes `project-a` 1.0.0 -> 1.0.1 with `"project-b": "2.1.0"`.

Prereleases: by default side-effectful bumps stay stable. After

```shell
nx release version prepatch --preid rc --projects project-b
```

project-b becomes `2.0.1-rc.0` but project-a becomes plain `1.0.1`. To propagate the preid:

```json
{ "release": { "version": { "updateDependents": "always", "applyPreidToDependents": true } } }
```

Now project-a becomes `1.0.1-rc.0`. Enable it when packages release as a set and one `--preid rc` run should yield a consistent prerelease; leave it off when a stable dependent on an rc dependency is intentional. It can be scoped per group via `release.groups.<group>.version.applyPreidToDependents`.

See nx-release-groups for group boundaries.

## Checked

2026-11-07. Confirmed against Update Dependents: updateDependents values always (default since v22), auto (old default) and never, the side-effectful patch bump example (2.0.0 to 2.1.0 gives 1.0.0 to 1.0.1), prepatch with --preid rc leaving the dependent at 1.0.1, applyPreidToDependents giving 1.0.1-rc.0, guidance on when to enable it, and the per-group setting. Removed: the invented dry-run Verify step.

Method: documentation only; no commands were run.
