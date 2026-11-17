---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-maintenance-mode
name: consul-maintenance-mode
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, maintenance-mode, consul-maint, drain-node]
level: practitioner
status: docs-checked
description: "Use consul maint to take a service or node out of DNS and API results for patching, and understand it registers a critical check."
sources: ["https://developer.hashicorp.com/consul/commands/maint"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Maintenance mode marks a service, or all services on a node, as under maintenance so they do not appear in DNS query or API results. Under the hood it registers a critical health check against the node or service, and `-disable` deregisters that check.

```sh
consul maint -enable -reason "kernel patch"             # whole node
consul maint -enable -service web-1 -reason "deploy"    # one service ID
consul maint                                            # list mode: show current maintenance
consul maint -disable
consul maint -disable -service web-1
```

- `-service` takes a service ID, and the node and service flags are independent.
- `-reason` is optional and appears in the Notes field of the critical check.
- Requires the `node:write` ACL.

Gotchas:
- `-disable` is the only way back: the node flag is a registered check, so remember to run it after patching.
- The page describes the effect on DNS and API results only; draining existing connections is a separate task for your application or proxy.

## Checked

2026-11-03. Confirmed against the Consul v1.22 docs source (commands/maint): flags, list mode, critical check mechanism, Notes field, `node:write`. Removed: claims about cached client addresses, mesh proxies, persistence across agent restart, and the `dig` Verify step, none of which are on the page.
Method: documentation only; no commands were run.
