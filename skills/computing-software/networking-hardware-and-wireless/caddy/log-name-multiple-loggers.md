---
id: computing-software.networking-hardware-and-wireless.caddy.log-name-multiple-loggers
name: log-name-multiple-loggers
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [log-name, no-hostname, access-log, multiple-loggers, health-check, caddyfile]
level: practitioner
status: docs-checked
description: "Route requests to different access log files with log_name and the log directive no_hostname option, such as a separate health-check log."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/log_name
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: send selected requests to a differently configured logger.

Syntax: `log_name [<matcher>] <names...>`. It overrides the logger name used for the request when writing access logs. Several names can be listed, in which case the request log goes to every matching logger.

Pairing: a named logger is declared with `log <name> { ... }`. Adding the `no_hostname` option to that log stops it being associated with the site block's hostnames, so only requests that set `log_name` for that name reach it.

Example from the page for health checks:
`localhost { log { output file ./caddy.access.log }  log health_check_log { output file ./caddy.access.health.log  no_hostname }  handle /healthz* { log_name health_check_log  respond "Healthy" }  handle { respond "Hello World" } }`
Normal traffic goes to the default access log file; `/healthz` requests go to the dedicated file because their handler sets `log_name health_check_log`, and the `no_hostname` logger would otherwise never receive anything.

Use this to keep noisy probes out of the main log, to split traffic by path or method, or to give one class of request a different encoder or output.

## Checked

2026-11-03: read caddyfile/directives/log_name against this skill. Confirmed: log_name syntax, multiple names, pairing with log no_hostname, the health-check example.
Removed or reworded: the closing suggestion to use log_skip (that directive is not on the cited page).
Method: documentation only; no commands were run.
