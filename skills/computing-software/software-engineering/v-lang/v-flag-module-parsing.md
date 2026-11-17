---
id: computing-software.software-engineering.v-lang.v-flag-module-parsing
name: v-flag-module-parsing
category: computing-software
field: software-engineering
product: v-lang
tags: [v-flag-module-parsing, cli-and-flag-modules, flag, flag module, command line, options, arguments, usage, parse args, fp, v-lang]
level: practitioner
status: docs-checked
description: "Parse command-line options with flag.new_flag_parser, typed getters, defaults, usage text and remaining positional args."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parsing flags with the flag module

Goal: simple option parsing.

```v
import flag
import os
mut fp := flag.new_flag_parser(os.args)
fp.application('mytool')
fp.version('0.1.0')
fp.description('does things')
fp.skip_executable()
n := fp.int('count', `c`, 3, 'how many')
verbose := fp.bool('verbose', `v`, false, 'chatty')
name := fp.string('name', `n`, 'x', 'who')
rest := fp.finalize() or { eprintln(err); println(fp.usage()); return }
```
- Struct-based parsing: `config, unmatched := flag.to_struct[Config](os.args, skip: 1)!` returns the struct and the flags that matched no field; field attributes are `@[short: v]`, `@[long: name]`, `@[only: n]`, `@[repeats]`, `@[ignore]`, `@[xdoc: 'text']`.
- Getters: `string, int, float, bool, string_multi, int_multi`.
- `finalize()` handles `--help`/`-h` itself (prints `usage()` and exits) and `--version` (prints application name and version, then exits).

Gotchas:
- `skip_executable()` removes the first argv entry (the executable name).
- `finalize()` returns the remaining non-option args in order and returns an error for an unknown flag or an invalid value, unless `allow_unknown_args()` was called.

Verify: run with `--count 5 -v file` and assert values.

## Checked

2026-11-03. Confirmed against the V repository source (vlib modules and doc/docs.md) read in this batch: FlagParser methods application/version/description/skip_executable/int/bool/string/float/string_multi/int_multi/usage/finalize/allow_unknown_args and builtin --help/--version handling (vlib/flag/flag.v), to_struct[T](input, config) !(T, []string) and the attribute list (vlib/flag/flag_to.v, README.md).
Removed or corrected: `config := flag.to_struct[Config](os.args)!` (it returns a tuple), `(confirm availability)`, the claim that -h is handled by usage() alone, and the 'skip_executable before getters' ordering rule.
Method: documentation only; no commands were run.
