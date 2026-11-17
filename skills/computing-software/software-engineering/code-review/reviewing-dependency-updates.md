---
id: computing-software.software-engineering.code-review.reviewing-dependency-updates
name: reviewing-dependency-updates
category: computing-software
field: software-engineering
product: code-review
tags: [code-review, specialised-review, dependency-review, dependabot, renovate, supply-chain-security, licence-compliance, lockfile-review, changelog]
level: practitioner
status: draft
description: "Review new dependencies and version bumps: necessity, maintenance health, licence, security posture, transitive impact, lockfile diffs and changelog breaking changes."
sources: ["https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/about-dependency-review", "https://securityscorecards.dev/", "https://docs.renovatebot.com/", "https://openssf.org/resources/guides/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reviewing dependency updates

**Goal:** every third-party package that enters or changes in the build is deliberate,
safe and legally usable.

## New dependency checklist
1. **Necessary?** Could the standard library or an existing dependency do it in a few
   lines? (left-pad lesson.)
2. **Health**: recent releases, responsive maintainers, more than one maintainer,
   downloads/usage, open security issues. OpenSSF Scorecard (`scorecard --repo=...`)
   gives a quick signal.
3. **Licence** compatible with your distribution model (GPL/AGPL in proprietary
   products, no-licence repos). Licence scanners: `licensee`, FOSSA, GitHub dependency review.
4. **Size and transitive tree**: how many packages does it pull in? (`npm ls`, `cargo tree`,
   `pipdeptree`, `go mod graph`)
5. **Name check**: typosquats and lookalikes (`reqeusts`), recently transferred packages.
6. **Install-time behaviour**: postinstall scripts, native builds, network access during build.

## Version bumps (Dependabot/Renovate PRs)
- Read the changelog/release notes between versions for breaking changes, deprecations
  and security fixes; Renovate includes them in the PR body.
- Major bumps: check migration guides; expect code changes.
- Lockfile diff: unexpected NEW transitive packages or registry URLs changing are red
  flags; large churn deserves a look.
- CI green is necessary, not sufficient: tests rarely cover every library behaviour you
  rely on.
- Security patches: fast-track, but still verify the fixed version is the one resolved.

## Process
- Enable GitHub dependency review action (`actions/dependency-review-action`) to fail PRs
  introducing known-vulnerable or disallowed-licence packages.
- Group low-risk updates (patch/minor dev dependencies) to reduce noise; keep runtime
  majors separate.
- CODEOWNERS for lockfiles/manifests so a platform/security owner sees new dependencies.

## Verify
- [ ] New dependency PRs state why it's needed and alternatives considered.
- [ ] Dependency review action blocks a test PR adding a package with a known CVE.
