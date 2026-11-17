---
id: computing-software.software-engineering.erlang.string-module
name: string-module
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-text, string-module]
level: practitioner
status: docs-checked
description: "Erlang string module: trim, split, lexemes, find, replace, pad, length and case functions working on Unicode strings."
sources:
  - https://www.erlang.org/doc/apps/stdlib/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The string module
**Goal:** handle text with the modern string API.

```erlang
string:trim("  hi  "),                        % "hi"
string:split("a,b,c", ",", all),              % ["a","b","c"]
string:lexemes("a  b", " "),                  % ["a","b"]
string:find("hello", "ll"),                   % "llo"
string:replace("a-b", "-", "_", all),         % chardata
string:uppercase("ß"), string:length("é"),
string:pad("7", 3, leading, $0).              % "007"
```
- Since OTP 20 the module accepts `unicode:chardata()` (strings, binaries, iolists mixed) and works on grapheme clusters; binary input gives binary output.
- The old Latin-1 functions such as `string:tokens/2`, `string:strip/1` and `string:len/1` are obsolete; do not use them in new code.
- `string:to_integer/1` returns `{Int, Rest}` or `{error, Reason}` (`no_integer` or `badarg`); `list_to_integer/1` and `binary_to_integer/1` are BIFs.
- `string:find/2` returns `nomatch` if absent. Most functions return `chardata()`; use `unicode:characters_to_binary/1` for a flat binary.

## Gotchas
- Results can be iolists, not flat strings, so do not compare them with `=:=` to a flat string.

## Self-check
Run each example in the shell and check the return shapes.

## Checked
2026-11-02. STDLIB `string` module docs (OTP 20 rework, grapheme clusters, chardata specs, obsolete function group, to_integer, find, pad, replace, split), ERTS `erlang` docs (list_to_integer, binary_to_integer), STDLIB `unicode` module (characters_to_binary). Removed: nothing contradicted; result comments for `uppercase`/`length` already omitted.
Method: documentation only; no commands were run.
