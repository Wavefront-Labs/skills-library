---
id: computing-software.networking-hardware-and-wireless.caddy.respond-static-responses
name: respond-static-responses
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [respond, static-response, health-check, early-hints, heredoc, content-type, caddyfile]
level: practitioner
status: docs-checked
description: "Write fixed responses with the Caddyfile respond directive: status-or-body argument rules, 103 Early Hints, close, heredoc bodies and the Content-Type default."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/respond
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: return a hard-coded response from the Caddyfile.

Syntax: `respond [<matcher>] <status>|<body> [<status>] { body <text>  close }`. The first non-matcher argument is either a three-digit status or a body string; if it is a body, the next argument may be the status. Default status is `200`. Status `103` (Early Hints) writes without a body and lets the handler chain continue, since 1xx responses are informational. The `body` subdirective is an alternative for multi-line text. `close` closes the client connection after the response.

Content-Type: if the body is non-empty and the header is unset, Caddy uses `text/plain; utf-8`, or `application/json` when the body is a valid JSON object or array. For anything else (HTML for example) set the type yourself with the `header` directive.

Examples: `respond /health-check 200` plus `respond "Hello, world!"`; `respond /secret/* "Access denied" 403 { close }`; and an HTML page using a heredoc: `header Content-Type text/html` then `respond <<HTML ... HTML 200`, using heredoc syntax to control whitespace.

Distinction: responding with an error status is not the same as returning an error in the handler chain. A `respond` 403 does not invoke `handle_errors`; the docs suggest the `error` directive when you want the error handlers to run.

## Checked
2026-11-03. Confirmed against the Caddy respond directive page: syntax, option names, defaults, limits and examples stated here. Removed: statements the page does not make.
Method: documentation only; no commands were run.
