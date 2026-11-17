---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-acl-policies-and-rules
name: consul-acl-policies-and-rules
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, acl-policies, acl-rules, consul-policy]
level: practitioner
status: docs-checked
description: "Author Consul ACL policies granting read, write or deny on services, keys and nodes, using exact and prefix matching."
sources: ["https://developer.hashicorp.com/consul/docs/reference/acl/policy", "https://developer.hashicorp.com/consul/docs/reference/acl/rule", "https://developer.hashicorp.com/consul/commands/acl/policy/create"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A policy is a set of rules over resources. Labelled resources come in an exact form and a `_prefix` form: `service`/`service_prefix`, `key`/`key_prefix`, `node`/`node_prefix`, `agent`/`agent_prefix`, `session`/`session_prefix`, `query`/`query_prefix`, `event`/`event_prefix`. `acl`, `keyring`, `mesh` and `operator` take no label and are written `operator = "read"`. Dispositions are `read`, `write` and `deny`. The special `list` disposition works only on `key_prefix` and needs `acl.enable_key_list_policy = true` on the agents.

```hcl
service_prefix "web-" { policy = "write" }
service_prefix ""     { policy = "read" }
node_prefix ""        { policy = "read" }
key_prefix "config/web/" { policy = "read" }
```

```sh
consul acl policy create -name web-team -rules @web-team.hcl
consul acl policy read -name web-team
```

Gotchas:
- Exact labels (`service "web-prod"`) match only that name. With prefix rules, the most specific prefix match decides. Where rules tie on the same exact resource, the order of precedence is `deny`, then `write`, then `read`.
- An empty prefix (`service_prefix ""`) applies to every resource of that type, which is easy to grant by accident. `service ""` is an exact match on an empty name, not "all services".
- A policy has no effect until it is linked to a token or role (see `consul-acl-tokens-and-roles`).
- A `write` rule on `key_prefix` also gives `list`; `list` also gives `read` on all suffixes.
- Agents need `write` on their own node name (via `acl.tokens.agent`) to register node metadata; registering a service needs `service:write` on that service's name.

## Checked

2026-11-03. Confirmed against the Consul v1.22 docs source: reference/acl/policy (labels, dispositions, prefix matching, precedence), reference/acl/rule (resource table, key list rules, node and service registration), reference/agent/configuration-file/acl (`enable_key_list_policy`), commands/acl/policy/create (`-name`, `-rules @file`). Fixed: `service ""` was written as if it matched all services, `session`/`query`/`operator` dispositions were listed loosely, and `list` was missing its prerequisite. Removed: the claim that DNS and mesh need read on other services, and the invented Verify step.
Method: documentation only; no commands were run.
