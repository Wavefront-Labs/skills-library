---
id: computing-software.software-engineering.elixir.bitstring-matching-nimble-parsec
name: bitstring-matching-nimble-parsec
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, bitstring, binary-pattern-matching, nimble-parsec, parser-combinator, endianness, big-little, protocol-parsing, binary-parsing]
level: advanced
status: draft
description: "Parse binary protocols with <<>> patterns (size, endianness, types) and text formats with NimbleParsec combinators."
sources: ["https://hexdocs.pm/elixir/Kernel.SpecialForms.html#%3C%3C%3E%3E/1", "https://hexdocs.pm/nimble_parsec"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Binary pattern matching and NimbleParsec

**Goal:** decode structured bytes and text without regexes.

```elixir
<<version::8, flags::4, len::size(12), payload::binary-size(len), rest::binary>> = packet
<<a::16-little, b::32-big-signed, f::float-32, s::binary-size(4), _::binary>> = data
<<255, 1>> = <<255::8, 1::8>> ; <<x::utf8, rest::binary>> = "é!"
for <<byte <- bin>>, do: byte

# NimbleParsec
defmodule Kv do
  import NimbleParsec
  defparsec :kv, ascii_string([?a..?z], min: 1) |> ignore(string("=")) |> integer(min: 1) |> tag(:pair)
end
Kv.kv("abc=12")     #=> {:ok, [pair: ["abc", 12]], "", %{}, {1, 0}, 6}
```

## Rules
- Default segment type is integer, 8 bits, unsigned, big-endian; specify `little`, `signed`, `float`, `binary`, `utf8`, `size(n)`, `unit`.
- A `binary-size(len)` can use a previously matched variable in the same pattern.
- Match failures raise `MatchError` or fall through to the next clause; use multi-clause functions for variants.
- NimbleParsec compiles combinators into function clauses at compile time (fast); keep `defparsec` modules small to limit compile time.
- Always handle the `rest` binary: it may hold the next message.

## Self-check
Parse a 2-byte length-prefixed message from a binary and return the remainder.
