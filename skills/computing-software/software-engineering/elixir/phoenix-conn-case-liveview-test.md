---
id: computing-software.software-engineering.elixir.phoenix-conn-case-liveview-test
name: phoenix-conn-case-liveview-test
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, conncase, datacase, liveviewtest, phoenix-conntest, live-render, element-click, fixtures, phoenix-testing]
level: practitioner
status: docs-checked
description: "Test with ConnCase (get/post and html_response), LiveViewTest (live/2, element/3, render_click) and DataCase; use generated fixtures."
sources: ["https://hexdocs.pm/phoenix/testing.html", "https://hexdocs.pm/phoenix_live_view/Phoenix.LiveViewTest.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing Phoenix controllers and LiveViews

**Goal:** cover web behaviour with fast tests.

```elixir
defmodule MyAppWeb.PostControllerTest do
  use MyAppWeb.ConnCase, async: true
  test "index", %{conn: conn} do
    conn = get(conn, ~p"/posts")
    assert html_response(conn, 200) =~ "Posts"
  end
  test "json create", %{conn: conn} do
    conn = post(conn, ~p"/api/posts", %{post: %{title: "x"}})
    assert %{"data" => %{"id" => _}} = json_response(conn, 201)
  end
end
defmodule MyAppWeb.CounterLiveTest do
  use MyAppWeb.ConnCase
  import Phoenix.LiveViewTest
  test "increments", %{conn: conn} do
    {:ok, view, html} = live(conn, ~p"/counter")
    assert html =~ "Count: 0"
    assert view |> element("button", "+") |> render_click() =~ "Count: 1"
  end
end
```

## Rules
- Test business logic in context tests (DataCase); keep controller tests for HTTP concerns.
- Select elements by id or data attributes rather than text for stability.
- `render_async/1` waits for `assign_async` results.

## Self-check
Write a failing-path test (invalid params) and assert the error response.

## Checked
2026-11-08: confirmed against the Phoenix testing guide, Phoenix.ConnTest (get, post, html_response, json_response) and Phoenix.LiveViewTest (live, element, render_click, render_async, assign_async). Removed: the log_in_user helper advice and the 422 status.
Method: documentation only; no commands were run.
