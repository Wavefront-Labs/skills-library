---
id: computing-software.software-engineering.crystal.crystal-tool-format
name: crystal-tool-format
category: computing-software
field: software-engineering
product: crystal
tags: [crystal-tool-format, cli-spec-docs-format, tool-format, formatter, crystal-format, check, style, ci-format, gofmt-like, crystal]
level: intro
status: docs-checked
description: "Format Crystal source with crystal tool format: files and folders, --check for CI, -i and -e path filters, and - for stdin to stdout."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/man/crystal/README.md
  - https://github.com/crystal-lang/crystal/blob/master/src/compiler/crystal/command/format.cr
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# crystal tool format

Goal: enforce one code style.

- `crystal tool format [--check] [<path>...]` applies the default format; a path can be a file or a folder (all Crystal files in the tree). Omitting the path means the current working directory. Example: `crystal tool format src spec`.
- `--check` checks that formatting produces no changes (use it in CI); `-i <path>` / `--include <path>` and `-e <path>` / `--exclude <path>` filter paths (exclude default: `lib`); `--no-color` disables colour.
- To format stdin to stdout, use `-` in place of any path argument.
- The formatter also formats Crystal code blocks inside doc comments.

Gotchas:
- Run it before committing; a CI step with `--check` catches unformatted files.

Verify: `crystal tool format --check` exits 0.

## Checked

2026-11-03. Confirmed against the Crystal compiler manual (`crystal tool format` synopsis, path rules, code blocks in comments) and the `format` command source (options `--check`, `-i`, `-e`, `--no-color`, stdin with `-`).
Removed: the list of fixed style rules, "no config file", "does not reflow comments", "reports the line on syntax errors" and the editor/LSP integration note (none appear in the pages read).
Method: documentation only; no commands were run.
