---
id: computing-software.web-development.biome.cli-configuration-flags-override-config
name: cli-configuration-flags-override-config
category: computing-software
field: web-development
product: biome
tags: [biome, cli-config-flags, vcs-flags, formatter-flags, json-parse-flags, css-parse-flags, html-formatter-flags, whitespace-sensitivity, operator-linebreak]
level: advanced
status: docs-checked
description: "Shared CLI flags that override biome.json: VCS, files, general formatter, per-language formatter, linter and assist toggles, and parser flags."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/reference/cli.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Configuration flags override the equivalent settings in `biome.json`. Language-specific flags such as `--javascript-formatter-quote-style` carry the language and tool in the name; unset language options inherit the global value.

**VCS and files:** `--vcs-enabled`, `--vcs-client-kind=git`, `--vcs-use-ignore-file`, `--vcs-root`, `--vcs-default-branch`, `--files-max-size` (default 1 MiB), `--files-ignore-unknown`.

**General formatter:** `--format-with-errors` (false), `--indent-style` (tab), `--indent-width` (2), `--line-ending` (lf), `--line-width` (80), `--attribute-position`, `--bracket-same-line`, `--bracket-spacing`, `--delimiter-spacing`, `--expand=<auto|always|never>`, `--trailing-newline` (strongly discouraged to disable), `--use-editorconfig`.

**JavaScript:** `--jsx-everywhere` (default true, JSX allowed in .js/.mjs/.cjs), `--jsx-quote-style`, `--quote-properties=<preserve|as-needed>`, `--trailing-commas=<all|es5|none>`, `--semicolons=<always|as-needed>`, `--arrow-parentheses`, `--javascript-formatter-quote-style` (double), `--javascript-formatter-operator-linebreak=<before|after>` (default after), plus `--javascript-formatter-enabled`, `--javascript-linter-enabled`, `--javascript-assist-enabled` and inheritable indent/width/ending/attribute/bracket/delimiter/expand/trailing-newline flags.

**JSON:** `--json-formatter-*` (enabled, indent, line width, `--json-formatter-trailing-commas=<none|all>` default none, expand, bracket and delimiter spacing), `--json-linter-enabled`, `--json-assist-enabled`, parser flags `--json-parse-allow-comments` and `--json-parse-allow-trailing-commas`.

**CSS:** `--css-parse-css-modules` (enable when files do not end in `.module.css`), `--css-parse-tailwind-directives` (Tailwind CSS 4 directives), `--css-formatter-*` including `--css-formatter-quote-style`, `--css-linter-enabled`, `--css-assist-enabled`. **GraphQL** and **GritQL** have analogous `enabled`, indent, width, ending, trailing-newline, linter and assist flags.

**HTML:** `--html-formatter-whitespace-sensitivity=<css|strict|ignore>` (default css), `--html-formatter-indent-script-and-style` (false), `--html-formatter-self-close-void-elements=<always|never>` (never), `--html-formatter-bracket-same-line`, `--html-formatter-attribute-position`; its trailing-newline defaults to true rather than inheriting.

## Checked

2026-11-04: every remaining claim, flag, default and example was compared with the cited page(s) read in full and confirmed. Removed: the generic `--<language>-<tool>-<option>` naming pattern sentence (the page lists concrete flags) and the invented Verify step.

Method: fetched the cited pages with tools/review/fetch_pages.py, read them in full, ran tools/review/phrase_check.py and compared the remaining misses by hand.
