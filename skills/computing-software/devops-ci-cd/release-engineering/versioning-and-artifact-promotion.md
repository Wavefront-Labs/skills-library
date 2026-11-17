---
id: computing-software.devops-ci-cd.release-engineering.versioning-and-artifact-promotion
name: versioning-and-artifact-promotion
category: computing-software
field: devops-ci-cd
product: release-engineering
tags: [release-engineering, releases, semver, semantic-versioning, calver, conventional-commits, changelog, release-notes, semantic-release, release-please, changesets, git-tags, release-branches, trunk-based-development, release-train, hotfix, cherry-pick, feature-flags, artifact-promotion, build-once-deploy-many, container-registry, image-digest, immutable-artifacts]
level: practitioner
status: docs-checked
description: "Ship predictably: pick SemVer or CalVer, automate changelogs from commits, trunk-based release branches and hotfixes, feature flags, and promote one immutable artifact."
sources: ["https://semver.org/", "https://www.conventionalcommits.org/", "https://keepachangelog.com/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Release engineering — versions, changelogs and artifact promotion

**Goal:** any release can be traced from version → commit → artifact digest → where it
runs, and cutting a release is a boring, automated step.

## 1. Choose a versioning scheme deliberately
- **SemVer `MAJOR.MINOR.PATCH`** for anything others depend on (libraries, APIs, CLIs).
  MAJOR = breaking, MINOR = backward-compatible feature, PATCH = fix. In `0.y.z`, anything
  may break — don't stay on 0.x for years if people depend on you.
  Pre-releases: `2.0.0-rc.1` sorts *before* `2.0.0`.
- **CalVer** (`2026.10.1`, `24.04`) for apps and products released on a cadence where
  "breaking" isn't meaningful to users.
- **Deployed services** often need no human version at all: the commit SHA (and a build
  number) is the version. Don't invent SemVer for a web backend nobody imports.
- Tag releases in Git as annotated tags: `git tag -a v1.4.0 -m "v1.4.0" && git push origin v1.4.0`.
  Never move or reuse a published tag.

## 2. Automate the version bump and changelog
- Adopt **Conventional Commits** (`feat:`, `fix:`, a `!` after the type, or a `BREAKING CHANGE:` footer),
  enforced on PR titles if you squash-merge (e.g. commitlint or a PR-title check).
- Then let a tool compute the next version and write `CHANGELOG.md`:
  - Examples: release-please, semantic-release, changesets. Their release flows differ; read each tool's current docs.
- Changelogs are for humans: group by Added/Changed/Fixed/Removed (Keep a Changelog),
  call out breaking changes and migration steps at the top.

## 3. Branching that keeps releases calm
- **Trunk-based:** everyone merges small changes to `main` behind flags; `main` is always
  releasable. Cut `release/1.4` only if you must stabilise or support old versions.
- **Hotfixes:** fix on `main` first, then `git cherry-pick -x <sha>` onto the release
  branch (`-x` records the origin). Fixing only on the release branch is how regressions
  "come back" in the next release.
- **Release trains:** a fixed cadence (e.g. every two weeks) where whatever is merged and
  green ships; late features wait for the next train instead of delaying it.

## 4. Feature flags separate deploy from release
- Deploy code dark, then turn it on per environment, percentage or cohort (a flag service or a config table).
- Every flag has an owner and an expiry; delete the flag and the dead branch of code
  once fully rolled out. Stale flags are a top source of untested combinations.
- Kill switches (long-lived ops flags) are a separate, documented category.

## 5. Build once, promote the same artifact
- CI builds one artifact per commit and stores it immutably: container image pushed by
  digest (`registry/app@sha256:...`), packages in Artifactory/Nexus/GitHub Packages.
- Promotion to staging → production changes **only configuration and pointers**
  (re-tag, copy between repositories, or update the digest in the deploy config), never
  rebuilds. Tools: `crane copy`/`crane tag`, `skopeo copy`, `docker buildx imagetools create`,
  registry promotion features.
- Deploy by digest, not by mutable tag (`:latest`, `:prod`): a tag can be pushed over;
  a digest can't.
- Attach metadata to the artifact: commit SHA, build URL, version (OCI labels such as
  `org.opencontainers.image.revision`), and sign it (see the secrets-management skill
  `computing-software.devops-ci-cd.secrets-management.secrets-and-supply-chain-hygiene`).

## 6. Release checklist (automate as much as possible)
Version computed → changelog updated → tag created → artifact built once, signed and
published → promoted through environments with checks → release notes published →
rollback target (previous digest/version) recorded.

## Verify
- [ ] Given a production pod/binary you can name its version, commit and build in one step.
- [ ] Staging and production run the same image digest for the same release.
- [ ] Next version and changelog are generated from commits with no manual editing of numbers.
- [ ] Every hotfix exists on `main` (cherry-picked with `-x`).
- [ ] Each feature flag has an owner and removal date.

## Checked

2026-10-28. Confirmed: semver.org (MAJOR.MINOR.PATCH, 0.y.z initial development, pre-release identifiers such as `2.0.0-rc.1`), Conventional Commits spec (`feat`, `fix`, `!` and `BREAKING CHANGE:` footer), Keep a Changelog (CHANGELOG.md, Added/Changed/Deprecated/Removed/Fixed/Security), git-cherry-pick `-x`, `docker buildx imagetools create`, and the OCI annotation `org.opencontainers.image.revision`. Removed: per-tool release-please, semantic-release and changesets behaviour, the named feature-flag vendors, and the old Unconfirmed section.

Method: documentation only; no commands were run.
