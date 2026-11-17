---
id: computing-software.software-engineering.elixir.exunit-assert-describe-test
name: exunit-assert-describe-test
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, exunit, assert, refute, assert-raise, assert-receive, describe, test-case, mix-test, exunit-basics, elixir-testing]
level: intro
status: docs-checked
description: "Write ExUnit tests with assert, assert_raise, assert_receive/refute_receive and describe blocks; run one test by file:line."
sources: ["https://hexdocs.pm/ex_unit/ExUnit.html", "https://hexdocs.pm/ex_unit/ExUnit.Assertions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ExUnit tests, assertions and describe

**Goal:** write readable, failing-for-the-right-reason tests.

```elixir
defmodule MathTest do
  use ExUnit.Case, async: true

  describe "add/2" do
    test "adds integers" do
      assert Math.add(1, 2) == 3
    end
    test "pattern match" do
      assert {:ok, %{id: id}} = fetch()          # binds id on success
      refute Math.zero?(1)
    end
    test "raises" do
      assert_raise ArithmeticError, fn -> 1 / 0 end
    end
    test "message" do
      send(self(), {:done, 1})
      assert_receive {:done, 1}, 500             # timeout ms
      refute_receive :other, 100
    end
  end
end
```
```bash
mix test ; mix test test/math_test.exs:12 ; mix test --include external:true
```

## Rules
- Call `ExUnit.start()` before tests run.
- A failed `assert left == right` prints `left:` and `right:` values in the diff.
- `assert` still expects a truth value when a match is used; use `==` or `match?/2`, and `match?/2` when the pattern needs guards.
- Tests inside a module never run concurrently; with `async: true` the module runs concurrently with other modules, so enable it only if tests change no global state (default `false`).
- `assert_receive` and `refute_receive` default to a 100 ms timeout (`assert_receive_timeout`), and tests time out after 60_000 ms by default.

## Self-check
Run a single test by line number with `mix test file:line`.

## Checked
2026-11-03: confirmed against the ExUnit, ExUnit.Case and ExUnit.Assertions docs (`async` default false and same-module serial runs, `assert_raise/2`, `assert_receive`/`refute_receive` with timeout and 100 ms default, `match?/2` for guards, 60_000 ms test timeout, `--include external:true`, file:line shortcut). Removed: `doctest`, the `_test.exs` and `test_helper.exs` naming rule, the actual-on-the-left advice, and the `--failed`, `--only`, `--seed`, `--trace` flags (the Mix test task page was not read).
Method: documentation only; no commands were run.
