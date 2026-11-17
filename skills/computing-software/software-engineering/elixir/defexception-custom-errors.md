---
id: computing-software.software-engineering.elixir.defexception-custom-errors
name: defexception-custom-errors
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, defexception, exception, message-callback, error-struct, exception-message]
level: practitioner
status: docs-checked
description: "Define exception structs with defexception, a message field or message/1 callback and use them in raise and as {:error, exception} values."
sources: ["https://hexdocs.pm/elixir/Kernel.html#defexception/1"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom exceptions with defexception

**Goal:** typed, matchable errors, following the `Kernel.defexception/1` docs.

```elixir
defmodule MyAppError do
  defexception [:message]
end

value = [:hello]
raise MyAppError,
  message: "did not get what was expected, got: #{inspect(value)}"

# preferred: pass the value to raise/2 and build the message in exception/1
defmodule MyAppError do
  defexception [:message]

  @impl true
  def exception(value) do
    msg = "did not get what was expected, got: #{inspect(value)}"
    %MyAppError{message: msg}
  end
end

raise MyAppError, value
```

## Rules
- Exceptions are structs backed by a module implementing the `Exception` behaviour: `exception/1` receives the arguments given to `raise/2` and returns the struct; `message/1` receives the struct and returns the message.
- With a `:message` field, `message/1` and a default `exception/1` are provided: the default accepts a string (used as the message) or keyword arguments merged into the struct. Both are overridable (`@impl true`).
- If the exception has no `:message` field, implement `message/1` yourself.
- The `defstruct/1` API is available in `defexception/1` (fields, defaults).
- Customising the message in `exception/1` from the value passed to `raise/2` is the preferred strategy.
- Rescue with `rescue e in MyAppError -> ...`; `Exception.message/1` calls the `message/1` callback.
- Do not use exceptions for ordinary control flow; return tagged tuples (see the design anti-patterns guide).

## Self-check
Raise the exception in IEx and read the printed message and struct fields.

## Checked
Date: 2026-11-02. Confirmed against Kernel.defexception/1 docs and Exception docs (behaviour callbacks, default exception/1 and message/1 with a :message field, preferred strategy, defstruct API). Removed: Plug.Exception status example, Error suffix naming claim, multi-field message/1 example, Exception.format example.
Method: documentation only; no commands were run.
