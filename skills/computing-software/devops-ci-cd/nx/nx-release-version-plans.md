---
id: computing-software.devops-ci-cd.nx.nx-release-version-plans
name: nx-release-version-plans
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, nx-release, version-plans, changesets, semver, ci]
level: practitioner
status: docs-checked
description: "Use nx release version plans (file-based versioning): enable, write .nx/version-plans files, nx release plan, plan:check in CI and ignorePatternsForPlanCheck."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/guides/Nx%20Release/file-based-versioning-version-plans.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: record desired bumps in committed files (like Changesets/Beachball) when commit messages cannot be enforced.

Enable in `nx.json` (bool, or per release group): `{ "release": { "versionPlans": true } }`.

Plan files live in `.nx/version-plans/*.md` and must be tracked by git (ignore only `.nx/workspace-data` and `.nx/cache`, not all of `.nx`). Front matter maps project or group names to bumps; the markdown body becomes the changelog entry:

```md
---
my-app: minor
my-lib: patch
release-group-a: major
---

One change that affects multiple projects and release groups.
```

With a single fixed version for everything, use `__default__: minor`. Unknown names make the release error. File names only need to be unique.

Create interactively: `nx release plan`. Apply: just run `nx release` (or the programmatic API); plans are the source of truth for bumps, applied plans are deleted, and the deleted file is staged and committed with the release (depending on your release config). Filtering with `--projects`/`--groups` applies only plans for the released projects; other plans stay but are still validated (an invalid one blocks the release). A plan touching projects both inside and outside the filter fails; split such files.

CI gate: `nx release plan:check` fails (non-zero) when touched projects (directly changed, not affected) lack a plan. It accepts `nx affected` style options (`--base`, `--head`, `--files`, `--uncommitted`), so set SHAs first, e.g. GitHub `uses: nrwl/nx-set-shas@v5`, CircleCI step `nx/set-shas`. Add `--verbose` to see changed-file detection.

Ignore files from the check (gitignore semantics, so `["*", "!src/"]` does NOT work):

```jsonc
{ "release": { "versionPlans": { "ignorePatternsForPlanCheck": ["**/*.spec.ts"] } } }
```

Working: `["**/*.ts", "!**/src/**"]`.

## Checked

2026-11-07. Confirmed against File Based Versioning (Version Plans): release.versionPlans true and per-group setting, the .nx/version-plans directory and git-tracking advice, front matter mapping of project or group names to bumps, the multi-project example, __default__ for a single version, error on unknown names, unique file names, nx release plan, plans deleted after being applied, --projects/--groups filtering rules, plan:check behaviour (touched not affected, non-zero exit), nx-set-shas@v5 and nx/set-shas, ignorePatternsForPlanCheck with gitignore semantics and the working and non-working patterns, and --verbose. Removed: the invented Verify step and the unqualified claim that the deletion is always committed.

Method: documentation only; no commands were run.
