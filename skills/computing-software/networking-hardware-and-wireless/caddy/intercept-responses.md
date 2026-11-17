---
id: computing-software.networking-hardware-and-wireless.caddy.intercept-responses
name: intercept-responses
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [intercept, handle-response, replace-status, response-matcher, x-accel-redirect, frankenphp, caddyfile]
level: advanced
status: docs-checked
description: "Intercept and rewrite responses from any handler with the Caddyfile intercept directive: response matchers, replace_status, handle_response and X-Accel-Redirect."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/intercept
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: react to what a handler returned, generalising the response interception built into reverse_proxy.

Syntax: `intercept [<matcher>] { @name { status <code...>  header <field> [<value>] }  replace_status [<response_matcher>] <code>  handle_response [<response_matcher>] { <directives...> } }`. It works with any handler that produces responses, including plugin handlers such as FrankenPHP's `php_server`.

Matching: define one or more uniquely named response matchers (`@name`), matching on status codes and on the presence or value of a response header. The first matching `handle_response` route or `replace_status` is invoked. If a `handle_response` has no matcher, every response is intercepted; with several blocks, the first match is applied, and any directive may be used inside.

Behaviour: when a route runs, the original body is held back so the route can write a different body, a new status, or adjust headers. If the route writes no body, the original body is sent. `replace_status` only swaps the status code.

Placeholders inside `handle_response`: `{resp.status_code}` and `{resp.header.*}` expose the original response.

Example (X-Accel-Redirect support in front of PHP): `localhost { root /srv  intercept { @accel header X-Accel-Redirect *  handle_response @accel { root /path/to/private/files  rewrite {resp.header.X-Accel-Redirect}  method GET  file_server } }  php_server }`. The PHP app names a file via the header and Caddy serves it from the private root.

## Checked

2026-11-03: read caddyfile/directives/intercept against this skill. Confirmed: intercept syntax, response matchers, replace_status and handle_response behaviour, {resp.*} placeholders, X-Accel-Redirect example.
Removed: nothing; no claim failed the check.
Method: documentation only; no commands were run.
