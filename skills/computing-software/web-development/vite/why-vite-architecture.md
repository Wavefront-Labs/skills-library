---
id: computing-software.web-development.vite.why-vite-architecture
name: why-vite-architecture
category: computing-software
field: web-development
product: vite
tags: [vite-architecture, unbundled-esm-dev, rolldown-oxc, full-bundle-mode]
level: intro
status: docs-checked
description: "Why Vite exists and how it works: pre-bundled dependencies plus on-demand native ESM source, the Rolldown/Oxc toolchain, full bundle mode and the Environment API."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/why.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Vite splits work in two:
- Dependencies, which rarely change, are pre-bundled once with fast native tooling.
- Source code is served on demand over native ESM; the browser loads only what the current page needs and Vite transforms each file when requested. Startup stays near instant regardless of app size, and edits use HMR over native ESM.

Production still bundles, because unbundled ESM costs extra network round trips from nested imports.

Toolchain: Vite originally used esbuild for dev and Rollup for builds. Rolldown (written in Rust, compatible with the plugin API the ecosystem relied on) unifies both, using Oxc for parsing, transforming and minifying, giving one consistent pipeline from dev to production.

Direction:
- Full bundle mode (being explored): the dev server would bundle like production, to cut the network overhead of many unbundled requests in very large codebases.
- Environment API: frameworks define custom environments (edge runtimes, service workers) with their own module resolution and execution rules.

The plugin API, based on Rollup conventions, made integration natural for frameworks such as Nuxt and SvelteKit, which chose Vite as their foundation.

## Checked

2026-11-07. Re-read the Why Vite guide (docs/guide/why.md) in full. Confirmed the pre-bundled dependencies versus on-demand native ESM split, near-instant startup, HMR, why production still bundles, the esbuild plus Rollup to Rolldown and Oxc story, full bundle mode and the Environment API. Reworded two overstated lines: full bundle mode is something the team is exploring, and the Rollup-based plugin API made framework integration natural rather than being the stated reason frameworks chose Vite.

Method: documentation only; no commands were run.
