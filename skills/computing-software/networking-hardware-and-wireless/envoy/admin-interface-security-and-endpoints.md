---
id: computing-software.networking-hardware-and-wireless.envoy.admin-interface-security-and-endpoints
name: admin-interface-security-and-endpoints
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, admin, admin-interface, config-dump, allow-paths, quitquitquit, healthcheck-fail, clusters, logging]
level: practitioner
status: docs-checked
description: "Secure the Envoy admin listener and use its main endpoints (config_dump, clusters, stats, runtime, logging, drain) safely."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/operations/admin.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# admin interface security and endpoints
The admin interface exposes destructive operations (shutdown) and private data (stats, cluster names, certs), so it must be reachable only over a secure network, ideally localhost only. Restrict reachable paths with `allow_paths`:

```yaml
admin:
  address: { socket_address: { address: 127.0.0.1, port_value: 9901 } }
  access_log_path: /dev/null
  allow_paths:
  - exact: /ready
  - prefix: /stats
```
`allow_paths` is a list of string matchers. All mutations are POST; a GET mutation returns 400. Hosts that reach the admin port should be attached only to the secure network to avoid CSRF.

Endpoints seen in the docs: `/help`, `/certs`, `/clusters` (with `?format=json`, `?filter=regex`), `/config_dump` (with `include_eds`, `mask`, `resource`, `name_regex`), `/contention`, `/cpuprofiler`, `/heapprofiler`, `/healthcheck/fail` and `/ok`, `/hot_restart_version`, `/init_dump`, `/listeners`, `/logging` (change log levels at runtime), `/memory`, `/quitquitquit`, `/reset_counters`, `/drain_listeners`, `/server_info`, `/ready`, `/stats`, `/runtime`, `/runtime_modify`, `/tap`, `/reopen_logs`.

Gotchas: `?format=json` omits default-valued fields; `/ready` returns non-200 until initialised. Verify with `curl -s localhost:9901/server_info` and `curl -s localhost:9901/ready`.

## Checked

2026-11-03. Confirmed against: operations/admin.rst (endpoint list, POST-only mutations, 400 on GET) and bootstrap.proto (allow_paths as StringMatcher list). Removed or corrected: the version hedge and the piped head in the verify step.

Method: documentation only; no commands were run.
