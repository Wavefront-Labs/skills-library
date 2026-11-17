---
id: computing-software.web-development.phoenix.testing-controllers
name: testing-controllers
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, testing, conncase, controller-tests, json-api, exunit, phx-gen-json]
level: practitioner
status: docs-checked
description: "Write Phoenix controller tests with ConnCase for generated HTML and JSON resources: success and failure paths, redirects, 404s and fallback 422s."
sources:
  - https://hexdocs.pm/phoenix/testing_controllers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: test generated HTML and JSON controllers with `use HelloWeb.ConnCase`, covering success and failure at the integration level only.

## HTML controller tests (from `mix phx.gen.html Blog Post posts title body:text`)
Test files start with `use HelloWeb.ConnCase`, import fixtures (`import Hello.BlogFixtures`), define module attributes (`@create_attrs`, `@update_attrs`, `@invalid_attrs`) and use one `describe` per action.

- index: `conn = get(conn, ~p"/posts")` then `assert html_response(conn, 200) =~ "Listing Posts"`. The `~p` path is checked against the router.
- create, valid: `post(conn, ~p"/posts", post: @create_attrs)`, then `assert %{id: id} = redirected_params(conn)`, `assert redirected_to(conn) == ~p"/posts/#{id}"`, then `get` the show page and assert 200.
- create, invalid: post `@invalid_attrs` and assert `html_response(conn, 200) =~ "New Post"` (the form is re-rendered).
- delete: use `setup [:create_post]` (a private function returning `%{post: post_fixture()}`), `delete(conn, ~p"/posts/#{post}")`, assert `redirected_to(conn) == ~p"/posts"`, then:

```elixir
assert_error_sent 404, fn ->
  get(conn, ~p"/posts/#{post}")
end
```

`assert_error_sent` (from `Phoenix.ConnTest`) checks that an exception was raised and that it maps to the given status (here `Ecto.NotFoundError` becomes 404). The guide prefers it over `assert_raise Ecto.NotFoundError` because it checks what the browser would actually receive.

## How many failure cases?
Do not test every validation (missing title, missing body, short title) in controller tests. Those rules belong in context and schema tests; the controller is the integration layer and only needs broad success and failure coverage.

## JSON controller tests (from `mix phx.gen.json News Article articles title body`)
Follow the generator's final steps, then run `mix test`. JSON resources omit `new` and `edit` (`resources "/articles", ArticleController, except: [:new, :edit]`), so fewer tests are generated. JSON is built by plain functions in `ArticleJSON` (`index/1`, `show/1`), with no template.

- index: `conn = get(conn, ~p"/api/articles")`, `assert json_response(conn, 200)["data"] == []`.
- create, valid: the action calls `put_status(:created)` and sets a `location` header; test with `json_response(conn, 201)["data"]`, pull out `"id"`, then `get` it and match the fields.
- create, invalid: the action uses `with`, so `{:error, changeset}` falls through to `action_fallback HelloWeb.FallbackController`, which responds 422 via `ChangesetJSON`. Test: `assert json_response(conn, 422)["errors"] != %{}`.
- delete: the action returns `send_resp(conn, :no_content, "")`; test `assert response(conn, 204)` then `assert_error_sent 404, fn -> get(...) end`.

Context and schema code is the same for HTML and JSON; only the controller and view layers differ.

## Checked

2026-11-08. Read the Phoenix guide Testing Controllers in full. Confirmed the HTML and JSON test shapes, assert_error_sent 404 reasoning, the guideline on failure cases, action_fallback with a 422 response, and the 204 delete. Nothing removed.

Method: documentation only; no commands were run.
