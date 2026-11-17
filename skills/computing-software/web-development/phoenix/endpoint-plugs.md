---
id: computing-software.web-development.phoenix.endpoint-plugs
name: endpoint-plugs
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, endpoint, pipeline, plug, request-lifecycle, router, controller]
level: practitioner
status: docs-checked
description: "How a Phoenix request flows from endpoint plugs through router and controller to the view, and what each layer is responsible for."
sources:
  - https://hexdocs.pm/phoenix/request_lifecycle.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: decide which layer (endpoint, router, controller, view) should hold a piece of request handling.

## Flow
All HTTP requests start in the endpoint, `HelloWeb.Endpoint` in `lib/hello_web/endpoint.ex`. It is a list of `plug` calls; each plug is one slice of request processing. The skeleton:
```elixir
defmodule HelloWeb.Endpoint do
  use Phoenix.Endpoint, otp_app: :hello

  plug Plug.Static, ...
  plug Plug.RequestId
  plug Plug.Telemetry, ...
  plug Plug.Parsers, ...
  plug Plug.MethodOverride
  plug Plug.Head
  plug Plug.Session, ...
  plug HelloWeb.Router
end
```
The last plug is the router, which takes over all further processing. The router maps verb/path pairs to controllers, and the controller asks a view to render a template.

## Layer responsibilities
- Endpoint (`Phoenix.Endpoint`): the common initial path for every request. Anything that must happen on all requests goes here.
- Router (`Phoenix.Router`): dispatches verb/path pairs to controllers and scopes functionality (for example, some pages need authentication, others not).
- Controller (`Phoenix.Controller`): reads request information, talks to the business domain, prepares data for the presentation layer.
- View: turns the controller's structured data into the presentation; views are often named after the content format they render.

## Related
computing-software.web-development.phoenix.request-lifecycle-page

## Checked

Date: 2026-11-07

Confirmed: read each cited page in full, including embedded code snippets and command output, and matched every claim, command, option, function name and default line by line against the page text. Where a source is a repository guide, the guide markdown on the main branch was read.

Removed or changed: Nothing needed removal; every claim matched the page text.

Method: documentation only; no commands were run.
