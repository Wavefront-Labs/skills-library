---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-service-defaults-config-entries
name: consul-service-defaults-config-entries
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, config-entries, service-defaults, proxy-defaults]
level: practitioner
status: docs-checked
description: "Write service-defaults, proxy-defaults and service-router config entries as HCL files and apply them with consul config write."
sources: ["https://developer.hashicorp.com/consul/docs/connect/intentions", "https://developer.hashicorp.com/consul/docs/services/configuration/services-configuration-reference"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Config entries are cluster-wide, centrally stored settings for the mesh.

```hcl
Kind     = "service-defaults"
Name     = "api"
Protocol = "http"
```

```sh
consul config write api-defaults.hcl
consul config read -kind service-defaults -name api
consul config list -kind service-defaults
consul config delete -kind service-defaults -name api
```

L7 intentions apply when the destination service uses an HTTP-based protocol, so set `Protocol` accordingly, and a `proxy-defaults` entry holds defaults for proxies.

Gotchas: write entries through the CLI or API; servers can also insert them at leadership with `config_entries.bootstrap` in the agent configuration. The ACL needed to write depends on the kind: `service:write` for service-defaults and service-router, `mesh:write` or `operator:write` for proxy-defaults, `intentions:write` for service-intentions.

Verify: `consul config read` returns the written entry.

## Checked

2026-11-03. Confirmed against the config entries HTTP API page (ACL per kind), the consul config write, read, list and delete command pages, the service-defaults reference (Protocol), the intentions overview (L7 needs an HTTP-based protocol) and the general options page (config_entries.bootstrap). Removed: the claim that entries are outside agent config, the disruption and silent-revert claims and the Envoy filter chain check.

Method: documentation only; no commands were run.
