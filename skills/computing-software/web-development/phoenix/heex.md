---
id: computing-software.web-development.phoenix.heex
name: heex
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, heex, sigilh, template, interpolation, escaping, raw]
level: practitioner
status: docs-checked
description: "Use HEEx templates in Phoenix: curly-brace interpolation, escaping and raw, attribute syntax, :if and :for shorthands, and block constructs."
sources:
  - https://hexdocs.pm/phoenix/components.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: write HEEx ("HTML + Embedded Elixir") correctly.

Interpolate Elixir with `{...}` in bodies and tag attributes; `@name` reads `assigns.name`. Block constructs use `<%= ... %>`:

```heex
<%= if some_condition? do %>
  <p>True for user: {@messenger}</p>
<% else %>
  <p>False for user: {@messenger}</p>
<% end %>

<%= for number <- 1..10 do %>
  <tr><td>{number}</td><td>{number * number}</td></tr>
<% end %>
```

## HTML-aware extensions

- Escaping: `{"<b>Bold?</b>"}` renders the literal text, preventing HTML injection. `{raw("<b>Bold?</b>")}` allows HTML; use with extreme care.
- Attributes: `<div title="My div" class={@class}>`. `false` removes the attribute; a list of classes is handled.
- Dynamic attribute sets from a keyword list or map: `<div title="My div" {@many_attributes}>`.
- Validation: a missing or mistyped closing tag (`</div-typo>`) is reported.
- Shorthands:

```heex
<div :if={@some_condition}>...</div>

<ul>
  <li :for={item <- @items}>{item.name}</li>
</ul>
```

Templates are powered by the `~H` sigil (`Phoenix.Component` docs).

Related: computing-software.web-development.phoenix.function-components

## Checked

Date: 2026-11-07

Confirmed: read each cited page in full, including embedded code snippets and command output, and matched every claim, command, option, function name and default line by line against the page text. Where a source is a repository guide, the guide markdown on the main branch was read.

Removed or changed: Nothing needed removal; every claim matched the page text.

Method: documentation only; no commands were run.
