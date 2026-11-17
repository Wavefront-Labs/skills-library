---
id: computing-software.software-engineering.erlang.binary-module
name: binary-module
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-binaries, binary-module]
level: practitioner
status: docs-checked
description: "Erlang binary module: split, match, part, replace, copy, decode_unsigned; sub-binary references; iolists and iolist_to_binary."
sources:
  - https://www.erlang.org/doc/apps/stdlib/binary.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The binary module and iolists
**Goal:** manipulate binaries without converting to lists.

```erlang
binary:split(<<"a,b,c">>, <<",">>, [global]).           % [<<"a">>,<<"b">>,<<"c">>]
binary:match(<<"hello">>, <<"ll">>).                     % {2,2}
binary:part(<<"hello">>, 1, 3).                          % <<"ell">>
binary:replace(<<"a-b">>, <<"-">>, <<"_">>, [global]).
binary:decode_unsigned(<<1,0>>, little).                 % 1
iolist_to_binary([<<"a">>, "b", [$c]]).                  % <<"abc">>
```
- Build output as an iolist (nested lists of bytes and binaries) and hand it to `gen_tcp:send/2` or `file:write/2` unflattened.
- `binary:split/3` returns binaries that reference the subject (no copy), so the subject cannot be garbage collected until the results are no longer referenced.
- `binary:copy/1` on a binary that references a larger one can free the larger binary for garbage collection. `binary:referenced_byte_size/1` reports the size of the referenced binary, to decide when to copy.

## Gotchas
- The module docs warn that deliberate copying does not necessarily free the larger binary and can create much more binary data than needed. Sharing is generally beneficial; copy only when small parts reference large binaries that are no longer used in any process.
- `binary_to_list/1` on large data creates a huge list of integers.

## Self-check
Split a CSV line, rebuild with iolists, and check `byte_size/1` of both.

## Checked

2026-11-03. Confirmed in the `binary` module page: `split`, `match`, `part`, `replace`, `decode_unsigned/2`, `copy/1`, `referenced_byte_size/1` and the reference/garbage-collection notes. Removed: the 64-byte reference-counting threshold.
Method: documentation only; no commands were run.
