---
id: computing-software.devops-ci-cd.nx.nx-release-independent
name: nx-release-independent
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, nx-release, independent, releasetag, changelog, projects-filter]
level: practitioner
status: docs-checked
description: "Configure nx release independent versioning: per-project prompts and git tags, releaseTag.pattern (Nx 22+ vs releaseTagPattern), project changelogs and the --projects filter."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/guides/Nx%20Release/release-projects-independently.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: version and publish projects on separate schedules.

Enable: `{ "release": { "projectsRelationship": "independent" } }` in `nx.json` (or per group, see nx-release-groups).

What changes versus fixed releases:
- A version bump prompt per released project.
- One git tag per project, default pattern `{projectName}@{version}` (e.g. `pkg-1@1.1.0`). Customise with `release.releaseTag.pattern` (Nx 22+) or `release.releaseTagPattern` (Nx < 22) and keep `{projectName}` in it for uniqueness:

```json
{ "release": { "releaseTag": { "pattern": "release/{projectName}/{version}" } } }
```
Nx < 22: `{ "release": { "releaseTagPattern": "release/{projectName}/{version}" } }`.
- Still a single commit, message listing every project, e.g. `chore(release): publish` then `- project: pkg-1 1.1.0` lines.
- No workspace-level `CHANGELOG.md`. Enable per-project changelogs: `{ "release": { "changelog": { "projectChangelogs": true } } }`.

Filter with `--projects` (same specifiers as `nx run-many`: names, tags, directories, globs, `!` negation):

```shell
nx release --projects=pkg-1,pkg-2
nx release --projects=server/*
nx release --projects='!ui/*'
```
Only matching projects are versioned, get changelogs, and are published.

Dependents of an independently versioned project are handled by `version.updateDependents` (see nx-release-update-dependents).

## Checked

2026-11-07. Confirmed against Release Projects Independently: projectsRelationship independent, per-project prompts, one tag per project with default {projectName}@{version}, releaseTag.pattern (Nx 22+) versus releaseTagPattern (Nx < 22) with the release/{projectName}/{version} example, the single release commit message, no workspace CHANGELOG.md, projectChangelogs true, the --projects filter examples and the updateDependents pointer. Removed: the invented dry-run Verify step.

Method: documentation only; no commands were run.
