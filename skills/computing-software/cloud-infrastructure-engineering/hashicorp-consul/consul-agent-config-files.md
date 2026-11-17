---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-agent-config-files
name: consul-agent-config-files
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, agent-configuration, config-files, consul-validate]
level: practitioner
status: docs-checked
description: "Structure Consul agent config in HCL or JSON files, use correct duration strings and address roles, and validate with consul validate."
sources: ["https://developer.hashicorp.com/consul/docs/agent/config/config-files"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Write agent configuration in HCL or JSON files and group related settings (for example ACL parameters) into separate files so changes are easier to manage. Start the agent with `-config-dir` to load a directory of files.

```hcl
datacenter  = "dc1"
data_dir    = "/opt/consul"
bind_addr   = "10.0.0.11"
client_addr = "127.0.0.1"
log_level   = "INFO"
```

Gotchas: time values are strings with a unit (ns, us, ms, s, m, h; for example `"30s"` or `"2h45m"`), and an invalid duration string makes the agent fail to start with an error message. `bind_addr` is the address for internal cluster communications and defaults to 0.0.0.0; `client_addr` is where client interfaces (HTTP, DNS and so on) bind and defaults to 127.0.0.1, loopback only. `data_dir` is required for every agent and must be durable across reboots. TLS settings nest under `tls.defaults` with per-interface overrides in `tls.internal_rpc`, `tls.https` and `tls.grpc`.

Verify: `consul validate /etc/consul.d` prints "Configuration is valid!" and returns 0 (1 if there are problems); give it the complete set of files the agent will load, because it cannot validate partial fragments.

## Checked

2026-11-03. Confirmed against the Consul docs pages: agent configuration file reference (HCL/JSON, time values and units, invalid duration fails startup, tls.defaults and per-interface overrides), general options (bind_addr, client_addr default 127.0.0.1, data_dir required and durable) and the consul validate command page (output, exit codes, complete file set). Removed: lexical merge order, advertise_addr role and NAT advice, the consul members check and the version-control advice, none of which a fetched page states.

Method: documentation only; no commands were run.
