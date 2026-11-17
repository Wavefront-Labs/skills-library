---
id: computing-software.web-development.biome.config-files-and-vcs-options-reference
name: config-files-and-vcs-options-reference
category: computing-software
field: web-development
product: biome
tags: [biome, files-maxsize, files-ignoreunknown, experimentalscannerignores, vcs-root, vcs-defaultbranch, scanner, node-modules, force-ignore]
level: practitioner
status: docs-checked
description: "Reference for files and vcs options: includes semantics, ignoreUnknown, maxSize, scanner behaviour, force-ignore, vcs.root and defaultBranch."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/reference/configuration.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**`files.includes`** (string[]): globs selecting files and directories Biome can process. Omitted means no extra restriction; `[]` selects nothing. Biome ignores `node_modules/` even if a pattern matches.

**Scanner behaviour.** The scanner discovers nested configs and ignore files, and when enabled rules use the `project` or `types` domains it also indexes source files and project dependencies. It respects `files.includes` and VCS ignore files, but may still discover required metadata or index excluded source files needed for analysis. To guarantee a path is never indexed use a force-ignore pattern: `"includes": ["**", "!!**/dist"]`. Force-ignore build output and nested projects; prefer a regular `!` exclusion for generated source files that provide types or other project info.

**`files.ignoreUnknown`** (boolean, default false): whether to suppress diagnostics for unrecognised file types.

**`files.maxSize`** (integer bytes, default 1048576): larger files are skipped for performance with a warning diagnostic.

**`files.experimentalScannerIgnores`** (deprecated): names matched as whole path components, ignored unconditionally and never added to the module graph. Use force-ignore patterns in `files.includes`, or run `biome migrate`.

**`vcs`**
- `enabled` (default false): requires `clientKind` (`"git"` only).
- `useIgnoreFile` (default false): applies `.gitignore`, `.git/info/exclude` and supported `.ignore` files including nested ones. Root-file patterns resolve from `vcs.root`; nested ones from their own directory.
- `root`: directory where Biome looks for VCS files; relative values resolve from the config file's directory. Set it when the config is not at the repo root, e.g. `"root": "../"` in `frontend/biome.json`. If omitted: the config's directory, then the working directory; if neither exists VCS integration is disabled with a diagnostic.
- `defaultBranch`: base for `--changed` when `--since` is absent. With neither set, `--changed` fails.

## Checked

2026-11-04: every remaining claim, flag, default and example was compared with the cited page(s) read in full and confirmed. Removed: the invented Verify step.

Method: fetched the cited pages with tools/review/fetch_pages.py, read them in full, ran tools/review/phrase_check.py and compared the remaining misses by hand.
