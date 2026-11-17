---
id: computing-software.software-engineering.elixir.json-jason-encode-decode
name: json-jason-encode-decode
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, json, jason, jason-encoder, derive, encode-decode, json-module, poison, json-jason, elixir-data-formats]
level: practitioner
status: draft
description: "Encode and decode JSON with Jason, derive Jason.Encoder for structs with only/except and handle decode errors (newer Elixir ships a JSON module)."
sources: ["https://hexdocs.pm/jason"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# JSON with Jason and the JSON module

**Goal:** reliable JSON in and out.

```elixir
Jason.decode("{\"a\": 1}")                       #=> {:ok, %{"a" => 1}}
Jason.decode!(bin, keys: :atoms!)                # only existing atoms; plain :atoms is unsafe on untrusted input
Jason.encode!(%{a: 1}, pretty: true)
defmodule User do
  @derive {Jason.Encoder, only: [:id, :name]}    # allow-list fields so secrets are never serialised
  defstruct [:id, :name, :password_hash]
end
defimpl Jason.Encoder, for: Money do
  def encode(m, opts), do: Jason.Encode.string(Money.to_string(m), opts)
end
# Phoenix: config :phoenix, :json_library, Jason
# Elixir 1.18 added a built-in JSON module (unconfirmed API details): check hexdocs.pm/elixir/JSON.html
```

## Rules
- Decode returns string keys by default; map to known atoms/structs deliberately via changesets.
- Structs have no encoder unless derived or implemented: `Protocol.UndefinedError`.
- Large integers are exact, floats may lose precision; dates are not special: encode to ISO 8601 strings (`DateTime` and `Date` are supported by Jason).
- Decode errors are `%Jason.DecodeError{}`; return `{:error, :invalid_json}` at API boundaries.

## Self-check
Derive the encoder with `only:` and confirm `password_hash` is absent.
