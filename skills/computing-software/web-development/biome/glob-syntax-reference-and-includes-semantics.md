---
id: computing-software.web-development.biome.glob-syntax-reference-and-includes-semantics
name: glob-syntax-reference-and-includes-semantics
category: computing-software
field: web-development
product: biome
tags: [biome, glob-syntax, includes, negation, force-ignore, last-match-wins, globstar, dist-exclusion, shell-expansion]
level: advanced
status: docs-checked
description: "Biome glob rules: *, **, {a,b}, escapes, ! and !!, last match wins, files.includes versus other includes, and unsupported syntax."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/reference/configuration.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Globs match paths relative to the configuration directory, are case-sensitive and use `/`.

| Syntax | Meaning |
| --- | --- |
| `*` | characters within one path segment (`src/*.js`) |
| `**` | zero or more whole segments (`**/*.js`) |
| `{a,b}` | alternatives (`**/*.{js,ts}`) |
| `\` | escape; write `\\` in JSON (`file\\?.js`) |
| `!pattern` | exclude (`!**/*.test.js`) |
| `!!pattern` | force-ignore in `files.includes` (`!!**/dist`) |

Patterns are evaluated in order and **the last matching pattern wins**: `["**/*.js", "!**/*.test.js", "src/special.test.js"]` includes JS, excludes tests, then re-includes `src/special.test.js`. Start with a positive pattern, because a list with only exclusions selects no files.

`files.includes` applies to files and directories; other `includes` settings filter files for a feature, so directory exclusions are written differently:

| Goal | `files.includes` | other `includes` |
| --- | --- | --- |
| Exclude root `dist` | `!dist` | `!dist/**` |
| Exclude `dist` at any depth | `!**/dist` | `!**/dist/**` |
| Force-ignore `dist` at any depth | `!!**/dist` | not supported |

Outside `files.includes`, `!!` behaves like a regular `!`.

**Not supported:** `?` as a wildcard, character classes like `[abc]` or `[0-9]`, nested alternatives `{{a,b},c}`, `a**` or `**a` or `***` (`**` must fill a whole segment), consecutive `**/**`.

**CLI caution.** Biome does not interpret CLI arguments as globs. Unquoted globs may work only because your shell expands them first, and shell support varies (some lack `**`), so prefer `includes` in configuration.

## Checked

2026-11-04: every remaining claim, flag, default and example was compared with the cited page(s) read in full and confirmed. Removed: the invented Verify step.

Method: fetched the cited pages with tools/review/fetch_pages.py, read them in full, ran tools/review/phrase_check.py and compared the remaining misses by hand.
