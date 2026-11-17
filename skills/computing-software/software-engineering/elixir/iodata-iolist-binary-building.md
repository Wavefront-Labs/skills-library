---
id: computing-software.software-engineering.elixir.iodata-iolist-binary-building
name: iodata-iolist-binary-building
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, iodata, iolist, binary-append, io-puts-iolist, refc-binary, sub-binary, efficiency-guide, iodata-binaries, elixir-performance]
level: advanced
status: docs-checked
description: "Build large outputs as iodata (nested lists of binaries) instead of concatenating binaries; convert with IO.iodata_to_binary/1."
sources: ["https://www.erlang.org/doc/system/efficiency_guide.html", "https://hexdocs.pm/elixir/IO.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# iodata, binaries and string building

**Goal:** avoid copies when producing or sending text.

```elixir
body = ["<html>", for(i <- items, do: ["<li>", i.name, "</li>"]), "</html>"]   # iodata: nested lists of binaries
IO.iodata_to_binary(body) ; IO.iodata_length(body)
File.write!(path, body)                         # content must be iodata
```

## Rules
- Concatenating binaries copies them into a new binary, which is why IO data exists for many append operations on small chunks.
- You cannot pattern match on the start of IO data; convert with `IO.iodata_to_binary/1` (implemented natively), and use `IO.iodata_length/1` to get the size without converting.
- Integers in IO data are bytes (0..255); integers in chardata are code points, and `IO.iodata_to_binary/1` on chardata raises an argument error.

## Self-check
`IO.iodata_to_binary(["The symbol for pi is: ", ?π])` raises, because the code point does not fit in a byte.

## Checked
2026-11-03: confirmed against the Elixir IO docs (iodata and chardata, copying on concatenation, `iodata_to_binary/1`, `iodata_length/1`) and the File docs (`write!/3` content is iodata). Removed: reference-counted/off-heap binary and `:binary.copy/1` claims, the 64-byte threshold, `:gen_tcp.send` and Phoenix `send_resp/3` claims, and the regex advice (none on the pages read).
Method: documentation only; no commands were run.
