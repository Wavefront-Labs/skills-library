---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-raft-autopilot
name: vault-raft-autopilot
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, vault-autopilot, dead-server-cleanup, min-quorum]
level: practitioner
status: docs-checked
description: "Configure Vault Autopilot dead-server cleanup, thresholds and min-quorum, avoiding accidental removal of healthy nodes."
sources: ["https://developer.hashicorp.com/vault/docs/commands/operator/raft"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Autopilot manages Raft membership health for integrated storage.

```sh
vault operator raft autopilot get-config
vault operator raft autopilot set-config \
  -cleanup-dead-servers=true -dead-server-last-contact-threshold=24h \
  -min-quorum=3 -server-stabilization-time=10s
vault operator raft autopilot state
```

Gotchas: keep `dead-server-last-contact-threshold` high (a day is suggested), since low values can remove a node that is only temporarily partitioned and then require rejoin with wiped data. `min-quorum` has no default; set it whenever cleanup is enabled so Autopilot never shrinks below a safe voter count. A new node's dead-server threshold must exceed the time it takes to load a Raft snapshot, or the node may be removed before it finishes starting. Enterprise adds redundancy zones and automated upgrades.

`autopilot state` shows `Healthy`, `Failure Tolerance`, the voters and each server's status.

## Checked

2026-11-03. Confirmed against the Vault `operator raft` command page: `autopilot get-config`, `set-config` and `state`, and the flags `cleanup-dead-servers` (requires `min-quorum`), `dead-server-last-contact-threshold` (default 24h, keep high), `min-quorum` (no default), `server-stabilization-time` (default 10s). Removed: maintenance-window claim, an invented verify procedure and an alerting tip.

Method: documentation only; no commands were run.
