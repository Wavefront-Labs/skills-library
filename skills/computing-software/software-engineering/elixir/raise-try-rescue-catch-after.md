---
id: computing-software.software-engineering.elixir.raise-try-rescue-catch-after
name: raise-try-rescue-catch-after
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, raise, rescue, try, catch, after, throw, exit, reraise, raise-rescue]
level: practitioner
status: docs-checked
description: "Raise exceptions, rescue by struct, use after for cleanup, and know throw/exit are rarely used except at boundaries."
sources: ["https://hexdocs.pm/elixir/try-catch-and-rescue.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# raise, try/rescue/catch/after

**Goal:** handle errors, throws and exits without swallowing real bugs, following the Elixir try/catch/rescue guide.

```elixir
raise "oops"                          # RuntimeError
raise ArgumentError, message: "bad"   # raise/2 with an exception name and keyword arguments

try do
  raise "oops"
rescue
  e in RuntimeError -> e              # %RuntimeError{message: "oops"}
end

try do
  Enum.each(-50..50, fn x -> if rem(x, 13) == 0, do: throw(x) end)
  "Got nothing"
catch
  x -> "Got #{x}"                     # "Got -39"
end

try do
  exit("I am exiting")
catch
  :exit, _ -> "not really"
end

try do
  File.write!(path, "olá")
after
  File.close(file)                    # runs whether or not the body raised
end

# observability: log, then reraise unchanged
try do
  work()
rescue
  e ->
    Logger.error(Exception.format(:error, e, __STACKTRACE__))
    reraise e, __STACKTRACE__
end
```

## Rules
- Elixir has three mechanisms: errors (exceptions), throws and exits. Errors are for unexpected or exceptional situations, never for controlling flow.
- Developers rarely use `try/rescue`: `File.read/1` returns `{:ok, _}`/`{:error, reason}` for `case`, while `File.read!/1` raises when a missing file is truly an error. The convention is a `foo` returning tuples plus a `foo!` that raises.
- "Fail fast" / "let it crash": for unexpected failures, do not rescue; processes are isolated and a supervisor restarts them from a known state.
- `throw`/`catch` is for the uncommon case where a value cannot be retrieved otherwise (for example a library without a proper API); if an API exists use it (`Enum.find/2`).
- `catch` catches exits (`:exit, reason`), and is rarely needed. A function body can use `rescue`, `catch` or `after` directly without a `try` line; a `catch` clause that matches nothing has no effect.
- `after` handles side effects and does not change the return value, but gives only a soft guarantee: if a linked process exits, `after` does not run. Files, ETS tables, sockets and ports are linked to the process and are cleaned up if it crashes.
- An `else` block matches on the result of the `try` body when it finishes without a throw or error.
- Use `__STACKTRACE__` both when formatting the exception and when reraising, so it is reraised as is.

## Self-check
Log from an `after` clause and confirm it runs when the body raises.

## Checked
Date: 2026-11-02. Confirmed against the Elixir try-catch-and-rescue guide (errors, throws, exits, rescue, catch, after soft guarantee, else, reraise with __STACKTRACE__, let it crash, function-body try). Removed: rescue with multiple exceptions list, tail-position and variable-leak rules, throw/catch :throw form, exit signalling claim.
Method: documentation only; no commands were run.
