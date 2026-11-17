---
id: computing-software.software-engineering.d.d-dfmt-dscanner-and-editor-tooling
name: d-dfmt-dscanner-and-editor-tooling
category: computing-software
field: software-engineering
product: d
tags: [d-dfmt-dscanner-and-editor-tooling, dev-tools, dfmt, dscanner, serve-d, dcd, editorconfig, lint, formatter, code-d, style-check, static-analysis, d]
level: practitioner
status: docs-checked
description: "Format with dfmt (.editorconfig keys), lint with dscanner (dscanner.ini, --styleCheck, --syntaxCheck), use serve-d/DCD/code-d editor tooling and dub lint in CI."
sources:
  - https://github.com/dlang-community/dfmt
  - https://github.com/dlang-community/D-Scanner
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dfmt, D-Scanner and EditorConfig

Goal: enforce style and static checks.

- Format: `dfmt` reads stdin and writes stdout; with a file name it writes the result to stdout; `dfmt --inplace file.d` (or `-i`) edits the file in place and needs a file name. The README calls dfmt beta quality and advises source control before `--inplace`.
- Config: dfmt reads `.editorconfig` files that apply to the file; command-line options override them. Standard keys: `indent_style` (`tab` or `space`, default `space`), `indent_size` (default 4), `tab_width`, `max_line_length` (default 120), `end_of_line`. dfmt-specific keys are prefixed `dfmt_`: `dfmt_brace_style` (`allman` default, `otbs`, `stroustrup`, `knr`), `dfmt_soft_max_line_length` (default 80), `dfmt_align_switch_statements`, `dfmt_space_after_cast`, `dfmt_template_constraint_style`, `dfmt_keep_line_breaks`, and others listed in the README.
- Example: `dfmt --inplace --space_after_cast=false --max_line_length=80 --soft_max_line_length=70 --brace_style=otbs file.d`.
- Skip a region: put `// dfmt off` before it and `// dfmt on` after it.
- D-Scanner: `dscanner lint source/` lists issues; `dscanner -S source/` or `--styleCheck` runs the style checks; `-s` / `--syntaxCheck` reports lex/parse errors only; `--report` writes a JSON report; `-f` / `--errorFormat` sets the message format (`-f github` for GitHub Actions); `--sloc` / `-l` counts lines of code; `--ctags` / `-c` emits ctags; `--imports` / `-i` lists imported modules.
- D-Scanner config: `dscanner.ini` found in the working directory or a parent overrides other files; `--config` gives a path; `--defaultConfig` generates a default file. Each check is `"enabled"`, `"disabled"` or `"skip-unittest"`; `--skipTests` equals turning every `"enabled"` into `"skip-unittest"`.
- Checks include unused variables and parameters, undocumented public declarations, redundant parentheses, `opCmp`/`opEquals`/`toHash` not declared `const`, and names that do not follow Phobos style (see the README list).
- Install: `dub run dfmt -- -h` runs it through DUB; `dub fetch dscanner && dub run dscanner`.

Gotchas:
- Different dfmt versions can format differently; pin the version in CI.
- Some options are listed as not yet implemented in the README (for example `dfmt_outdent_attributes`).

Verify: run dfmt then dscanner on a file with a deliberate violation.

## Checked

2026-11-03. Confirmed against: the dfmt README (options, EditorConfig properties, defaults, `// dfmt off`) and the D-Scanner README (`--styleCheck`/`-S`, `--syntaxCheck`/`-s`, `--report`, `--sloc`, `--ctags`, `--imports`, `--defaultConfig`, `dscanner.ini` values, check list).

Removed because the pages read did not confirm it: `dub lint`, `style_check` key, camelCase/PascalCase naming rule, `==` on floats check, serve-d/code-d/Neovim/Emacs/IntelliJ plugin names, `dub fetch dfmt && dub build dfmt`, the `git diff --exit-code` recipe.

Method: documentation only; no commands were run.
