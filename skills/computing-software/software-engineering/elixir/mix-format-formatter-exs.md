---
id: computing-software.software-engineering.elixir.mix-format-formatter-exs
name: mix-format-formatter-exs
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, mix-format, formatter-exs, line-length, locals-without-parens, import-deps, check-formatted, formatter]
level: practitioner
status: docs-checked
description: "Configure .formatter.exs (inputs, line_length, import_deps, locals_without_parens), run mix format and enforce with --check-formatted in CI."
sources: ["https://hexdocs.pm/mix/Mix.Tasks.Format.html", "https://hexdocs.pm/elixir/Code.html#format_string!/2"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mix format and .formatter.exs

**Goal:** one canonical format with no style debates.

```elixir
# .formatter.exs
[
  import_deps: [:ecto, :phoenix],             # reuse deps' locals_without_parens
  plugins: [MixMarkdownFormatter],            # modules implementing the Mix.Tasks.Format behaviour
  inputs: ["{mix,.formatter}.exs", "{config,lib,test}/**/*.{ex,exs}"],
  line_length: 98,
  locals_without_parens: [my_dsl: 2]
]
```
```bash
mix format                       # rewrite files
mix format --check-formatted     # exit 1 if any file differs (CI)
mix format --dry-run                 # do not save files after formatting
```

## Rules
- The default `line_length` is 98; it is the length to aim for, not a guarantee.
- Newlines inside blocks are kept as in the input, with a few exceptions listed in the `Code.format_string!/2` docs.
- The formatter hard codes no names; add DSL macro names to `locals_without_parens`, or list the dependency in `import_deps` (the dependency exports its `locals_without_parens` from its own `.formatter.exs`).
- Use `--check-formatted` in a pre-commit hook or CI; output may differ between Elixir versions. `--no-exit` reports problems without a non-zero exit.
- With plugins, your code is compiled first unless `--no-compile` is given; plugins run in the order listed, and their file extensions must be added to `inputs`.

## Failure modes
- Files that match no `inputs` pattern are not formatted by a bare `mix format`; add plugin file extensions (for example `.md`) to `inputs`.

## Self-check
Commit an unformatted file and confirm `mix format --check-formatted` exits non-zero.

## Checked
2026-11-03: confirmed against the Mix.Tasks.Format and Code.format_string!/2 docs (`inputs`, `import_deps`, `plugins`, `line_length` default 98, `locals_without_parens`, `--check-formatted`, `--no-exit`, `--dry-run`, `--no-compile`, plugin ordering, newline handling). Removed: `subdirectories`, `--check-equivalent`, the Phoenix LiveView plugin example, the claims about `do:` versus `do/end` and Credo, and the editor-on-save advice.
Method: documentation only; no commands were run.
