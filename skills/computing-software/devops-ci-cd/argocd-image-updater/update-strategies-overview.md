---
id: computing-software.devops-ci-cd.argocd-image-updater.update-strategies-overview
name: update-strategies-overview
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, update-strategy, semver, newest-build, digest, alphabetical, calver, mutable-tags]
level: intro
status: docs-checked
description: "Pick one of five update strategies (semver, newest-build, digest, alphabetical, calver), set it globally or per image, avoid the old aliases."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/basics/update-strategies.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/configuration/images.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Update strategies overview

A strategy defines how new versions are found. Set `updateStrategy` in `commonUpdateSettings` at three levels; image beats application beats global:

- `spec.commonUpdateSettings`
- `spec.applicationRefs[].commonUpdateSettings`
- `spec.applicationRefs[].images[].commonUpdateSettings`

| Strategy | Picks |
|---|---|
| `semver` (default) | highest allowed semantic version |
| `newest-build` | most recently created image (alias `latest`, deprecated) |
| `digest` | newest push of one mutable tag |
| `alphabetical` | last tag in a lexical sort (alias `name`, deprecated) |
| `calver` | newest calendar version tag |

The old names still work but produce a warning in the controller logs and may be removed. If no strategy is given or the value is invalid, `semver` is used.

Mutable versus immutable: every strategy except `digest` assumes tags are immutable and new images get new tags. To follow a mutable tag such as `latest`, use `digest`.

The version constraint in `imageName` (`some/image:<constraint>`) only matters for `semver`, `digest` (the tag to watch) and `calver` (the tag layout). For other strategies all registry tags are candidates; narrow them with `allowTags` and `ignoreTags`.

Multi-arch `platforms` only has effect for strategies that fetch metadata: newest-build and digest.

## Checked

2026-11-08. Read in full: docs/basics/update-strategies.md, docs/configuration/images.md and docs/index.md. Confirmed the five strategies and deprecated aliases, the three configuration levels and precedence, the semver fallback for missing or invalid values, the mutable tag rule, the version-constraint note and the platforms note. Nothing removed.

Method: documentation only; no commands were run.
