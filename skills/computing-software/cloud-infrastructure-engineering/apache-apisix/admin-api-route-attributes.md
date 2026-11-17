---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.admin-api-route-attributes
name: admin-api-route-attributes
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, admin-api, route, uris, hosts, priority, vars, enable-websocket]
level: practitioner
status: docs-checked
description: "Route object attributes in the APISIX Admin API: uri or uris, host matching, remote_addr, methods, priority, vars, upstream binding, timeout, enable_websocket and status."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/admin-api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Route attributes

Matching:
- `uri` or `uris`: one is required; they are mutually exclusive.
- `host` / `hosts`: exact or wildcard domains.
- `remote_addr` / `remote_addrs`: IPv4, IPv4 CIDR or IPv6.
- `methods`: an empty list matches all methods.
- `priority`: default 0; higher wins.
- `vars`, `filter_func`: advanced match rules.

Behavior:
- `plugins` and `script`: plugin and script configuration.
- `upstream` (inline) or `upstream_id`; `service_id`; `plugin_config_id`.
- `timeout`: object with `connect`, `send`, `read` in seconds.
- `enable_websocket`: false by default.
- `status`: 1 enabled (default), 0 disabled.
- `name`, `desc`, `labels`: metadata. A list GET can filter on `name`, `label` and (Routes only) `uri`; multiple filters are intersected.

The Admin API also takes a `ttl` URI parameter ("Request expires after the specified target seconds", example `ttl=1`).

## Checked

2026-11-04: read the Admin API page (Route request body table, filtering section, ttl URI parameter). Confirmed uri/uris, host/hosts, remote_addr, methods, priority default 0, vars, filter_func, timeout, enable_websocket default false, status default 1. Removed the claim that name/desc/labels are list filters (page lists name, label, uri) and the claim that ttl expires the route (page says the request expires).

Method: documentation only; no commands were run.
