---
id: computing-software.devops-ci-cd.packer.console-command
name: console-command
category: computing-software
field: devops-ci-cd
product: packer
tags: [console, repl, interpolation, debugging, cmd-console]
level: practitioner
status: docs-checked
description: "Experiment with variable interpolations and functions using packer console, in HCL2 and legacy JSON modes."
sources:
  - https://developer.hashicorp.com/packer/docs/commands/console/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`packer console` lets you experiment with variable interpolations. You can reach variables in the config you started it with, or supply them with `-var` (repeatable, e.g. `-var "myvar=asdf"`) and `-var-file` (e.g. `-var-file myvars.json`). Type an expression, press Enter to see the result; exit with `exit` or Control-C. `packer console -h` lists all options.

Versions: `console` exists from 1.4.2; HCL2 mode from 1.6.0. Go templating (`{{..}}` calls) does not work in HCL2 mode.

REPL commands: `help`, `exit`, and `variables` (lists variables read from `-var`, `-var-file` and the template).

HCL2 mode starts when you pass a folder or a `.pkr.hcl` file, or set `--config-type=hcl2` to play without a config file:

```bash
packer console folder/
packer console file.pkr.hcl
packer console --config-type=hcl2
```

Without a config file it is useful for the expression syntax and built-in functions. For scripting, pipe newline-separated commands in; only the output of the final command is printed unless an error occurs earlier:

```bash
$ echo "1 + 5" | packer console
6
```

JSON mode: given a template with `"variables": {"myvar": "asdfasdf"}`, entering `` {{user `myvar`}} `` prints `asdfasdf`, and `` {{user `myvar`}}-{{timestamp}} `` prints something like `asdfasdf-1559854396`. Piping one interpolation avoids the REPL: `echo {{timestamp}} | packer console` prints a Unix timestamp. Running with no template lets you try the template engine alone, and `packer console -var "myvar=fdsafdsa" -var-file myvars.json example_template.json` supplies variables.

## Checked

2026-11-08. Read the full console command page (Packer 1.16 docs source). Removed unsourced suggestions about regex, formatdate and cidrsubnet checks.

Method: documentation only; no commands were run.
