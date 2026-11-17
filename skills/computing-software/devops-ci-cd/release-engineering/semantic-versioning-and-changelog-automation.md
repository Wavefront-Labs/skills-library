---
id: computing-software.devops-ci-cd.release-engineering.semantic-versioning-and-changelog-automation
name: semantic-versioning-and-changelog-automation
category: computing-software
field: devops-ci-cd
product: release-engineering
tags: [release-engineering, semver, semantic-versioning, breaking-change, conventional-commits, commitlint, pr-title-lint, squash-merge, changelog, changelog-automation, release-notes, release-please, pre-release, release-candidate, version-bump, git-tags, monorepo-versioning]
level: practitioner
status: docs-checked
description: "Make version numbers mean something and changelogs write themselves: SemVer rules and edge cases, Conventional Commits enforcement, and release-please configuration."
sources: ["https://semver.org/", "https://www.conventionalcommits.org/en/v1.0.0/", "https://github.com/googleapis/release-please"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Semantic versioning and changelog automation

**Goal:** the next version number is computed, not argued about; it is *correct* (a
breaking change never ships as a minor); and every release has human-readable notes
produced without anyone hand-editing a file.

(The choice of SemVer vs CalVer and artifact promotion are in
`computing-software.devops-ci-cd.release-engineering.versioning-and-artifact-promotion`.)

## 1. SemVer rules that cause real breakage
- Versions are `MAJOR.MINOR.PATCH`, non-negative integers, no leading zeroes, each increasing numerically (1.9.0 -> 1.10.0).
- Major zero (`0.y.z`) is initial development: anything may change and the API is not stable.
- Minor must be incremented for new backward-compatible functionality and also when public API is marked deprecated.
  Remove deprecated API only in the next major.
- "Breaking" means a consumer who changes nothing gets a failure. Commonly missed: changing defaults, error types or
  the shape of a returned object; tightening accepted input; raising the minimum runtime version. SemVer does not rule on
  the runtime case, so write a policy in CONTRIBUTING and apply it consistently.
- Pre-1.0 behaviour differs per tool: release-please bumps minor for breaking changes before 1.0.0 only with
  `bump-minor-pre-major: true`. Make the behaviour explicit in config.

## 2. Make commits machine-readable
Conventional Commits: `type(scope)!: description`, with an optional footer `BREAKING CHANGE: <description>`.
- `fix` correlates with PATCH, `feat` with MINOR, and a `!` before the colon or a `BREAKING CHANGE:` footer (any type) with MAJOR.
- Other types (`docs`, `chore`, `ci`, `refactor`, `perf`, `test`, `build`, `style` from the commitlint config) have no implicit
  SemVer effect unless they carry a breaking change.
- If `!` is used, the footer may be omitted and the description is used to describe the break.
- **Squash-merge repos:** only the PR title lands on main, so lint the title, not each commit.
- Merge-commit repos: run commitlint in a commit-msg hook and in CI over the branch's commits.
- Teach the footer: a `!` without a migration note produces a useless changelog entry.

## 3. release-please
A bot keeps a release PR open that updates the version and changelog; merging it creates the release. For monorepos use
`release-please-config.json` (package settings) plus `.release-please-manifest.json` (current versions). Default strategy:
breaking changes bump major, features minor, fixes patch. Do not run two release automation tools on one repo.

## 4. Pre-releases
- Precedence from the spec: `1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-beta < 1.0.0-beta.2 < 1.0.0-beta.11 < 1.0.0-rc.1 < 1.0.0`.
  Dot-separated numeric identifiers compare numerically, so use `rc.1`, `rc.10` rather than `rc1`, `rc10`.
- Publish pre-releases on a separate channel or tag so default installs never pick them up.

## 5. Changelog quality
- Generated notes are a first draft; review the release PR body before merging.
- Order: breaking changes with migration steps, then features, then fixes.
- Revert commits can be awkward in generated notes; read the output.
- One consistent tag format; never re-point a tag.

## Verify
- [ ] Next version and notes are produced by CI with no human typing a number.
- [ ] A PR titled `feat!: ...` without a migration note is flagged in review or lint.
- [ ] The runtime-version-bump policy is written down.

## Checked
2026-11-01. Confirmed on semver.org (version form, major zero, deprecation increments minor, pre-release precedence example),
the Conventional Commits 1.0.0 spec (types, `!`, footer, SemVer mapping, commitlint types) and the release-please manifest and
customizing docs (config file names, `bump-minor-pre-major`, default strategy). Removed unconfirmed claims: tool comparison
for semantic-release, changesets and git-cliff, API-diff tool list, squash-merge lint action names, `perf` as patch.
Method: documentation only; no commands were run.
