---
id: computing-software.web-development.biome.why-biome-toolchain-principles
name: why-biome-toolchain-principles
category: computing-software
field: web-development
product: biome
tags: [biome, toolchain, formatter, linter, assist-actions, rust, one-package, design-principles, rome-fork]
level: intro
status: docs-checked
description: "What Biome is and its design principles: one package, one config, fast by default, zero-config start, actionable diagnostics, editor-first."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/introduction/why-biome.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Biome is a toolchain for web projects, built to be fast and easy to set up. It began in August 2023 as a fork of Rome. Out of the box you get a Prettier-compatible **formatter** (it can format malformed code), a **linter** with hundreds of rules (Biome's own plus ports from ESLint and popular plugins), and **assist actions** that tidy code by sorting imports, ordering object keys, removing duplicate CSS classes and more.

**Design principles**
- **One package.** Install only `@biomejs/biome`. No parser plugins for TypeScript or JSX, no compatibility packages between formatter and linter, no separate ignore file. Biome parses each file once and hands the same context to formatter, linter and assist, so a lint fix never produces code the formatter rewrites, nor vice versa.
- **Fast by default.** Written in Rust (predictable memory, true parallelism, no Node.js dependency). On the official benchmark Biome formats about 25 times faster than Prettier and lints about 15 times faster than ESLint.
- **Zero configuration to start.** Run `biome check --write` to format, lint and tidy. In CI run `biome ci`, which checks and fails the build if anything needs fixing. When you want control, `biome init` creates `biome.json`. The formatter has a deliberately small option set (the Prettier option philosophy); the linter is the opposite, with rules enabled or disabled individually, by group or by domain.
- **Informative and actionable.** Every rule follows three pillars: explain the error, explain why it is a problem, tell you what to do. Diagnostics show the exact range, a plain-language explanation and a fix when one exists.
- **Built for the editor.** A first-party language server gives the same diagnostics, formatting and code actions as the CLI, even while code is malformed. Official extensions exist for VS Code, IntelliJ and Zed.
- **Compatible with what you use.** The formatter matches Prettier output in about 97 percent of cases; `biome migrate eslint` and `biome migrate prettier` convert existing configs.

## Checked

2026-11-08. Read the why-biome page in full. Unchanged: every claim (August 2023 Rome fork, six design principles, the 25x and 15x benchmark figures, 97 percent Prettier match). Removed: the invented Verify step.

Method: documentation only; no commands were run.
