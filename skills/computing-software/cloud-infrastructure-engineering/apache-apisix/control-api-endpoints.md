---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.control-api-endpoints
name: control-api-endpoints
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, control-api, healthcheck, plugins-reload, schema, port-9090]
level: practitioner
status: docs-checked
description: "The APISIX Control API on 127.0.0.1:9090: enable_control settings and endpoints for schema, health checks, GC, routes, services, upstreams, plugin reload and discovery dumps."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/control-api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Control API endpoints

Default config:

```yaml
apisix:
  enable_control: true
  control:
    ip: "127.0.0.1"
    port: 9090
```

Add `router: 'radixtree_uri_with_parameter'` under `control` to enable parameter matching. Do not expose this server to public traffic.

Endpoints on `http://127.0.0.1:9090`:
- `GET /v1/schema`: schema for main, plugins and stream-plugins (enabled plugins only).
- `GET /v1/healthcheck`: status of all health checkers; `/v1/healthcheck/{src_type}/{src_id}` for one resource; `.../checkers` lists its checkers (`[]` if none, 404 if the resource is missing).
- `POST /v1/gc`: full GC in the HTTP subsystem.
- `GET /v1/routes`, `/v1/route/{id}`, `/v1/services`, `/v1/service/{id}`, `/v1/upstreams`, `/v1/upstream/{id}`.
- `GET /v1/plugin_metadatas`, `/v1/plugin_metadata/{plugin_name}`.
- `PUT /v1/plugins/reload`: hot reload plugins.
- `GET /v1/discovery/{service}/dump` and `/show_dump_file`: discovery memory dump and configured service details.

## Checked

2026-11-04: read the Control API page; default config block, radixtree_uri_with_parameter router, the warning about public traffic, and every listed endpoint (schema, healthcheck and checkers behaviour, gc, routes, services, upstreams, plugin_metadatas, plugins/reload, discovery dump and show_dump_file) match. Nothing removed.

Method: documentation only; no commands were run.
