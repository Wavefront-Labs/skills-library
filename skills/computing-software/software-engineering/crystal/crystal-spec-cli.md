---
id: computing-software.software-engineering.crystal.crystal-spec-cli
name: crystal-spec-cli
category: computing-software
field: software-engineering
product: crystal
tags: [crystal-spec-cli, cli-spec-docs-format, crystal-spec, spec-cli, line-filter, example-filter, fail-fast, order-random, junit, tap, verbose, tag-filter, crystal]
level: practitioner
status: docs-checked
description: "Run crystal spec on files, folders or file:line, filter with -e, --tag and --location, and use --order random with a seed, --fail-fast, --junit_output and --tap."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/man/crystal/README.md
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/guides/testing.md
  - https://github.com/crystal-lang/crystal/blob/master/src/compiler/crystal/command/spec.cr
  - https://github.com/crystal-lang/crystal/blob/master/src/spec/cli.cr
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# crystal spec command

Goal: run the right tests quickly.

- `crystal spec [<options>] [<file>[:line] | <folder>]... [-- <runner_options>]`. With no file argument it runs `spec/**/*_spec.cr`. Folder arguments add the `*_spec.cr` files under them. `file:line` runs the example at that line.
- All files are concatenated into one compiled binary; options the compiler does not recognise are forwarded to the spec runner, so `crystal spec --tag slow` works as well as putting them after `--`.
- Filters: `-e` / `--example <name>` (full nested name includes the text), `-l` / `--line <line>`, `--location <file>:<line>` (repeatable), `--tag <tag>` (repeatable; `~tag` excludes), `--list-tags`.
- Tags: `--tag a --tag b` runs examples tagged `a` or `b`; `--tag ~a --tag ~b` excludes both. Tag examples in code with `tags: "slow"`; `focus: true` runs only focused examples.
- Runner options: `-v` / `--verbose`, `--profile` (10 slowest; the short `-p` only works after `--`, since the compiler uses it for `--progress`), `--fail-fast`, `--junit_output <output_dir>`, `--tap`, `--color` / `--no-color`, `--dry-run`.
- `--order <mode>`: `default`, `random` or a numeric seed. A random run prints a seed on completion; rerun with `--order <seed>` to reproduce the order.
- Compile options before the files work too: `crystal spec -Dmyflag --release`, `--error-trace`.

Gotchas:
- The whole spec set compiles into one binary, so a compile error blocks all specs.
- Use `require "./spec_helper"` in each spec file if you keep a helper.

Verify: rerun a random-order failure with `--order <printed seed>`.

## Checked

2026-11-03. Confirmed against the Crystal compiler manual (`crystal spec` synopsis and runner options), the testing guide (tags, `focus`, random order and seed), the `spec` command source (forwarding of unknown options, compile options) and the spec runner's option parser.
Fixed: `--seed N` does not exist; the seed is passed as the value of `--order`. Removed: "randomise in CI to catch inter-test dependence".
Method: documentation only; no commands were run.
