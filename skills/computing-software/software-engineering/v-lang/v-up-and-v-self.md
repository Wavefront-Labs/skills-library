---
id: computing-software.software-engineering.v-lang.v-up-and-v-self
name: v-up-and-v-self
category: computing-software
field: software-engineering
product: v-lang
tags: [v-up-and-v-self, v-cli-maintenance, v up, v self, upgrade v, update compiler, v symlink, wipe-cache, version, v-lang]
level: practitioner
status: draft
description: "Upgrade V to the latest master with v up, rebuild the compiler with v self, and manage versions, symlinks and caches."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Updating V with v up and rebuilding with v self

Goal: keep the toolchain current and reproducible.

- `v up` pulls the latest source (git) and rebuilds the compiler; `v up -v` is verbose. Offers no pinning: V releases are rolling (confirm weekly tag scheme `weekly.YYYY.WW`).
- `v self` rebuilds the compiler from the current source tree without pulling (useful after local edits to `cmd/` or vlib).
- `v symlink` adds `v` to your PATH (on Windows `v symlink` modifies PATH, may need admin).
- `v version` prints something like `V 0.4.x <hash>`; `v doctor` prints environment details for bug reports.
- Pin a version in CI: clone the vlang/v repo, `git checkout <tag or commit>`, `make` (or `make.bat`).
- `v wipe-cache` removes compiled module caches after upgrades.

Gotchas:
- A dirty git tree may block `v up`.
- After upgrading, run `v fmt -w .` to migrate syntax changes and fix newly deprecated APIs.

Verify: `v version` shows the new commit.
