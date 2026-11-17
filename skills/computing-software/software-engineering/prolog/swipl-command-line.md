---
id: computing-software.software-engineering.prolog.swipl-command-line
name: swipl-command-line
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-cli, swipl-command-line, swipl-g-t]
level: intro
status: docs-checked
description: "Use swipl command line options: -g, -t, -q, -O, -f, -x, -o -c, --stack-limit, -- and exit codes."
sources:
  - https://github.com/SWI-Prolog/swipl-devel/blob/master/man/overview.plx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# swipl command line
```bash
swipl [options] file ... [[--] arg ...]
swipl -q -g main -t halt file.pl
swipl -g go -g halt file.pl           # exit 0 on success, 1 on failure, 2 on exception
swipl -o app -c file.pl               # compile to a saved state
swipl -x app.state -- arg1
swipl --stack-limit=2g file.pl
swipl --dump-runtime-variables
```
- `-g goal` can be repeated; goals run in order after loading.
- `-t goal` sets the toplevel; the process exits 0 if it succeeds and 1 if it fails.
- `-q` / `--quiet` sets the flag `verbose` to `silent`. `-O` optimises. `-f file` loads that initialisation file instead of the default; `-f none` skips it.
- `-x state` boots from a state; `-o output -c files` compiles to a state.
- `--stack-limit=size[bkmg]` limits stack size; the default is 1Gb combined on 64-bit.
- `--dump-runtime-variables` is the only option allowed this way: it prints shell variable settings.
- `--` stops option scanning; the remaining arguments are available through the flag `argv`.
- On Windows `swipl-win.exe` is the GUI version.
## Gotchas
- A failing or raising `-g` goal ends the process with status 1 or 2 as above.
## Self-check
`swipl -g fail -t halt; echo $?` prints 1.

## Checked

2026-11-03. SWI-Prolog manual "Command line options" page: usage line, -g/-t exit codes, -q, -O, -f, -x, -o/-c, --stack-limit, --dump-runtime-variables, `--`, flag argv, swipl-win. Removed: PLBASE environment variable remarks, the claim that a failing `-g` still enters the `-t` toplevel (the documented behaviour is the exit codes above) and a "console swipl.exe" claim.

Method: documentation only; no commands were run.
