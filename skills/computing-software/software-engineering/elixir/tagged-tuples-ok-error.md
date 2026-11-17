---
id: computing-software.software-engineering.elixir.tagged-tuples-ok-error
name: tagged-tuples-ok-error
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, ok-error, tagged-tuple, error-handling, fetch-bang, let-it-crash, tagged-tuples, elixir-errors]
level: practitioner
status: docs-checked
description: "Return {:ok, value} / {:error, reason} for expected failures, pair with ! variants, and let unexpected faults crash under a supervisor."
sources: ["https://hexdocs.pm/elixir/try-catch-and-rescue.html", "https://hexdocs.pm/elixir/design-anti-patterns.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tagged tuples and {:ok, _}/{:error, _}

**Goal:** a consistent error convention across a codebase, following the Elixir try/catch/rescue and design anti-patterns guides.

```elixir
File.read("hello")      #=> {:error, :enoent}
File.read("world")      #=> {:ok, "world"}

case File.read(file) do
  {:ok, body} -> IO.puts("Success: #{body}")
  {:error, reason} -> IO.puts("Error: #{reason}")
end

File.read!(path)        # returns the bare contents or raises File.Error

Map.fetch(map, key)     # {:ok, value} | :error
```

## Rules
- Convention: a function `foo` returns `{:ok, result}` or `{:error, reason}`; a `foo!` with the same arguments returns the bare result or raises. `File` is the model.
- Pick the tuple version when you want to handle outcomes with `case`/pattern matching; use the bang version when failure truly is an error (for example a file you expect to exist).
- A common community practice is `{:error, Exception.t}` (an exception struct as the reason), so callers can raise it with `raise/1`; a reason can also be an atom such as `:enoent`.
- Elixir does not impose exceptions: the application decides whether an error is exceptional. Errors are for unexpected situations, not for controlling flow; use tuples for expected failures.
- "Fail fast" / "let it crash": do not rescue what you cannot handle; supervisors restart the process.
- Functions like `Map.fetch/2` return `{:ok, value}` or a bare `:error` when there is a single failure mode.

## Self-check
Replace a `try/rescue` around `File.read!/1` with `case File.read/1`.

## Checked
Date: 2026-11-02. Confirmed against the Elixir try-catch-and-rescue guide, design-anti-patterns and Map.fetch/2 docs (foo/foo! convention, File examples, {:error, Exception.t} practice, let it crash). Removed: Ecto Repo.get example, atom-over-string reasons advice, MatchError at boundaries claim.
Method: documentation only; no commands were run.
