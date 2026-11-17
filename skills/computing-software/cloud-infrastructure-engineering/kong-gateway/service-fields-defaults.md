---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.service-fields-defaults
name: service-fields-defaults
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, service-entity, service-url, service-protocol, admin-api, services]
level: intro
status: docs-checked
description: "Kong Service entity fields and defaults (protocol http, port 80, enabled true), the write-only url shorthand, and creating a Service through the Admin API."
sources:
  - https://developer.konghq.com/gateway/entities/service/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service fields and defaults

A Service represents an upstream. Routes match client requests and forward them to a Service. Generally map one Service to each upstream service.

Fields:
- `host` (required)
- `name`
- `url`: shorthand that sets `protocol`, `host`, `port` and `path` together
- `protocol` (default `http`)
- `port`, `path`
- `enabled`: whether the Service is active
- `tags`

Defaults: `protocol` `http`, `port` `80`, `retries` `5`, `connect_timeout` / `read_timeout` / `write_timeout` `60000` ms, `enabled` `true`.

Create one with the Admin API (port 8001 by default):

```bash
curl -i -X POST http://localhost:8001/services/ \
  --header "Content-Type: application/json" \
  --data '{"name": "example-service", "url": "http://httpbun.com"}'
```

For traffic management a Service can point at an Upstream entity instead of a fixed URL.

## Checked

2026-11-04. Confirmed against services.lua (retries 5, protocol http, port 80, three timeouts 60000, enabled true, url shorthand fields) and the Gateway Services page (one Service per upstream, POST /services/ example, Upstream entity option). Removed unconfirmed specifics: the full protocol list, host case-sensitivity, the url write-only/not-returned claim, the 404 behaviour of a disabled Service, and the Upstream name matching rule. The Admin API port 8001 is the admin_listen default in kong.conf.default.

Method: documentation only; no commands were run.
