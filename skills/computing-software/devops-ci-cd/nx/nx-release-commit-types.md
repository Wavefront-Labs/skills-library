---
id: computing-software.devops-ci-cd.nx.nx-release-commit-types
name: nx-release-commit-types
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, nx-release, conventional-commits, changelog, semverbump, versioning]
level: practitioner
status: docs-checked
description: "Customise how conventional commit types map to semver bumps and changelog sections in nx release: disable, retitle, hide, add custom and __INVALID__ types."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/guides/Nx%20Release/customize-conventional-commit-types.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: tune `release.conventionalCommits.types` in `nx.json`. Defaults: `feat` -> minor, `fix` -> patch, `BREAKING CHANGE` footer or `!` after the type (`fix(...)!`) -> major. No relevant commits means no release (works with independent releases). Companion to nx-release-conventional-commits.

Each entry under `types` takes `semverBump` and `changelog`:

- Disable a type entirely (versioning and changelog): `"docs": false`.
- Keep it in the changelog but not versioning: `"docs": { "semverBump": "none" }`.
- Change the bump: `"docs": { "semverBump": "patch" }`.
- Rename the changelog section: `"docs": { "changelog": { "title": "Documentation Changes" } }`.
- Hide from changelog: `"chore": { "changelog": false }` or `"chore": { "changelog": { "hidden": true } }`.
- Custom type: `"awesome": {}`. With no `semverBump` it defaults to `patch`.

```json
{ "release": { "conventionalCommits": { "types": {
  "docs": { "semverBump": "patch", "changelog": { "title": "Documentation Changes" } },
  "chore": { "changelog": false }
} } } }
```

Invalid commits: non-conforming messages (not `<type>: <message>`) are ignored by default. The special `__INVALID__` type processes them; its default `semverBump` is `none`:

```json
{ "release": { "conventionalCommits": { "types": {
  "__INVALID__": { "semverBump": "patch", "changelog": { "title": "Uncategorized changes" } }
} } } }
```

Caution: invalid is not the same as unmatched. A valid commit whose type is disabled is not caught by `__INVALID__`. If commits cannot follow the standard, consider version plans (nx-release-version-plans).

## Checked

2026-11-07. Confirmed against Customize Conventional Commit Types: default feat/fix/breaking bumps, skipped release when no relevant commits, false to disable a type, semverBump none and patch, changelog title, changelog false and hidden true, the awesome custom type defaulting to patch, __INVALID__ (default semverBump none) and the invalid-versus-unmatched caution, and the version-plans alternative. Removed: the invented dry-run Verify step.

Method: documentation only; no commands were run.
