---
id: computing-software.networking-hardware-and-wireless.caddy.error-directive-trigger
name: error-directive-trigger
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [error, handle-errors, status-code, error-message, caddyfile, raise-error]
level: practitioner
status: docs-checked
description: "Raise an error from the Caddyfile with the error directive so handle_errors can render a response; syntax, defaults and a complete path-based example."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/error
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: turn a routing decision into an error that your handle_errors routes can present.

Syntax: `error [<matcher>] <status>|<message> [<status>] { message <text> }`. The first non-matcher argument is either a three-digit status or a message string; when it is a message, the status may follow. The default status is `500` and the default message is empty. The `message` subdirective is an alternate way to write multi-line text.

Key point: `error` does not write a response itself. It only injects an error into the handler chain; the response is produced by `handle_errors`. That is the difference from `respond`, which writes immediately and does not invoke error routes.

Worked example from the page:
`example.com { root /srv  error /private* "Unauthorized" 403  error /hidden* "Not found" 404  handle_errors { rewrite /{err.status_code}.html  file_server }  file_server }`
Requests under `/private` get a 403 error, those under `/hidden` get a 404 error, and the error route serves `403.html` or `404.html` from the site root. The message is available inside the error route as `{err.message}` and the code as `{err.status_code}`.

## Checked

2026-11-03: read caddyfile/directives/error against this skill. Confirmed: syntax, defaults 500 and empty message, difference from respond, the handle_errors example with {err.status_code} and {err.message}.
Removed: nothing; no claim failed the check.
Method: documentation only; no commands were run.
