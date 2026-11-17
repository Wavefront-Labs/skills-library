---
id: computing-software.software-engineering.elixir.mox-behaviour-mocks
name: mox-behaviour-mocks
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, mox, mock, expect, stub, verify-on-exit, defmock, behaviour-based-testing, mocks-mox]
level: advanced
status: draft
description: "Define a behaviour for an external dependency, create a Mox mock, set expectations per test and verify them; avoid mocking modules you do not own directly."
sources: ["https://hexdocs.pm/mox"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mocking with Mox and behaviours

**Goal:** test code that depends on HTTP, email, clocks, and so on without real calls.

```elixir
# lib: behaviour + config
defmodule MyApp.Weather do
  @callback temp(String.t()) :: {:ok, number()} | {:error, term()}
end
# config/test.exs
config :my_app, :weather, MyApp.WeatherMock
# lib code
@weather Application.compile_env(:my_app, :weather, MyApp.Weather.HTTP)
def report(city), do: @weather.temp(city)
# test_helper.exs
Mox.defmock(MyApp.WeatherMock, for: MyApp.Weather)
# test
import Mox
setup :verify_on_exit!
test "report" do
  expect(MyApp.WeatherMock, :temp, fn "Oslo" -> {:ok, 3} end)
  assert MyApp.report("Oslo") == {:ok, 3}
end
```

## Rules
- Mox requires a behaviour; this keeps mocks honest (the mock has the same callbacks).
- `expect/4` fails if not called the stated number of times; `stub/3` allows any number of calls.
- Concurrency: mocks are per-process; `async: true` works, but for processes spawned by the code under test use `allow/3` or global mode (`set_mox_global`, only for `async: false`).
- Prefer small explicit boundaries (ports and adapters) over stubbing deep internals.

## Self-check
Remove an `expect` call's matching invocation and see `verify_on_exit!` fail the test.
