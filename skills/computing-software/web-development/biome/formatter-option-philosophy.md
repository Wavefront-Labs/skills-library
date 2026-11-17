---
id: computing-software.web-development.biome.formatter-option-philosophy
name: formatter-option-philosophy
category: computing-software
field: web-development
product: biome
tags: [biome, formatter-philosophy, option-philosophy, opinionated, prettier-challenge, bike-shedding, legacy-options]
level: intro
status: docs-checked
description: "Why Biome has so few formatter options, which ones exist for Prettier compatibility, and why new options are unlikely to be added."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/formatter/option-philosophy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Biome follows Prettier's option philosophy. The existing option set is considered stable and requests for new options are unlikely to be considered and may be closed without discussion.

**Opinionated by design.** Ideally Biome assumes one correct way to format and enforces it everywhere, acting as its own automatic style guide rather than a tool for implementing other style guides. The benefit is that discussions about spacing, breaks and indentation disappear and code review becomes free of reformatting requests; the consistency across the web ecosystem also helps people move between projects.

**History.** Biome started with a strict subset aimed at the most contentious JavaScript choices: indent style (tabs vs spaces), indent width and semicolons. It could avoid Prettier's pitfalls with options like `--bracket-same-line` and `--arrow-parens`, which Prettier calls options it is not happy to have: they cause bike-shedding and now exist only as a historical artefact. When the Prettier Challenge was announced Biome accepted it, which required implementing all of Prettier's options to reach compatibility.

**How to treat the existing options.** Biome considers them a legacy feature for compatibility, not a baseline feature set. Their existence is not a reason to add more ("if those exist, why not this one?").

**Style changes.** The formatting style is relatively stable and matches Prettier as much as possible, with a few intentional deviations. Changes to style may be implemented, but they are unlikely to become options; they apply universally to all future versions.

## Checked

2026-11-04: every remaining claim, flag, default and example was compared with the cited page(s) read in full and confirmed. Removed: the 'Practical guidance' paragraph and the invented Verify step.

Method: fetched the cited pages with tools/review/fetch_pages.py, read them in full, ran tools/review/phrase_check.py and compared the remaining misses by hand.
