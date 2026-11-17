---
id: computing-software.web-development.vite.project-philosophy
name: project-philosophy
category: computing-software
field: web-development
product: vite
tags: [vite-philosophy, lean-core, modern-web-esm-only, framework-building, vite-ecosystem-ci]
level: intro
status: docs-checked
description: "Vite's design principles: lean extendable core, opinionated modern ESM, pragmatic native-tool performance, framework building blocks, and ecosystem CI."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/philosophy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
- Lean extendable core: Vite aims to support the most common patterns for building web apps out of the box while keeping core lean and maintainable, by providing strong primitives and APIs that plugins build on (and actively expanding core to be more extensible). Its plugin system is based on a superset of Rollup's plugin API. Its bundler, Rolldown, maintains compatibility with Rollup's plugin interface, so plugins can often be used across both Vite and plain Rollup projects.
- Pushing the modern web: Vite is opinionated toward modern code. Source code can only be written in ESM, so non-ESM dependencies must be pre-bundled as ESM to work; web workers are encouraged to use the `new Worker` syntax; Node.js modules cannot be used in the browser. New features follow these patterns to create a future-proof API, which may not always be compatible with other build tools.
- Pragmatic performance: the dev server architecture keeps HMR fast as projects scale. Vite is based on native tools (the Oxc toolchain and Rolldown) for intensive tasks, and keeps the rest of the code in JS to balance speed with flexibility. When needed, framework plugins tap into Babel to compile user code.
- Building frameworks on Vite: core is framework agnostic, with polished plugins for each UI framework. The JS API lets app framework authors build tailored experiences; Vite includes SSR primitives, and its plugins offer a way to share between frameworks. It also pairs well with backend frameworks such as Ruby and Laravel.
- Active ecosystem: Vite evolves through cooperation between framework and plugin maintainers, users and the Vite team. To minimise regressions each release, the team uses `vite-ecosystem-ci` to run the CI of major projects using Vite on selected PRs.

## Checked

Checked 2026-11-08 against the Vite guide page "Project Philosophy" (raw source of docs/guide/philosophy.md): all five principles, the ESM/worker/Node-module examples, the Rolldown-Rollup compatibility statement, Oxc/Rolldown/Babel usage, backend framework pairing and vite-ecosystem-ci were confirmed. Removed: the claim that workers "should" use `new Worker` (the page says "encouraged").

Method: documentation only; no commands were run.
