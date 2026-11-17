---
id: computing-software.software-engineering.zig.zig-version-management
name: zig-version-management
category: computing-software
field: software-engineering
product: zig
tags: [zig, zig-version-management, zig-cli-tooling, zigup, zvm, minimum-zig-version, setup-zig, nightly-builds]
level: practitioner
status: docs-checked
description: "Install Zig from the official downloads, choose release versus master builds, and set up CI with the setup-zig action."
sources:
  - https://ziglang.org/download/
  - https://github.com/mlugg/setup-zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Installing and pinning Zig versions
**Goal:** reproducible toolchains despite pre-1.0 churn.

- Official downloads: `ziglang.org/download/` lists the latest stable release and a "Bleeding Edge Development Version (master branch)". Tarballs and zips per platform, each with a `.minisig` signature made with minisign (the public key is on the page). Release notes are linked per release (`.../download/<version>/release-notes.html`); read them on every upgrade.
- Community version managers exist (zigup, zvm); check their own READMEs for flags, which this skill does not cover.
- GitHub Actions: `mlugg/setup-zig@v2` installs Zig to `PATH` and preserves the Zig cache across runs. The `version` input accepts a release (`0.13.0`), a specific nightly, `master` (latest nightly), `latest` (latest full release) or a Mach nominated version. If left empty it resolves the version from `minimum_zig_version` in `build.zig.zon`, falling back to `latest`.
- setup-zig verifies the tarball's minisign signature, tries community mirrors in random order and the official site last. Old nightlies may be purged from mirrors, so targeting a stale nightly can fail.
- Cache controls: `use-cache: false` disables caching; `cache-key` should include matrix variables (runner platform is already included); the cache is cleared above 2 GiB by default, changed with `cache-size-limit` (MiB; `0` disables the limit). On GitHub Actions use `mlugg/setup-zig@v2`; the codeberg URL form is for Forgejo Actions.
- Pin per project by setting `minimum_zig_version` in `build.zig.zon` and an explicit `version:` in CI when you need an exact toolchain.

## Self-check
Download one release and one master build into separate directories and show `zig version` for each through explicit paths.

## Checked

2026-11-08. Read: setup-zig README in full; ziglang.org/download page (releases, master section, minisign key, release-notes links) via search of the served HTML, not every line.
Removed: unverified release-cadence statements, package-manager lag claim, "single self-contained directory" claim, zigup/zvm behaviour, zig.guide source (not read).
Method: documentation only; no commands were run.
