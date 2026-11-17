---
id: computing-software.software-engineering.v-lang.v-stability-caveats-and-version-pinning
name: v-stability-caveats-and-version-pinning
category: computing-software
field: software-engineering
product: v-lang
tags: [v-stability-caveats-and-version-pinning, ecosystem-learning-and-stability, stability, pre-1.0, breaking changes, weekly release, experimental, version pinning, production readiness, autofree status, v-lang]
level: advanced
status: draft
description: "Plan for V being pre-1.0: breaking changes, weekly releases, experimental features, and pin compiler versions in CI and Docker."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pre-1.0 stability caveats and version pinning

Goal: use V in real projects with eyes open (confirm all claims against current release notes).

- V remains pre-1.0 (0.4.x as of 2025); syntax and stdlib can change between releases. Recent examples: attributes `[x]` -> `@[x]`, `go` -> `spawn`, `vweb` -> `veb`, generics `<T>` -> `[T]`.
- Experimental or uneven areas: autofree, the wasm/JS backends, `ui`, `x.*` modules, ORM coverage, some crypto; check docs for "experimental" tags.
- Pin: record the V commit/tag in CI (`git clone https://github.com/vlang/v; git checkout <sha>; make`), cache `v` binaries, and pin Docker images by digest.
- Upgrade routine: `v up` on a branch, `v fmt -w .`, fix deprecations, run `v test .`, review warnings.
- Mitigate risk: small isolated modules, tests around boundaries, C interop for critical libs, prefer long-lived stdlib modules.
- Plan for compiler bugs: keep reduced repros, search GitHub issues, file with `v doctor` output.

Gotchas:
- Marketing claims (zero-cost, 1s builds) apply to specific cases; benchmark your workload.
- Docs on master may describe features unreleased in your install.

Verify: CI builds from the pinned commit reproducibly.
