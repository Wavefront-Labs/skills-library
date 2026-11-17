---
id: computing-software.software-engineering.erlang.erl-interface-ei
name: erl-interface-ei
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-native, erl-interface-ei]
level: sme
status: draft
description: "Erlang C nodes: ei library for encoding terms and acting as a distributed node, versus ports."
sources:
  - https://www.erlang.org/doc/apps/erts/
  - https://www.erlang.org/doc/apps/erl_interface/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# C nodes with erl_interface and ei
**Goal:** know the options for a native program that talks Erlang distribution.

- `ei` (in the `erl_interface` application) is a C library that encodes and decodes the external term format and implements distribution handshake so a C program appears as a hidden node.
- Typical calls: `ei_connect_init`, `ei_connect`, `ei_x_new`, `ei_decode_*`, `ei_x_encode_*`, `ei_rpc` (names per the ei reference; verify signatures in the docs).
- Compare: ports (simplest, one OS process per port), NIFs (fastest, unsafe), C nodes (separate process, network speed, node lifecycle to manage).
- The wire format is the external term format: `term_to_binary/1,2` and `binary_to_term/1,2` in Erlang.
```erlang
Bin = term_to_binary(#{a => 1}, [compressed]),
#{a := 1} = binary_to_term(Bin).
```

## Gotchas
- Security: `binary_to_term/1` on untrusted data can create atoms and funs; use `binary_to_term(Bin, [safe])`.

## Self-check
Round-trip a term through the external format and inspect its first byte (131).
