---
id: computing-software.software-engineering.v-lang.v-awesome-v-and-ecosystem
name: v-awesome-v-and-ecosystem
category: computing-software
field: software-engineering
product: v-lang
tags: [v-awesome-v-and-ecosystem, ecosystem-learning-and-stability, awesome v, ecosystem, v-analyzer, vsql, libraries, projects, vpm, community, frameworks, v-lang]
level: practitioner
status: draft
description: "Survey the V ecosystem via Awesome V and VPM: web, GUI, game, database, editor tooling, notable projects and maturity expectations."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Awesome V and ecosystem survey

Goal: choose libraries wisely.

- Awesome V (github.com/vlang/awesome-v) lists libraries and apps by category; VPM lists installable modules with stars/updated dates.
- Core in-tree: `veb` (web), `gg` (graphics), `orm`, `db.*`, `json`, `net`, `cli`, `toml`. Separate repos: `ui` (GUI), `v-analyzer` (LSP), `vsql`, `vpkg`-style tools.
- Evaluate a dependency: recent commits, tests in CI, V version compatibility, issue activity, number of dependants.
- Prefer in-tree vlib modules where possible; they track compiler changes.
- For missing functionality wrap a C library (C interop is first-class) or call out via HTTP/CLI.
- Show-and-tell: V's own tools (compiler, `v doc`, vweb sites) are written in V; Vinix OS and Volt (confirm current names) are larger projects.

Gotchas:
- Abandoned packages are common; vendor critical ones.
- Star counts do not equal production readiness.

Verify: shortlist 3 candidates for a need and read their tests.
