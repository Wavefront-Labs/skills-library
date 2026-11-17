---
id: computing-software.web-development.phoenix.testing-basics
name: testing-basics
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, mixtest, tags, partition, exunit, conncase, seed, async]
level: practitioner
status: docs-checked
description: "Run Phoenix tests with mix test: by file or line, ExUnit tags (--only/--exclude/--include), seeds, CI partitioning, and how ConnCase works."
sources:
  - https://hexdocs.pm/phoenix/testing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: run and select Phoenix tests efficiently and understand the generated test scaffolding.

## ConnCase

Generated tests start with `use HelloWeb.ConnCase`, a `ExUnit.CaseTemplate` building on `ExUnit.Case`. Its `using` block sets `@endpoint`, adds `use HelloWeb, :verified_routes` (so `~p` works), imports `Plug.Conn` and `Phoenix.ConnTest`. Its `setup` sets up the SQL sandbox and returns `{:ok, conn: Phoenix.ConnTest.build_conn()}`, which tests pattern match: `test "GET /", %{conn: conn} do ... get(conn, ~p"/") ... html_response(conn, 200)`. View tests use `import Phoenix.Template` and `render_to_string(HelloWeb.ErrorHTML, "404", "html", [])`. `async: true` runs a case in parallel with other cases (tests inside still run serially).

## Select what runs

```console
mix test                                  # all
mix test test/hello_web/controllers/      # directory
mix test test/hello_web/controllers/error_html_test.exs      # file
mix test test/hello_web/controllers/error_html_test.exs:11   # test at line (any line of that test works)
```

Line numbers are treated as tags (`Including tags: [line: "11"]`).

## Tags

```elixir
@moduletag :error_view_case          # whole module; atom means true
@moduletag error_view_case: "value"
@tag individual_test: "yup"          # single test
```

```console
mix test --only error_view_case
mix test --only error_view_case:true
mix test --exclude error_view_case
mix test --only individual_test:yup
mix test --exclude error_view_case --include individual_test:yup
```

`--only tag:false` matches nothing and ExUnit reports that no test executed. Exclude by default in `test/test_helper.exs`:

```elixir
ExUnit.start(exclude: [error_view_case: true])
```

Override with `mix test --include error_view_case`. Useful for slow tests you only want in CI.

## Randomization

ExUnit randomizes order with a seed (printed at the end of each run). Re-run a failure sequence with `mix test --seed 401472`. Order-dependent sporadic failures hint at tests that leave state behind.

## Partitioning (CI)

`config/test.exs` uses `database: "hello_test#{System.get_env("MIX_TEST_PARTITION")}"`. Split across machines:

```console
MIX_TEST_PARTITION=1 mix test --partitions 4
MIX_TEST_PARTITION=2 mix test --partitions 4
MIX_TEST_PARTITION=3 mix test --partitions 4
MIX_TEST_PARTITION=4 mix test --partitions 4
```

Generators (e.g. `mix phx.gen.html Blog Post posts title body:text`) also generate tests. See `mix help test` for more.

## Checked

2026-11-08. Read the Phoenix guide Introduction to Testing in full. Confirmed ConnCase, running tests by directory, file and line, the --only/--exclude/--include tag behaviour, ExUnit.start(exclude: ...), --seed, and MIX_TEST_PARTITION with --partitions. Nothing removed.

Method: documentation only; no commands were run.
