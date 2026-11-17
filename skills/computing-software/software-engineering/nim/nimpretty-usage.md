---
id: computing-software.software-engineering.nim.nimpretty-usage
name: nimpretty-usage
category: computing-software
field: software-engineering
product: nim
tags: [nimpretty-usage, formatting-and-linting, nimpretty, formatter, format, indent, maxlinelen, check, editor-integration, nim]
level: practitioner
status: docs-checked
description: "Format Nim code with nimpretty (options --out, --outDir, --stdin, --indent, --maxLineLen) or the nph formatter (--check, --diff, --outdir, .nph.toml)."
sources:
  - https://nim-lang.org/docs/tools.html
  - https://github.com/nim-lang/Nim/blob/devel/nimpretty/nimpretty.nim
  - https://github.com/arnetheduck/nph
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nimpretty and nph formatting

Goal: consistent formatting.

- nimpretty is described on the Nim tools page as a source code beautifier that formats code according to the official style guide. Its usage text (from `nimpretty.nim`): `nimpretty [options] nimfiles...`.
- Options: `--out:file` (default: overwrite the input file), `--outDir:dir` (default: overwrite the input files), `--stdin` (read stdin, write stdout), `--indent:N` (`0`, the default, means autodetect), `--maxLineLen:N` (default 80), `--version`, `--help`.
- By default nimpretty overwrites the input, so run it on a clean git tree and review the diff. The usage text lists no `--check`, `--backup` or `--output` option.
- `nph` is a separate, opinionated, AST-based formatter. Per its README: `nph file0.nim file1.nim` formats in place, `nph src/` formats a directory, `--outdir:/tmp` writes elsewhere, `--check` verifies a file is formatted (useful in CI), `--diff` shows what would change, and `-` reads stdin. Configure it with `.nph.toml` (`exclude`, `extend-exclude`, `include`).

Gotchas:
- Different formatters produce different output; pick one per repo.
- Formatting in CI: use `nph --check`, since nimpretty has no check mode.

Verify: running the formatter twice produces no further change.

## Checked

2026-11-03. Confirmed: nimpretty usage text in the Nim source (options and defaults); Nim tools page description; nph README (commands, `--check`, `--diff`, `--outdir`, stdin, `.nph.toml` keys). Removed: `file.pretty.nim` output, `--backup`, `--output`, `nimpretty --check`, the `find | xargs` recipe, editor-integration claims, "experimental" and "widely used" wording, and the nimble-install claim for nph (not in the README text read).
Method: documentation only; no commands were run.
