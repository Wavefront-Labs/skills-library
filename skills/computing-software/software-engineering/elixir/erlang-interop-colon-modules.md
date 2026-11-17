---
id: computing-software.software-engineering.elixir.erlang-interop-colon-modules
name: erlang-interop-colon-modules
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, erlang-interop, erlang-module, colon-atom-call, charlist-boundary, rebar3-dep, hex-erlang-dependency, erl-term, elixir-interop]
level: practitioner
status: docs-checked
description: "Call Erlang modules as :module.function, convert strings and charlists at the boundary, and use Erlang dependencies from Mix."
sources: ["https://hexdocs.pm/elixir/erlang-libraries.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Calling Erlang modules and OTP libraries

**Goal:** use the whole OTP library set from Elixir.

```elixir
Base.encode16(:crypto.hash(:sha256, "Elixir"))
:io.format("Pi is approximately given by:~10.3f~n", [:math.pi])
to_string(:io_lib.format("~10.3f", [:math.pi]))   # formats to an iolist
:rand.uniform(6) ; :queue.new() ; :math.sqrt(2) ; :zlib.compress(data)
:binary.bin_to_list("Ø")   # [195, 152] raw bytes; String.to_charlist("Ø") gives [216]
```

## Rules
- Erlang module names are lowercase atoms (`:crypto`); Elixir modules are atoms too, and both are called by dispatching to the module name. Elixir discourages merely wrapping Erlang libraries: call them directly.
- `String` handles UTF-8 text and returns Unicode codepoints; `:binary` works on raw bytes for data that is not necessarily UTF-8.
- Elixir has no `printf`; use `:io.format/2` (to the terminal) or `:io_lib.format/2` (to an iolist). The format specifiers differ from printf.
- Any module outside the `:kernel` and `:stdlib` Erlang applications needs its application listed in `extra_applications` in `mix.exs` (for example `[extra_applications: [:crypto]]`); the application name is shown in the Erlang documentation sidebar.
- `:ets`/`:dets` hold large tables in memory or on disk; ETS tables are protected by default (only the owner writes, any process reads), and `:digraph` is built on ETS, so its functions mutate the graph in place.

## Self-check
Hash a string with `:crypto.hash/2` and encode it with `Base.encode16/1`; confirm `:crypto` is in `extra_applications`.

## Checked

Checked 2026-11-09 against the Elixir "Erlang libraries" guide on hexdocs.pm (Elixir v1.20.5 pages), read in full.
Confirmed: module naming and dispatch, `:binary` versus `String`, `:io.format/2` and `:io_lib.format/2`, `:crypto` with `extra_applications` and the `:kernel`/`:stdlib` rule, ETS default protection, `:digraph` in-place behaviour, the `:queue`, `:math`, `:rand` and `:zlib` examples.
Removed as unconfirmed: the charlist conversion advice, `:undefined` mapping, `:erlang.binary_to_term` with `[:safe]`, rebar3/Hex Erlang dependency notes, the `:timer`, `:lists`, `:calendar`, `:inet`, `:string` and `:proplists` calls, and the Erlang stdlib landing page source.

Method: documentation only; no commands were run.
