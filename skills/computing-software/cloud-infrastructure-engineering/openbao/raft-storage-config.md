---
id: computing-software.cloud-infrastructure-engineering.openbao.raft-storage-config
name: raft-storage-config
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, raft, storage, node-id, retry-join]
level: practitioner
status: docs-checked
description: "Configure storage raft in OpenBao: path, node_id, performance_multiplier, snapshot and log settings, entry limits and retry_join stanzas."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/configuration/storage/raft.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# storage "raft"

```hcl
storage "raft" {
  path    = "/path/to/data"
  node_id = "node1"
  retry_join {
    leader_api_addr = "https://example.com:8200"
  }
}
cluster_addr = "https://node1.example.com:8201"
```

## Parameters and defaults

- `path`, `node_id`: env `BAO_RAFT_PATH`, `BAO_RAFT_NODE_ID` override
- `performance_multiplier`: 0 means minimal-server timing (equivalent to 5); 1 is highest performance and recommended for production; max 10
- `trailing_logs` 10000; `snapshot_threshold` 8192; `snapshot_interval` 120 (seconds, randomised up to 2x)
- `max_entry_size` 1048576 (larger Puts fail); `max_transaction_size` 8388608
- `retry_join_as_non_voter` false (env `BAO_RAFT_RETRY_JOIN_AS_NON_VOTER`)
- `autopilot_reconcile_interval` `"10s"`, `autopilot_update_interval` `"2s"`

## retry_join keys

`leader_api_addr`, `auto_join` (go-discover syntax), `auto_join_scheme`, `auto_join_port`, `leader_tls_servername`, and either file keys (`leader_ca_cert_file`, `leader_client_cert_file`, `leader_client_key_file`) or inline (`leader_ca_cert`, `leader_client_cert`, `leader_client_key`).

## Rules

- `cluster_addr` is required.
- A separate `ha_storage` cannot be declared with Integrated Storage.
- Each `retry_join` uses file paths or inline values, not both; and `leader_api_addr` or `auto_join`, not both.

## Checked

2026-11-04. Read the OpenBao Integrated Storage (Raft) configuration page in full. Confirmed: every parameter, default and environment variable listed, the `performance_multiplier` semantics and maximum of 10, `snapshot_interval` staggering, entry and transaction sizes, the `retry_join` keys and exclusivity rules, `cluster_addr` requirement and the `ha_storage` restriction. Removed: nothing.
Method: documentation only; no commands were run.
