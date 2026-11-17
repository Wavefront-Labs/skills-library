---
id: computing-software.devops-ci-cd.nx.nx-release-version-changelog-git
name: nx-release-version-changelog-git
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, nx-release, changelog, conventional-commits, versioning, git]
level: advanced
status: docs-checked
description: "Tune nx release versioning, changelogs and git: conventionalCommits, updateDependents, preid, zero-major bumps, workspace and project changelog, createRelease, git commit/tag."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/reference/nx-json.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/features/manage-releases.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: configure the version, changelog and git phases of `nx release` in `nx.json`.

Version (core options are top level since Nx 21; ecosystem options go in `versionActionsOptions`; default implementation `@nx/js/src/release/version-actions`):
```jsonc
{ "release": { "version": {
  "conventionalCommits": true,
  "manifestRootsToUpdate": ["dist/packages/{projectName}"],
  "versionActionsOptions": { "skipLockFileUpdate": true }
} } }
```
Defaults that changed:
- Nx 22: `preserveMatchingDependencyRanges` defaults true (a dependent's `^1.0.0` stays when releasing 1.2.0; set false for exact versions). `updateDependents` defaults `"always"` (others: `"auto"` only within selected projects/groups, `"never"`). Legacy versioning removed; run `nx migrate` to convert config.
- Nx 23: `adjustSemverBumpsForZeroMajorVersion` defaults true (on 0.x, breaking bumps minor, features bump patch); set false for old behaviour.
- `--preid` bumps to dependents are stable patches by default (dependent of a `2.0.1-rc.0` project goes to `1.0.1`); `version.applyPreidToDependents: true` (also per group) propagates the preid.

Changelog (workspace changelog does not apply to independent releases):
```jsonc
{ "release": { "changelog": {
  "workspaceChangelog": { "createRelease": "github", "file": false },
  "projectChangelogs": true
} } }
```
- `workspaceChangelog: false` disables it. `projectChangelogs: true` uses defaults, or an object with `createRelease: "github"` and `file: false` (no CHANGELOG.md files, one GitHub release per project).
- New entries are prepended; `replaceExistingContents: true` (Nx 22+, on either changelog) rewrites the whole file.

Git:
```jsonc
{ "release": { "git": { "commit": true, "tag": false } } }
```
`commit` commits version/changelog changes; `tag` creates one tag per release, or per project when independent.

## Checked

2026-11-07. Confirmed against the nx.json reference (Version, Changelog and Git sections): versionActionsOptions and the @nx/js version-actions default, manifestRootsToUpdate, the Nx 22 and Nx 23 default changes (preserveMatchingDependencyRanges, updateDependents, adjustSemverBumpsForZeroMajorVersion, legacy versioning removal, strictPreid), applyPreidToDependents and its per-group form, workspaceChangelog false and the createRelease github plus file false objects, projectChangelogs true, replaceExistingContents (Nx 22+) for both changelogs, and git commit and tag. Removed: the invented dry-run Verify step.

Method: documentation only; no commands were run.
