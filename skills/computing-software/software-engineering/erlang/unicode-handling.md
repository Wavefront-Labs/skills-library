---
id: computing-software.software-engineering.erlang.unicode-handling
name: unicode-handling
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-text, unicode-handling]
level: advanced
status: docs-checked
description: "Erlang Unicode: utf8 binaries, unicode:characters_to_binary/list, io:format ~ts, source encoding and +pc unicode."
sources:
  - https://www.erlang.org/doc/apps/stdlib/unicode.html
  - https://www.erlang.org/doc/apps/stdlib/unicode_usage.html
  - https://www.erlang.org/doc/apps/stdlib/io.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unicode, encodings and binaries
**Goal:** avoid mojibake and badarg on non-ASCII text.

```erlang
Bin = unicode:characters_to_binary("héllo"),            % UTF-8 binary
List = unicode:characters_to_list(Bin),
io:format("~ts~n", [List]),                              % ~ts for Unicode chardata
<<"é"/utf8>>.                                            % bit syntax utf8
```
- The source file encoding default has been UTF-8 since OTP 17.0; an encoding comment at the start of the file can change it. Binaries holding Unicode text use UTF-8 as the standard encoding.
- The shell and `~p` treat only Latin-1 characters as printable by default; start with `erl +pc unicode` to print wider characters as strings. This only affects heuristic output of lists and binaries; `~ts` always outputs a valid character list.
- `unicode:characters_to_binary/3` converts between encodings (`latin1`, `unicode`, `utf8`, `utf16`, `utf32`, with endianness tuples). It returns a binary, `{error, Binary, RestData}` or `{incomplete, Binary, Binary}` on bad input instead of raising, so check the result.
- `~ts` takes Unicode chardata; with plain `~s` a list containing integers above 255 is an error.

## Gotchas
- `list_to_binary/1` takes an iolist (bytes and binaries); use `unicode:characters_to_binary/1` for text with code points above 255.

## Self-check
Convert a string with an emoji to a binary and back and print it with `~ts`.

## Checked

2026-11-03. Confirmed in the `unicode` module page, the "Using Unicode in Erlang" chapter (source encoding, `+pc`, printable range) and the `io` page (`~ts`, `~s`). Removed: the JSON/HTTP libraries advice. The statement that `list_to_binary` fails above 255 was recast using the documented iolist argument type.
Method: documentation only; no commands were run.
