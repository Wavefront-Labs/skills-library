---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-service-mesh-intentions
name: consul-service-mesh-intentions
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, service-intentions, intentions, service-defaults]
level: practitioner
status: docs-checked
description: "Create L4 and L7 Consul intentions to allow or deny service traffic, use default-deny, and know existing connections are not cut."
sources: ["https://developer.hashicorp.com/consul/docs/connect/intentions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Intentions authorise which services may talk to each other through the mesh. L4 intentions decide by mTLS identity; L7 intentions can also match methods, paths and headers when the destination protocol is HTTP.

```sh
consul intention create -deny web db
consul intention create -allow api db
consul intention check web db
consul intention list
```

Intentions can also be defined with a service-intentions config entry. The default intention behaviour follows the `default_policy` setting: allow permits all service-to-service connections by default, deny blocks them unless an intention allows them.

Gotchas: changing allow to deny does not terminate existing connections; L4 changes affect new connections and L7 changes affect new requests. Intentions are cached locally on the agent and in supported proxies, so authorizations persist even if the agent is severed from the servers. Match order is by specificity, and deny beats allow when match criteria are weighted equally. Namespaces are an Enterprise feature; in Consul CE the only valid namespace is `default`.

Verify: `consul intention check web db` prints `Denied` and a new connection attempt through the sidecar is refused.

## Checked

2026-11-03. Confirmed against the intentions overview (L4 and L7 semantics, existing connections not severed, local caching, specificity then deny over allow, namespaces Enterprise, default_policy) and the consul intention create and check pages (-allow, -deny, Allowed or Denied output). Removed: the version-control preference, the restart or drain advice and the ACL-specific phrasing of default_policy.

Method: documentation only; no commands were run.
