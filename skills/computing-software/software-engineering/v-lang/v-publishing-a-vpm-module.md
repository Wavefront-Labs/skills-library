---
id: computing-software.software-engineering.v-lang.v-publishing-a-vpm-module
name: v-publishing-a-vpm-module
category: computing-software
field: software-engineering
product: v-lang
tags: [v-publishing-a-vpm-module, vpm-packages, publish module, vpm publish, v.mod, release, git tag, semantic versioning, library authoring, v-lang]
level: practitioner
status: draft
description: "Prepare v.mod, README, tests and a git repo, then register the module on vpm.vlang.io and release versions with tags."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Publishing a module to VPM

Goal: release a reusable library.

1. `v new --lib mylib` or hand-create the dir with `v.mod` (name, description, version, license, dependencies).
2. Make the public API small: `pub` only what you mean, doc comments on every pub symbol, `README.md` with a usage example.
3. Add `*_test.v` tests and CI: `v fmt -verify .`, `v vet .`, `v test .` on Linux/macOS/Windows.
4. Push to GitHub/GitLab and tag releases `v0.1.0` following semver.
5. Register: sign in at https://vpm.vlang.io/ with your Git hosting account and submit the repository URL (confirm current flow); VPM indexes `v.mod`.
6. Choose a licence (MIT is common) and add a CHANGELOG.

Gotchas:
- V is pre-1.0: state the minimum V version/commit you test against.
- Renaming the module breaks dependants; use a new major version.

Verify: from a clean machine `v install author.mylib` and import it.
