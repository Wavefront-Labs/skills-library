---
id: computing-software.web-development.phoenix.function-components
name: function-components
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, component, attr, slot, function-component, heex, html, layouts]
level: practitioner
status: docs-checked
description: "Define Phoenix function components with attr/3, call them with <.name /> or Module.name, mark attributes required or default, and use layout components."
sources:
  - https://hexdocs.pm/phoenix/components.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: encapsulate markup as a function component.

A function component is any function that accepts `assigns` and returns a HEEx template. Docs: `Phoenix.Component` (phoenix_live_view package, which supplies HEEx and function components; `phoenix_html` supplies safe HTML building blocks).

Template `show.html.heex` is embedded in the view module, so components added to that module are callable from it:

```elixir
defmodule HelloWeb.HelloHTML do
  use HelloWeb, :html

  embed_templates "hello_html/*"

  attr :messenger, :string, required: true

  def greet(assigns) do
    ~H"""
    <h2>Hello World, from {@messenger}!</h2>
    """
  end
end
```

`use HelloWeb, :html` calls `html/0` in `HelloWeb`, setting up imports and config; those imports are also available in templates. Call it:

```heex
<Layouts.app flash={@flash}>
  <section>
    <.greet messenger={@messenger} />
  </section>
</Layouts.app>
```

- `<.greet` : component in the same module, dot-prefixed name.
- `<Layouts.app` or `<HelloWeb.HelloHTML.greet messenger="..." />` : component in another module, full name.

Required attributes make Phoenix warn when omitted. Optional: `attr :messenger, :string, default: nil`.

## Layouts

The root layout holds `<head>` and `<body>`, set in the router with `plug :put_root_layout, html: {HelloWeb.Layouts, :root}`; its `{@inner_content}` receives the rendered template. Menus live in the `app` component in `lib/hello_web/components/layouts.ex`; add e.g. `Layouts.admin` for another layout. The nested `:layouts`/`:layout` options are discouraged in new apps.

Related: computing-software.web-development.phoenix.heex

## Checked

Date: 2026-11-07

Confirmed: read each cited page in full, including embedded code snippets and command output, and matched every claim, command, option, function name and default line by line against the page text. Where a source is a repository guide, the guide markdown on the main branch was read.

Removed or changed: Nothing needed removal; every claim matched the page text.

Method: documentation only; no commands were run.
