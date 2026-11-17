---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-raft-integrated-storage
name: vault-raft-integrated-storage
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, raft-storage, integrated-storage, retry-join]
level: practitioner
status: docs-checked
description: "Set up Vault integrated storage with path, node_id, cluster_addr and retry_join, avoiding ha_storage conflicts and mlock mistakes."
sources: ["https://developer.hashicorp.com/vault/docs/configuration/storage/raft", "https://developer.hashicorp.com/vault/docs/concepts/ha"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Integrated storage keeps data on each node's disk and replicates with Raft, removing the external backend.

```hcl
storage "raft" {
  path    = "/opt/vault/data"
  node_id = "vault-0"
  retry_join {
    leader_api_addr = "https://vault-1.example.com:8200"
    leader_ca_cert_file = "/etc/vault.d/tls/ca.pem"
  }
  retry_join {
    leader_api_addr = "https://vault-2.example.com:8200"
  }
}
cluster_addr = "https://vault-0.example.com:8201"
```

Gotchas: `cluster_addr` is required and a separate `ha_storage` cannot be declared alongside Raft. With a Shamir seal, nodes joined through `retry_join` still need manual unsealing. A `retry_join` stanza takes either `leader_api_addr` or `auto_join`, not both, and certificates must be all file paths or all inline. Set `node_id` explicitly; otherwise it is a random GUID in `data/node-id`. `max_entry_size` defaults to 1 MiB.

`vault operator raft list-peers` returns the Raft peer set.

## Checked

2026-11-03. Confirmed against the Vault Raft storage configuration page and the `vault operator raft` command page (developer.hashicorp.com): parameters, defaults, constraints and examples. Removed: the SSD advice, the migration remark, the Verify claims about leader and HA Mode, and the full-disk paragraph (not on the pages).

Method: documentation only; no commands were run.
