---
id: computing-software.web-development.phoenix.custom-error-pages
name: custom-error-pages
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, errorjson, errorhtml, customexceptions, error-pages, plug-exception, debug-errors, heex]
level: practitioner
status: docs-checked
description: "Customise Phoenix error pages with ErrorHTML templates and ErrorJSON clauses, plus custom exceptions with Plug.Exception."
sources:
  - https://hexdocs.pm/phoenix/custom_error_pages.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: serve your own error pages and map custom exceptions to HTTP statuses.

New projects have `ErrorHTML` and `ErrorJSON` views in `lib/hello_web/controllers/`. By default they render the status message from the template name (`"404.html"` becomes "Not Found") via `Phoenix.Controller.status_message_from_template/1`.

## See production behaviour in dev
In dev Phoenix shows a debug page. Set `debug_errors: false` in `config/dev.exs` and restart the server:
```elixir
config :hello, HelloWeb.Endpoint,
  ...,
  debug_errors: false,
  code_reloader: true,
```
Then visit a bad path such as http://localhost:4000/such/a/wrong/path.

## Custom HTML error pages
A view's `render/2` is the fallback when no `some_template/1` function exists. Quick option: add a clause in `HelloWeb.ErrorHTML`:
```elixir
def render("404.html", _assigns) do
  "Page Not Found"
end
```
Better: create `lib/hello_web/controllers/error_html/` with `404.html.heex` (your own markup), then in `ErrorHTML` add `embed_templates "error_html/*"` and delete the equivalent `render/2` clause, otherwise the function overrides the template.

Error templates are not rendered through the application layout, to avoid circular errors (a broken layout would fail again). Keep dependencies and logic in error templates minimal.

## ErrorJSON
Add clauses for particular codes:
```elixir
def render("500.json", _assigns) do
  %{errors: %{detail: "Internal Server Error"}}
end
```

## Custom exceptions
```elixir
defmodule HelloWeb.SomethingNotFoundError do
  defexception [:message]
end

raise HelloWeb.SomethingNotFoundError, "oops"
```
Plug and Phoenix treat all exceptions as 500 by default. Set the status either with the `Plug.Exception` protocol:
```elixir
defimpl Plug.Exception, for: HelloWeb.SomethingNotFoundError do
  def status(_exception), do: 404
  def actions(_exception), do: []
end
```
or a field: `defexception [:message, plug_status: 404]`. The protocol is handy for actionable errors.

## Actionable errors
`actions/1` returns buttons shown on the debug page when `debug_errors` is `true`, as a list of `%{label: String.t(), handler: {module(), function :: atom(), args :: []}}`. Phoenix itself uses this for a pending-migrations button.
```elixir
def actions(_exception) do
  [%{label: "Run seeds", handler: {Code, :eval_file, ["priv/repo/seeds.exs"]}}]
end
```

## Checked

Date: 2026-11-07

Confirmed: read each cited page in full, including embedded code snippets and command output, and matched every claim, command, option, function name and default line by line against the page text. Where a source is a repository guide, the guide markdown on the main branch was read.

Removed or changed: Nothing needed removal; every claim matched the page text.

Method: documentation only; no commands were run.
