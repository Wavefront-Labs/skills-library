---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-server-config-hcl
name: vault-server-config-hcl
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, vault-server-config, vault-hcl, api-addr]
level: practitioner
status: docs-checked
description: "Compose a Vault HCL config with listener, Raft storage, api_addr, cluster_addr, UI and disable_mlock, and know what each address is for."
sources: ["https://developer.hashicorp.com/vault/docs/configuration", "https://developer.hashicorp.com/vault/docs/configuration/listener/tcp", "https://developer.hashicorp.com/vault/docs/configuration/storage/raft", "https://developer.hashicorp.com/vault/docs/concepts/ha"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A server config with a listener, integrated (Raft) storage, advertised addresses and the UI.

```hcl
ui            = true
disable_mlock = true
api_addr      = "https://vault-0.example.com:8200"
cluster_addr  = "https://vault-0.example.com:8201"

listener "tcp" {
  address       = "0.0.0.0:8200"
  tls_cert_file = "/etc/vault.d/tls/tls.crt"
  tls_key_file  = "/etc/vault.d/tls/tls.key"
}

storage "raft" {
  path    = "/opt/vault/data"
  node_id = "vault-0"
}
```

- `api_addr` is a full URL including the scheme, not just IP and port. It is the address standbys give clients for redirection. With direct client access each node uses its own address; behind a load balancer all nodes use the load balancer address (the HA page calls that setup prone to redirect loops and not recommended when avoidable). It can also be set with `VAULT_API_ADDR`, which takes precedence.
- `cluster_addr` is the address a node advertises to standbys for request forwarding; Vault ignores its scheme (cluster traffic always uses TLS). The Raft storage page says you must provide `cluster_addr`. Env var `VAULT_CLUSTER_ADDR` takes precedence.
- `disable_mlock` needs an explicit value with integrated storage. Disabling mlock is not recommended unless the host uses encrypted swap or no swap, so disable swap.
- `node_id` can be overridden by `VAULT_RAFT_NODE_ID`; unset, Vault assigns a random GUID at initialization and writes it to `data/node-id` under the storage `path`.
- `ui = true` enables the built-in UI on all listeners at `/ui`.
- On `SIGHUP` Vault updates the log level; some other settings (for example `enable_post_unseal_trace`) are also marked as updatable that way. Do not assume other settings reload.

## Checked
2026-11-03. Confirmed on the configuration page (`ui`, `disable_mlock`, `api_addr`, `cluster_addr`, SIGHUP log level), the Raft storage page (`cluster_addr` required, `node_id`, swap) and the HA concepts page (`api_addr` full URL, load balancer caveat, env vars). Removed: "seal" as a required element (not in the example), TLS-file reload on SIGHUP, file-permission advice, the `vault status` Verify step with a journal message, and the closing advice on templating configs across nodes.
Method: documentation only; no commands were run.
