---
id: computing-software.cybersecurity-defensive.application-security.dependency-pinning-and-lockfiles
name: dependency-pinning-and-lockfiles
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [supply-chain-security, dependency-pinning, lockfiles, hash-pinning, action-pinning, reproducible-builds]
level: practitioner
status: docs-checked
description: "Pin dependencies with committed lockfiles, pip hash-checking and commit-SHA-pinned GitHub Actions, then keep them fresh with automated updates."
sources: ["https://raw.githubusercontent.com/ossf/scorecard/main/docs/checks.md", "https://pip.pypa.io/en/stable/topics/secure-installs/", "https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dependency pinning and lockfiles

**Goal:** builds use exactly the dependency content you reviewed, and updates arrive deliberately.

## What "pinned" means (OpenSSF Scorecard)
A pinned dependency is set explicitly to a specific hash instead of a mutable version or range. The Pinned-Dependencies
check (risk Medium, GitHub-hosted repositories only) looks for unpinned dependencies in Dockerfiles, shell scripts and
GitHub workflows used in build and release. Go modules count full semantic versions as pinned because the Go tool
verifies downloads against hashes; a GitHub Actions `uses:` tag counts as pinned when backed by an immutable release.
Benefits: checking and deployment use the same software (reproducibility), a later compromised release does not
reach you automatically, and it helps counter dependency confusion.

Remediation from Scorecard:
- For an application, declare all dependencies with specific versions in the package format file (`package.json`,
  `requirements.txt`, `packages.config`); check in lock files such as `package-lock.json`, which hold signatures for
  the whole dependency tree. For C/C++, check in trusted source with a README of the version and archive SHA hashes.
- Use dependency update tools to keep pinned dependencies fresh. Pinning can inhibit updates (including security
  fixes), so notify on outdated dependencies and update quickly.

## Python: pip hash-checking mode
- By default pip does no checks against remote tampering. Use `--require-hashes` (or put `--hash=sha256:...` per
  requirement) and `--only-binary :all:` to disallow source distributions.
- Hash-checking is all or nothing: hashes are required for all requirements and all dependencies, and requirements
  must be pinned (`==`, URL or path). `--require-hashes` also helps bootstrap hashes, since it prints them; `pip
  hash` computes them.
- Recommended algorithm is sha256; md5, sha1 and sha224 are excluded. Several hashes per package support multiple
  platforms. Hashes from the PyPI download URL fragment do not satisfy the local-hash requirement.
- Do not install your project with `python setup.py install` or `develop`; use `python -m pip install --no-deps .`.

## GitHub Actions
- A compromised action can reach all repository secrets and may write to the repository with `GITHUB_TOKEN`.
- GitHub says a workflow dependency lockfile is the strongest protection and supersedes SHA pinning where adopted.
- Otherwise pin to a full-length commit SHA (verify it comes from the action's repository, not a fork). A tag is
  acceptable only if you trust the creator, and even then tags can be moved or deleted.
- Dependabot can keep action references up to date; it creates alerts only for actions using semantic versioning, not
  those pinned to SHAs.

## Gotchas
Pinned but never updated is a backlog of vulnerabilities; pin and automate updates together.

## Verify
The Scorecard Pinned-Dependencies check passes; pip installs fail on a hash mismatch; workflows reference SHAs.

## Checked
Method: docs-checked 2026-11-09 against the OpenSSF Scorecard checks page (Pinned-Dependencies), the pip "Secure
installs" page (read in full) and GitHub's "Security hardening for GitHub Actions" (third-party actions section).
Removed unconfirmed claims: npm ci, Go and Gradle/Maven commands, Docker digest pinning, the 2025 incident, Renovate
settings such as minimumReleaseAge, and the Renovate and pip-tools/uv commands.
