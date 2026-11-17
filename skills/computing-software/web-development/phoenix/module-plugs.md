---
id: computing-software.web-development.phoenix.module-plugs
name: module-plugs
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, plug, moduleplug, init, call, assign, locale, elixir]
level: practitioner
status: docs-checked
description: "Write a Phoenix module plug with init/1 and call/2, add it to a router pipeline, and read its assign in a template."
sources:
  - https://hexdocs.pm/phoenix/plug.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: package a connection transformation as a module plug.

A module plug implements two functions: `init/1` initialises the options later passed to `call/2`, and `call/2` transforms the conn (it is just a function plug).

Example in `lib/hello_web/plugs/locale.ex`, storing `:locale` for downstream plugs, actions and views:

```elixir
defmodule HelloWeb.Plugs.Locale do
  import Plug.Conn

  @locales ["en", "fr", "de"]

  def init(default), do: default

  def call(%Plug.Conn{params: %{"locale" => loc}} = conn, _default) when loc in @locales do
    assign(conn, :locale, loc)
  end

  def call(conn, default) do
    assign(conn, :locale, default)
  end
end
```

Add it to the `:browser` pipeline in `lib/hello_web/router.ex` with the default as option:

```elixir
plug HelloWeb.Plugs.Locale, "en"
```

Multiple `call/2` heads pattern-match the params and fall back to the default. `assign/3` (from `Plug.Conn`) stores values in the conn.

Show it in `lib/hello_web/controllers/page_html/home.html.heex`:

```heex
<p>Locale: {@locale}</p>
```

`http://localhost:4000/` shows the default; `http://localhost:4000/?locale=fr` shows `fr`. The page notes this pairs with Gettext for internationalisation.

Related: computing-software.web-development.phoenix.function-plugs

## Checked

Date: 2026-11-07

Confirmed: read each cited page in full, including embedded code snippets and command output, and matched every claim, command, option, function name and default line by line against the page text. Where a source is a repository guide, the guide markdown on the main branch was read.

Removed or changed: Nothing needed removal; every claim matched the page text.

Method: documentation only; no commands were run.
