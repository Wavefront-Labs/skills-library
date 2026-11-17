---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-node-and-service-deregistration
name: consul-node-and-service-deregistration
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, deregistration, services-deregister, critical-timeout]
level: practitioner
status: docs-checked
description: "Remove Consul services and nodes with consul services deregister, catalog API and deregister_critical_service_after, avoiding zombies."
sources: ["https://developer.hashicorp.com/consul/docs/services/configuration/services-configuration-reference", "https://developer.hashicorp.com/consul/docs/services/usage/checks", "https://developer.hashicorp.com/consul/commands/force-leave"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Graceful shutdown scripts should deregister before stopping the application.

```sh
consul services deregister -id=web-1
consul leave                      # graceful agent leave
```

Automatic cleanup for crashed services uses the check option `deregister_critical_service_after = "30m"` (API field `DeregisterCriticalServiceAfter`): if a check stays critical for longer than that duration, its service and all of its checks are deregistered.

Gotchas: `consul services deregister` only removes services registered with the agent it talks to; for services from configuration files the docs recommend deleting the file and reloading. If it reports an Unknown service ID, use the catalog API (`PUT /v1/catalog/deregister` with the node and service id). A node that dies without leaving is reaped as failed after 72 hours by default; `consul force-leave` moves it to `left` sooner, but only takes full effect if the agent has shut down permanently, and a returning agent rejoins before it is reaped. `leave_on_terminate` (on a TERM signal) defaults to true for clients and false for servers.

Verify: `consul catalog services` no longer lists the service, and `consul members` shows the node as `left`.

## Checked

2026-11-03. Confirmed against the consul services deregister page (local agent only, config file advice, catalog fallback), the agent check API page (DeregisterCriticalServiceAfter), the consul force-leave page (72 hours, left state, caveats) and the general options page (leave_on_terminate defaults). Removed: the one-minute reap interval, the anti-entropy claim and the quorum claim about consul leave.

Method: documentation only; no commands were run.
