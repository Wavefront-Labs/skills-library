---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-service-registration
name: consul-service-registration
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, service-registration, service-definition, consul-services]
level: practitioner
status: docs-checked
description: "Register Consul services via definition files with unique ids, tags, meta and ACL token, and avoid port and ports conflicts."
sources: ["https://developer.hashicorp.com/consul/docs/services/configuration/services-configuration-reference"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A service definition file in the agent config directory registers it on that agent. Only `name` is required, but production definitions also set `id`, `port`, `tags`, `meta` and a health check.

```hcl
service {
  name = "web"
  id   = "web-1"
  port = 8080
  tags = ["v2", "prod"]
  meta = { owner = "payments" }
  check {
    http     = "http://localhost:8080/health"
    interval = "10s"
    timeout  = "2s"
  }
}
```

Gotchas: `id` defaults to the service `name` when omitted, so give distinct ids to multiple instances of one service. `port` and `ports` cannot both be set in one definition, and `ports` supports service discovery only. `token` is required if ACLs are enabled. `meta` allows up to 64 pairs, keys limited to 128 characters and values to 512.

Verify: `consul reload`, then `consul catalog services` lists `web`, `dig @127.0.0.1 -p 8600 web.service.consul` returns the node address, and `consul catalog nodes -service=web` shows the node.

## Checked

2026-11-03. Confirmed against the service definition reference (name required, id defaults to name, port and ports exclusive, ports discovery only, token required with ACLs, meta limits), the consul reload and consul catalog nodes pages and the DNS reference. Removed: the overwrite claim for duplicate ids, the namespace-inheritance claim and the tags-are-opaque claim.

Method: documentation only; no commands were run.
