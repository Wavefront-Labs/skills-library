---
id: computing-software.software-engineering.elixir.module-attributes-compile-time
name: module-attributes-compile-time
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, module-attribute, doc, moduledoc, accumulate, compile-time, external-resource, module-attributes]
level: practitioner
status: docs-checked
description: "Use @attributes for documentation, annotations and compile-time values, know they are snapshotted into functions, and prefer functions for plain constants."
sources: ["https://hexdocs.pm/elixir/Module.html", "https://hexdocs.pm/elixir/module-attributes.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Module attributes and compile-time values

**Goal:** use module attributes for documentation, annotations and compile-time values; prefer functions for plain constants.

```elixir
defmodule MyApp.Status do
  @service URI.parse("https://example.com")   # evaluated once, at compile time

  def status(_email), do: SomeHttpClient.get(@service)   # the computed %URI{} is substituted here

  @default_timezone "Etc/UTC"
  def shift(@default_timezone), do: :noop      # attributes work in patterns and guards
end

defmodule Constants do
  defp hours_in_a_day(), do: 24                # a function is usually enough for a constant
end
```

## Rules
- Reserved attributes include `@moduledoc`, `@doc`, `@spec` and `@behaviour`; see the `Module` docs for the full list of supported attributes (for example `@deprecated`, `@before_compile`, `@impl`, `@external_resource`).
- Attributes are temporary storage: the value is computed at compile time and a snapshot of it is substituted into every function that reads it; after compilation the attribute is discarded.
- Reading the same large attribute in many functions makes compilation slower (each read is a separate snapshot). Wrap it once in a private function (`defp example, do: @example`) and call that.
- Generally functions are sufficient for constants (`defp hours_in_a_day(), do: 24`). Use an attribute when you do work at compile time and inject the result, or inside patterns and guards (as an alternative to `defguard/1`).
- Do not put a newline between the attribute name and its value: it is then read, not set. Reading an undefined attribute prints a warning.
- `Module.register_attribute(__MODULE__, :name, accumulate: true)` makes repeated sets accumulate; `Module.get_attribute/2` then always returns a list.
- `@external_resource` annotates a file the module embeds so tools can recompile when it changes; its path is relative to the project's `mix.exs` folder (the current working directory), not to the source file.

## Self-check
After compilation `@service` no longer exists at runtime; only the functions that read it hold its value.

## Checked
Date: 2026-11-02. Confirmed against the Elixir module-attributes guide and Module docs (reserved attributes, compile-time substitution and snapshots, constants advice, patterns/guards use, accumulate, @external_resource path rule). Removed: Module.register_attribute order comment, Application.compile_env advice, regex/OTP-version caveat, unused-attribute warning claim, inline-in-function wording, Limits example.
Method: documentation only; no commands were run.
