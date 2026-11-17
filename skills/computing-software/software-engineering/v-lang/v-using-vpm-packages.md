---
id: computing-software.software-engineering.v-lang.v-using-vpm-packages
name: v-using-vpm-packages
category: computing-software
field: software-engineering
product: v-lang
tags: [v-using-vpm-packages, vpm-packages, vpm, packages, v install, vpm.vlang.io, dependencies, third party modules, awesome v, v-lang]
level: intro
status: draft
description: "Search vpm.vlang.io, install author.module packages, import them, pin versions via git tags and handle conflicts."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Finding and using packages from VPM

Goal: reuse community modules.

- Find: browse https://vpm.vlang.io/ or `v search json`; the Awesome V list (github.com/vlang/awesome-v) curates libraries by category.
- Install: `v install ui` or namespaced `v install author.name`; import by the installed path: `import author.name` (or just `import name` for top-level VPM names; confirm per package page).
- Version pinning: V lacks lock files; install from git with a tag: `v install --git https://github.com/org/repo` then `git -C ~/.vmodules/org/repo checkout v1.2.0` (confirm the module directory).
- Record dependencies in `v.mod` `dependencies: [...]` so teammates run `v install`.
- Inspect modules before use: read source, check last update and issues; V libraries vary in maturity.

Gotchas:
- Updating `v` itself can break third-party modules; pin your V version in CI.
- Packages may need C dependencies installed.

Verify: `v list` shows it and a sample import compiles.
