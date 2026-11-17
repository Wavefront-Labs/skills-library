---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-agent-tokens
name: consul-agent-tokens
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, agent-tokens, acl-tokens-agent, node-identity]
level: practitioner
status: docs-checked
description: "Set agent, default, dns and replication tokens on Consul agents with acl.tokens or consul acl set-agent-token, using node identities."
sources: ["https://developer.hashicorp.com/consul/docs/secure/acl/bootstrap", "https://developer.hashicorp.com/consul/commands/acl/set-agent-token", "https://developer.hashicorp.com/consul/docs/reference/agent/configuration-file/acl"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Every server and client agent needs a token. Create one per agent with a node identity, which grants the privileges to register a node by that name and read any service in the catalog.

```sh
consul acl token create -description "web-01 agent token" -node-identity "web-01:dc1"
```

Apply it in the agent config (recommended, so a restart reloads it) and run `consul reload`:

```hcl
acl {
  tokens {
    agent = "<agent-token-secret>"
  }
}
```

Or set it at runtime with a token that has `acl:write`:

```sh
consul acl set-agent-token agent "<agent-token-secret>"
```

Token types for `set-agent-token`: `agent`, `dns`, `config_file_service_registration`, `replication`, `recovery`, `default`.

Gotchas:
- Tokens set at runtime persist across restarts only if `acl.enable_token_persistence = true`.
- `agent` falls back to `default` if unset. `default` is used for requests with no token (and the anonymous token if `default` is unset), so keep it minimal. `dns` falls back to `default`; the docs strongly recommend a dedicated `dns` token built from the DNS templated policy.
- Apply the agent token to servers and confirm they work before applying it to clients.
- `config_file_service_registration` registers services and checks defined in config files and needs `service:write` on each; a `token` field on a service or check definition overrides it.
- `replication` is required on servers outside the primary datacenter when ACLs are enabled.

## Checked

2026-11-03. Confirmed against the Consul v1.22 docs source: secure/acl/bootstrap (node identity, config file and CLI methods, order of rollout), commands/acl/set-agent-token (token types, required `acl:write`, persistence), reference/agent/configuration-file/acl (`tokens.agent`, `default`, `dns`, `replication`, `config_file_service_registration`). Removed: the file mode advice, the log-line Verify step, and the node-identity Verify claim.
Method: documentation only; no commands were run.
