---
id: computing-software.software-engineering.nim.parseopt-basics
name: parseopt-basics
category: computing-software
field: software-engineering
product: nim
tags: [parseopt-basics, command-line-parsing, parseopt, getopt, commandlineparams, paramstr, cmdline, options, argv, nim]
level: practitioner
status: docs-checked
description: "Loop over short and long options and positional arguments with std/parseopt and commandLineParams."
sources:
  - https://nim-lang.org/docs/parseopt.html
  - https://nim-lang.org/docs/os.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# parseopt: parsing command-line options

Goal: parse CLI args without dependencies.

```nim
import std/parseopt
for kind, key, val in getopt():
  case kind
  of cmdArgument: echo "arg ", key
  of cmdLongOption, cmdShortOption:
    case key
    of "help", "h": echo "usage"
    of "out", "o": echo "out=", val
    else: echo "unknown ", key
  of cmdEnd: discard
```
- Values attach with `:` or `=` (`--out=x`, `--out:x`). Passing non-empty `shortNoVal` (e.g. `{'v'}`) or `longNoVal` (e.g. `@["verbose"]`) names the options that take no value and also allows whitespace-separated values for the others: `--foo bar` for long options and `-j4` for short ones. `-c val` works only in `LaxMode` and `GnuMode`, not the default Nim mode.
- `commandLineParams()`, `paramCount` and `paramStr(i)` come from `std/os`.

Gotchas:
- The parser does not validate syntax: an option marked in `shortNoVal`/`longNoVal` still gets a value if the user passes one explicitly.

Verify: `prog --out=x file` yields option out=x and argument file.

## Checked

2026-11-03. Confirmed against the parseopt and os pages: getopt, cmdArgument/cmdLongOption/cmdShortOption/cmdEnd, shortNoVal and longNoVal semantics, `-j4` syntax, LaxMode/GnuMode, commandLineParams, paramCount, paramStr. Real error fixed: the old text implied `-k value` always works and that NoVal lists prevent swallowing; in the default mode whitespace-separated values need NoVal lists. Removed: the `--` terminator claim and the exit-code advice.

Method: documentation only; no commands were run.
