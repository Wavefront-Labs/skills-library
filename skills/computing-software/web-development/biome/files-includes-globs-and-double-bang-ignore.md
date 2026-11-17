---
id: computing-software.web-development.biome.files-includes-globs-and-double-bang-ignore
name: files-includes-globs-and-double-bang-ignore
category: computing-software
field: web-development
product: biome
tags: [biome, files-includes, glob, negated-glob, double-bang, indexing, scanner, protected-files, tool-includes]
level: advanced
status: docs-checked
description: "Control which files Biome processes with files.includes, negated ! and !! patterns, per-tool includes, and know the protected lockfiles."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/configuration/configure-biome.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**CLI selection.** `biome format file1.js src/` processes `file1.js` and everything under `src/` (folders are traversed recursively). Globs on the command line are expanded by your shell, not Biome, and some shells lack recursive `**`.

**Protected files** are always ignored and never get diagnostics: `composer.lock`, `npm-shrinkwrap.json`, `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`.

**`files.includes`** takes glob patterns; entries starting with `!` exclude. Paths and globs in a config resolve from the directory containing that file (for an extended config, from the directory of the extending config). It applies to all tools; refine per tool with `<tool>.includes`:

```json
{
  "files": { "includes": ["src/**/*.js", "test/**/*.js", "!**/*.min.js"] },
  "linter": { "includes": ["**", "!test/**"] }
}
```

`biome format test/` formats `.js` files in `test/` except `.min.js`; `biome lint test/` lints nothing because the linter excludes `test/`.

**Caution:** a file not matching `files.includes` is excluded from every tool, so a tool-specific `includes` can never match it.

**`!` versus `!!`.** A single `!` excludes files from linting and formatting. A double `!!` excludes from any project-related operation: building the internal module graph (used by project rules) and type inference (used by type-aware rules). A file used by those operations is "indexed". Negated globs must be preceded by the `**` pattern:

```json
{ "files": { "includes": ["**", "!**/*.generated.js", "!!**/dist"] } }
```

Here `dist` is not indexed at all, while `*.generated.js` is not linted or formatted but is still indexed.

## Checked

2026-11-04: every remaining claim, flag, default and example was compared with the cited page(s) read in full and confirmed. Removed: the invented Verify step.

Method: fetched the cited pages with tools/review/fetch_pages.py, read them in full, ran tools/review/phrase_check.py and compared the remaining misses by hand.
