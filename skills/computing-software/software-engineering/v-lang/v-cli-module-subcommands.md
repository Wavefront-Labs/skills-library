---
id: computing-software.software-engineering.v-lang.v-cli-module-subcommands
name: v-cli-module-subcommands
category: computing-software
field: software-engineering
product: v-lang
tags: [v-cli-module-subcommands, cli-and-flag-modules, cli module, subcommands, cli.command, cli.flag, command tree, git-like cli, help, v-lang]
level: practitioner
status: docs-checked
description: "Build multi-command CLIs with cli.Command, flags per command, required flags, help and version output, and execute handlers."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Subcommands with the cli module

Goal: structured command trees (git-style).

```v
import cli
import os
mut app := cli.Command{ name: 'tool', description: 'demo', version: '1.0.0', execute: fn (cmd cli.Command) ! { println(cmd.help_message()) } }
app.add_command(cli.Command{ name: 'add', required_args: 1,
    flags: [cli.Flag{ flag: .bool, name: 'force', abbrev: 'f' }],
    execute: fn (cmd cli.Command) ! { f := cmd.flags.get_bool('force')!; println(cmd.args) } })
app.setup()
app.parse(os.args)
```
- Flag kinds (`FlagType`): `.bool .int .float .string .int_array .float_array .string_array`; `required: true`, `global: true` to add the flag to subcommands too, defaults via `default_value: ['x']`.
- Hooks: `pre_execute`, `post_execute`; `help`, `man` and (when `version` is set) `version` flags and commands are added automatically; `-h` and `-v` short forms need `posix_mode: true`.
- An error returned by a callback is printed with the label `cli execution error:` and the program exits.

Gotchas:
- Call `app.setup()` before `parse`; it links each subcommand to its parent.
- An unknown flag stops the program with `Command ... has no flag ...`; `disable_flags` skips flag parsing and the default flags.

Verify: `tool add x -f` prints args and flag.

## Checked

2026-11-03. Confirmed against the V repository source (vlib modules and doc/docs.md) read in this batch: Command fields name, description, version, execute, pre_execute, post_execute, flags, commands, required_args, args, posix_mode, disable_flags (vlib/cli/command.v), FlagType, Flag fields flag/name/abbrev/global/required/default_value, get_bool (vlib/cli/flag.v), setup, add_command, parse, help_message and the parse/error behaviour read in command.v.
Removed or corrected: defaults via `value` (the field is private, the default is `default_value`), and the vague 'Errors are printed and set exit code'.
Method: documentation only; no commands were run.
