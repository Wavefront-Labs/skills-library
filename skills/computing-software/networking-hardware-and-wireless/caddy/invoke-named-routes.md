---
id: computing-software.networking-hardware-and-wireless.caddy.invoke-named-routes
name: invoke-named-routes
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [invoke, named-routes, route-reuse, shared-state, load-balancing, caddyfile]
level: advanced
status: docs-checked
description: "Caddy named routes and the experimental invoke directive: share one handler and its load-balancer state across many sites."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/invoke
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: define a handler chain once and call it from several sites.

`invoke [<matcher>] <route-name>` (experimental) runs a named route. A route that does not exist triggers an error. `invoke` can also be used inside another named route. It is aimed at handlers that keep in-memory state or are expensive to provision; with hundreds of sites or more, sharing one instance reduces memory usage.

Definition: a named route is declared with an `&(name) { ... }` block, as in the example below. Unlike `import`, invoke takes no arguments; use `vars` to define variables that the route can read instead.

Example: `&(app-proxy) { reverse_proxy app-01:8080 app-02:8080 app-03:8080 { lb_policy least_conn  health_uri /healthz  health_interval 5s } }`. Then `example.com { handle_path /app* { invoke app-proxy }  handle { root /srv  file_server } }` and `app.example.com { invoke app-proxy }`. The page says the same in-memory load balancing state is reused for every site.

Compare with `import`: it includes a snippet or file and is evaluated at Caddyfile parse time, before the structure is parsed.

## Checked

2026-11-08. Read the invoke directive page in full and the import directive page (summary, snippet and parse-time wording). Confirmed: experimental status, syntax, error on a missing route, use inside another named route, memory rationale for hundreds of sites, no arguments with `vars` as the alternative, and the full example. Removed the unread claims that named routes must be top level, are analogous to snippets, and that health checks are shared.

Method: documentation only; no commands were run.

