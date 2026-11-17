---
id: computing-software.web-development.phoenix.direct-responses
name: direct-responses
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, send-resp, putstatus, contenttype, text, json, conn, controller]
level: practitioner
status: docs-checked
description: "Send Phoenix responses directly with send_resp/3, set the content type or HTTP status with put_resp_content_type, put_format and put_status."
sources:
  - https://hexdocs.pm/phoenix/controllers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: build a response by hand with Plug functions when render, text or json do not fit.

Status and empty body:

```elixir
def home(conn, _params) do
  send_resp(conn, 201, "")
end
```

The browser shows a blank page with status 201. Without a content type some browsers (Safari) download the response. Set one with `put_resp_content_type/2`:

```elixir
conn
|> put_resp_content_type("text/plain")
|> send_resp(201, "")
```

## Other content types

Change the Content-Type header and provide a matching template, e.g. XML:

```elixir
conn
|> put_resp_content_type("text/xml")
|> put_format(:xml)
|> render(:home, content: some_xml_content)
```

This needs a `home.xml.eex` template (rendered by EEx) and a `PageXML` view embedding it. Valid mime types: see the `MIME` library.

## HTTP status

`Plug.Conn.put_status/2` (imported into controllers) takes `conn` and an integer or a friendly atom; atoms are listed in the `Plug.Conn.Status.code/1` docs.

```elixir
conn
|> put_status(202)
|> render(:home)
```

The status must be a valid number.

Related: computing-software.web-development.phoenix.rendering

## Checked

Date: 2026-11-07

Confirmed: read each cited page in full, including embedded code snippets and command output, and matched every claim, command, option, function name and default line by line against the page text. Where a source is a repository guide, the guide markdown on the main branch was read.

Removed or changed: Nothing needed removal; every claim matched the page text.

Method: documentation only; no commands were run.
