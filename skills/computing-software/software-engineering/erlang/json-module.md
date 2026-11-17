---
id: computing-software.software-engineering.erlang.json-module
name: json-module
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-web, json-module]
level: practitioner
status: docs-checked
description: "Erlang/OTP 27 json module: json:encode/1 and json:decode/1,3 mapping to maps, binaries and null, with checked encoders."
sources:
  - https://www.erlang.org/doc/apps/stdlib/json.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JSON with the stdlib json module
**Goal:** encode and decode JSON without a dependency on OTP 27+.

```erlang
Iodata = json:encode(#{<<"a">> => [1, 2.5, true, null]}),
Bin = iolist_to_binary(Iodata),
#{<<"a">> := [1, 2.5, true, null]} = json:decode(Bin).
```
- The module is marked "since OTP 27.0". Objects decode to maps with binary keys; strings to binaries; arrays to lists; JSON null to the atom `null`.
- `json:encode/1` returns iodata. Atoms encode as strings (except `true`, `false`, `null`, which map to Boolean and Null); maps may have binary, atom or integer keys.
- `json:decode/3` is `decode(Binary, Acc0, Decoders)` and returns `{Result, Acc, Rest}`; `Decoders` is a map of optional callbacks (`array_start`, `object_push`, `null`, ...), for example decoding keys as atoms with `object_push`.
- `json:encode_map_checked/2` and `json:encode_key_value_list_checked/2` raise `error({duplicate_key, Key})` when the output would repeat a key.

## Gotchas
- `json:decode/1` errors: `unexpected_end` for incomplete JSON, `{invalid_byte, Byte}` for unexpected or invalid UTF-8 bytes.

## Self-check
Round-trip a nested map and print the encoded bytes.

## Checked

2026-11-03. Confirmed in the `json` module page: the data-mapping tables for `encode/1` and `decode/1`, `decode/3` signature and callback fallbacks, the checked encoders and their `duplicate_key` error, the decode errors, and "since OTP 27.0". Removed: the claim that jsx or jiffy are the older-OTP alternatives, the vague big-integer note, and the old ninenines source.
Method: documentation only; no commands were run.
