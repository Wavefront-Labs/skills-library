---
id: computing-software.software-engineering.elixir.strings-binaries-charlists
name: strings-binaries-charlists
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, binary, charlist, utf8, bitstring, codepoint, graphemes, strings-binaries]
level: practitioner
status: docs-checked
description: "Strings are UTF-8 binaries; know byte_size vs String.length, the <<>> syntax, charlists and when Erlang APIs want them."
sources: ["https://hexdocs.pm/elixir/binaries-strings-and-charlists.html", "https://hexdocs.pm/elixir/String.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Strings, binaries and charlists

**Goal:** stop confusing bytes, code points and graphemes and handle Erlang charlists, following the Elixir binaries-strings-and-charlists guide.

```elixir
string = "hełło"
String.length(string)           #=> 5   (graphemes)
byte_size(string)               #=> 7   (UTF-8 bytes)
String.codepoints("👩‍🚒")        # several code points
String.graphemes("👩‍🚒")         # one grapheme
IO.inspect("hełło", binaries: :as_binaries)   # <<104, 101, 197, 130, 197, 130, 111>>
<<head::binary-size(2), rest::binary>> = <<0, 1, 2, 3>>
<<x::utf8, rest::binary>> = "über"            # utf8 modifier matches a character, not a byte
String.valid?(<<239, 191, 19>>)               #=> false

~c"hello"                       # charlist: list of integer code points
to_charlist("hełło")
to_string(~c"hełło")
inspect(heartbeats_per_minute, charlists: :as_lists)
"he" <> "llo"                   # binary concatenation; charlists use ++
```

## Rules
- Strings are UTF-8 encoded binaries. `String.length/1` counts graphemes, `byte_size/1` counts bytes; one grapheme can be made of several code points.
- Binary pattern matching works on bytes unless you use modifiers such as `utf8`; `binary-size(n)` matches `n` bytes and `binary` matches the rest of a binary of unknown size. Strings can be matched too.
- A charlist is a list of integers that are valid code points, mostly seen when interfacing with older Erlang libraries. `~c"..."` is the sigil for charlists.
- IEx prints a list of integers as a charlist when all of them are in the ASCII range; force the list form with `inspect(list, charlists: :as_lists)`.
- `to_string/1` and `to_charlist/1` convert between the two (they are polymorphic and accept other shapes like integers and atoms). Charlists are concatenated with `++`; `<>` raises `ArgumentError` on them.
- Invalid UTF-8 is a binary that is not a valid string: check with `String.valid?/1`.

## Self-check
Predict `byte_size("ñ")` versus `String.length("ñ")` before running them.

## Checked
Date: 2026-11-02. Confirmed against the Elixir binaries-strings-and-charlists guide (length vs byte_size, graphemes, binary-size, utf8 modifier, valid?, charlists, inspect charlists: :as_lists, to_string/to_charlist, ++ vs <>). Removed: prefix <> rule with known-size claim, Erlang module names, byte_size("héllo") figure, <<104,105>> example.
Method: documentation only; no commands were run.
