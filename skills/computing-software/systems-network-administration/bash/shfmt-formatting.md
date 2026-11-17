---
id: computing-software.systems-network-administration.bash.shfmt-formatting
name: shfmt-formatting
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, shfmt-formatting, shfmt-editorconfig, shell-scripting]
level: practitioner
status: docs-checked
description: "Format shell scripts consistently with shfmt: indent flags, diff mode, editorconfig and CI check."
sources:
  - https://github.com/mvdan/sh
  - https://pkg.go.dev/mvdan.cc/sh/v3/cmd/shfmt
  - https://raw.githubusercontent.com/mvdan/sh/master/cmd/shfmt/shfmt.1.scd
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Formatting scripts with shfmt
**Goal:** enforce one style.
```bash
shfmt -i 2 -ci -bn -w script.sh     # 2 spaces, indent case, binary ops may start a line, write in place
shfmt -d .                           # CI: error with a diff when formatting differs
shfmt -l -w .                        # list files that differ and rewrite them
shfmt -ln posix script.sh            # parse as POSIX sh (-p is shorthand)
shfmt -f .                           # just list the shell files it finds
```
- Directories are walked for shell scripts: shell extensions like `foo.sh` and extensionless files with a shell shebang. `--detect exec|all` also reads shebangs of executable or all files.
- Dialect `-ln` is `bash`, `posix`, `mksh`, `bats` or `zsh` (default `auto`): detected from a shell extension, else the shebang, else bash. A `.sh` extension implies `posix` unless a valid shebang overrides it.
- Indent `-i`: `0` is tabs (the default), `N` is N spaces. `-i 2 -ci -bn` resembles Google's shell style.
- EditorConfig files are used for formatting options, but if any parser or printer flag is given, EditorConfig formatting options are not used (`-i=0` works as a harmless default). Use `--filename` so stdin finds the right EditorConfig.
- Other printer flags: `-sr` space after redirects, `-bl` block opening tokens on a new line; `-fn` and `-kp` are deprecated. `-s` simplifies code and `-mn` minifies (implies `-s`).
- shfmt parses statically and requires valid UTF-8, so it can stand in for `bash -n` as a syntax check, and it is stricter.
- Self-check: `shfmt -d` produces no output and exits cleanly after `-w`.

## Checked
Checked 2026-11-08 against the shfmt manual page source (flags, defaults, dialect detection, EditorConfig behaviour, examples), the project README and the pkg.go.dev overview. Removed: "pair it with ShellCheck" (not stated in the pages).

Method: docs-only read of cited pages, 2026-11-08
