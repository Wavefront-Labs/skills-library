---
id: computing-software.devops-ci-cd.nx.nx-release-conventional-commits
name: nx-release-conventional-commits
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, nx-release, conventional-commits, semver, versioning, ci]
level: practitioner
status: docs-checked
description: "Make nx release pick the semver bump from conventional commit messages instead of prompting, including per-project bumps and the useCommitScope option."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/guides/Nx%20Release/automatically-version-with-conventional-commits.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/guides/Nx%20Release/customize-conventional-commit-types.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let `nx release` derive the version bump from git history so it runs unattended in CI.

Enable it in `nx.json`:

```json
{ "release": { "version": { "conventionalCommits": true } } }
```

Bump rules: Nx reads commits since the last release and takes the highest bump: `feat` -> minor, `fix` -> patch (a breaking change gives major; see nx-release-commit-types). Example: history of `fix(pkg-1)`, `feat(pkg-2)`, `chore(pkg-3)`, `chore(release): 1.0.0` yields minor, so 1.1.0. If no relevant commits exist, the release is skipped.

Independent releases: the bump is computed per project. With `fix(pkg-1)`, `feat(pkg-2)`, `chore(pkg-3)`: pkg-1 gets patch, pkg-2 gets minor, pkg-3 is skipped ("No changes were detected").

Gotchas:
- Which projects a commit affects is decided by the files it changed, not by the commit scope. `feat(pkg-2)` that touched files in another project can bump that project.
- The scope does affect the size of the bump. By default `useCommitScope` is `true`: a commit only counts as feat/fix/breaking for a project when it has no scope or the scope equals the project name. Any other scope is treated as a `patch` for the projects it touched (e.g. `feat(button)` in project `ui`).
- To derive the bump purely from affected files, set it under `release.conventionalCommits`:

```json
{ "release": { "conventionalCommits": { "useCommitScope": false } } }
```

The CLI output shows "Resolved the specifier as "minor" using git history and the conventional commits standard" when it worked. For the current version it reads the git tag from `releaseTag.pattern` (e.g. `{projectName}@{version}`).

## Checked

2026-11-07. Confirmed against Automatically Version with Conventional Commits: the version.conventionalCommits flag, feat minor and fix patch, the 1.1.0 example, skipped release when nothing relevant, per-project independent bumps, files-not-scope project matching, useCommitScope default true and its patch treatment of other scopes, the false setting under release.conventionalCommits, and the sample CLI output. The major bump for breaking changes is confirmed on Customize Conventional Commit Types, added to sources. Removed: the invented dry-run Verify step and the unconfirmed remark that the option does not live under version.

Method: documentation only; no commands were run.
