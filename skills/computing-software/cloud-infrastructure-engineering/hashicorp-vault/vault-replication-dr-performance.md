---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-replication-dr-performance
name: vault-replication-dr-performance
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, vault-replication, dr-replication, performance-replication]
level: practitioner
status: docs-checked
description: "Know the differences between Vault Enterprise performance and DR replication, what replicates, and the DR enable, token and promote API calls."
sources: ["https://developer.hashicorp.com/vault/docs/enterprise/replication", "https://developer.hashicorp.com/vault/api-docs/system/replication/replication-dr"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Replication is a Vault Enterprise feature.

- DR replication: a warm standby that mirrors configuration, tokens and leases from the primary. A DR secondary can be promoted with minimal disruption if the primary is lost.
- Performance replication: secondaries serve client requests locally and manage their own tokens and leases.
- Local mounts (including audit devices) are not visible to performance secondaries but are replicated to DR secondaries.

DR setup API calls:

```sh
# on the primary
vault write -f sys/replication/dr/primary/enable
vault write sys/replication/dr/primary/secondary-token id=dr-secondary
# on the secondary
vault write sys/replication/dr/secondary/enable token=<activation token>
# to promote the secondary
vault write sys/replication/dr/secondary/promote dr_operation_token=<token>
```

- `secondary-token` requires `id`; the token `ttl` defaults to 30m.
- `secondary/enable` requires `token`; `secondary/promote` requires `dr_operation_token`.
- Replication status reports `state: stream-wals` when streaming.

## Checked
2026-11-03. Confirmed on the replication overview and DR API pages (Enterprise, DR and performance behaviour, local mounts, `primary/enable`, `secondary-token` `id` and 30m default, `secondary/enable`, `secondary/promote`, `stream-wals`). Removed: claims that DR secondaries serve no requests or write no audit logs until promoted, game-day, DNS and load-balancer advice, and pre-generating the DR operation token.
Method: documentation only; no commands were run.
