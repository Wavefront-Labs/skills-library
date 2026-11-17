---
id: computing-software.devops-ci-cd.release-engineering.api-compatibility-diff-for-semver
name: api-compatibility-diff-for-semver
category: computing-software
field: devops-ci-cd
product: release-engineering
tags: [release-engineering, cargo-semver-checks, api-diff, semver, breaking-changes, ci-gate]
level: practitioner
status: draft
description: "Gate releases on automated API diffs so the version bump matches the change: cargo-semver-checks, japicmp, apidiff, api-extractor and griffe."
sources: ["https://semver.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# API diff tools for semantic versioning

**Goal:** CI fails when a change breaks the public API without a major bump.

## Tools by ecosystem
| Ecosystem | Tool | Typical call |
|---|---|---|
| Rust | cargo-semver-checks | `cargo semver-checks` (check against the last published version); `--baseline-rev <git-rev>` |
| Java | japicmp (Maven/Gradle plugin) | compare against the previous release artifact |
| Go | `golang.org/x/exp/cmd/apidiff` | export API of two versions then diff |
| TypeScript | api-extractor | commit the `.api.md` report; CI diff fails on change |
| Python | griffe | `griffe check <package> --against <ref>` |
Flag names change between versions; read each tool's help.

## Pipeline pattern
1. Resolve the baseline: the latest release tag or published version.
2. Run the tool on the PR; a breaking result requires the PR to carry a `BREAKING CHANGE` footer / major bump.
3. Fail the job on breaks unless a label `semver-major` is present.
4. After release, update the baseline automatically (the tag moves).

## Gotchas
- Tools only see the declared public surface; behavioural changes need tests and human judgment.
- Pre-1.0 versions have looser rules; decide and document your policy.
- Private/internal packages must be excluded explicitly.

## Verify
Intentionally remove a public function in a test branch; the gate fails with a message naming it.
