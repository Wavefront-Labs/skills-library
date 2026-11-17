---
id: computing-software.web-development.biome.linter-plugins-choose-gritql-or-javascript
name: linter-plugins-choose-gritql-or-javascript
category: computing-software
field: web-development
product: biome
tags: [biome, linter-plugins, gritql, javascript-plugins, plugin-format, developer-preview, plugin-tradeoffs]
level: intro
status: docs-checked
description: "Compare GritQL and JavaScript Biome plugins on expressiveness, language support, semantic access, performance and memory before choosing."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/linter/plugins.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Biome supports two plugin forms: GritQL (a DSL for small expressive rules) and JavaScript (tapping into Biome infrastructure such as the CST and semantic model). The docs list the trade-offs.

**GritQL**
- A language is available to plugins only when both GritQL and Biome support it.
- You must learn the DSL, but a rule can be more expressive and need far less code.
- Plugins run on every file, whether or not the content matches the query.
- They use a different pipeline from Biome's Rust lint rules and have no access to the semantic model, file kind and similar information.
- Memory usage is minimal and controllable by Biome.

**JavaScript**
- Can support the same languages as Biome's Rust lint rules.
- Very verbose: a rule for something small could take about 10x more lines than GritQL.
- Has access to more information: the analysed file, the semantic model, CST navigation.
- It is much easier to write a plugin that hurts the performance of downstream users.
- Memory used by plugins cannot be controlled by Biome.

JavaScript plugins are in **Developer Preview**: breaking changes can happen in patch releases and features are missing; feedback goes to the JavaScript plugins tracking issue.

GritQL plugins currently target JavaScript, CSS and JSON. They can report diagnostics and suggest rewrites. Rewrites are applied by `--write` only if marked `fix_kind = "safe"`; with no `fix_kind` they count as unsafe and need `--write --unsafe`.

Decision guide (an editorial summary of the lists above, not stated verbatim by the docs): pick GritQL for syntactic pattern matching; pick a JavaScript plugin when you need the semantic model or file information, accepting the performance and memory risk.

## Checked

Method: 2026-11-08 compared against the Biome website source mdx for linter plugins (Decide the plugin format, GritQL plugins, JavaScript plugins). The trade-off lists and Developer Preview note match the page. Added the page's target-language and rewrite-safety facts, labelled the decision guide as editorial, and dropped an invented "Verify" step.
