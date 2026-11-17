---
id: computing-software.software-engineering.crystal.env-argv-optionparser
name: env-argv-optionparser
category: computing-software
field: software-engineering
product: crystal
tags: [env-argv-optionparser, process-system, env, argv, optionparser, option-parser, cli-arguments, flags, subcommands, help, exit-code, crystal]
level: practitioner
status: docs-checked
description: "Read environment variables, parse command-line flags with OptionParser, define subcommands, help text and exit codes."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/crystal/tree/master/src
  - https://github.com/crystal-lang/crystal-book/tree/master/docs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ENV, ARGV and OptionParser

Goal: build a CLI.

```crystal
require "option_parser"
verbose = false; port = 8080
parser = OptionParser.parse do |p|
  p.banner = "Usage: app [options]"
  p.on("-v", "--verbose", "Verbose") { verbose = true }
  p.on("-p PORT", "--port=PORT", "Port") { |v| port = v.to_i }
  p.on("-h", "--help", "Help") { puts p; exit }
  p.missing_option { |o| STDERR.puts "missing #{o}"; exit 1 }
  p.invalid_option { |o| STDERR.puts "bad #{o}"; exit 1 }
  p.unknown_args { |before_dash, after_dash| files = before_dash }
end
```
- `ENV["X"]` raises KeyError if absent, `ENV["X"]?`, `ENV.fetch("X", "d")`, `ENV["X"] = "v"`.
- `OptionParser.parse` defaults to `ARGV` and deletes the handled arguments from it, leaving the unhandled ones; `PROGRAM_NAME` is the binary.
- Subcommands: `p.on("build", "Build") { ... }`; once one is parsed, all subcommands are removed from the parser and its flags stay.
- `exit 2` for usage errors; write errors to STDERR.

Gotchas:
- Short options with values need a placeholder: `"-p PORT"`.
- Arguments after `--` are not parsed as options; `unknown_args` receives the ones before and after it separately.
- Env values are Strings; convert and validate.

Verify: run with `--help` and with a bad flag.

## Checked

Date 2026-11-03. Confirmed in the OptionParser and ENV source: OptionParser.parse(args = ARGV), on with short and long flag, banner, separator, missing_option, invalid_option, unknown_args (two arrays, before and after --), subcommand support and removal, handled arguments deleted from ARGV, ENV[], ENV[]?, ENV.fetch with default or block, ENV.delete. Fixed the unknown_args block (it yields two arrays) and a top-level @files that would not compile.

Method: documentation only; no commands were run.
