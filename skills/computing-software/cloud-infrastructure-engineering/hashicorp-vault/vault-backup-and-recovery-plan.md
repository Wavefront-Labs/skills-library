---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-backup-and-recovery-plan
name: vault-backup-and-recovery-plan
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, vault-recovery-plan, rto-rpo, recovery-keys]
level: practitioner
status: docs-checked
description: "Combine Raft snapshots, key custody, KMS key protection, and rehearsals into a documented Vault recovery plan with RTO and RPO."
sources: ["https://developer.hashicorp.com/vault/docs/commands/operator/raft", "https://developer.hashicorp.com/vault/docs/concepts/seal"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A snapshot alone does not recover a cluster; you also need the means to unseal it.

```sh
vault operator raft snapshot save /backup/vault-$(date +%F-%H%M).snap
sha256sum /backup/vault-*.snap | tee -a /backup/SHA256SUMS
# Drill: new empty cluster, same seal config, then
vault operator raft snapshot restore -force /backup/<snapshot>.snap
```

Record: who holds unseal or recovery keys, where the auto-unseal KMS key lives and how its deletion is prevented, how to regenerate a root token, and what DNS or load balancer change redirects clients. Define RPO from snapshot frequency and RTO from rehearsal timings.

Gotchas: restoring needs the same unseal keys or KMS key as the snapshot; a different one leaves data unreadable. Snapshots hold secrets and must be encrypted and access-logged. If the seal mechanism or its keys are permanently deleted, the cluster cannot be recovered even from backups, so control access to the seal key. Run restore drills in an isolated network so the test instance cannot revoke live third-party credentials.

## Checked

2026-11-03. Confirmed against the Vault "Restore a snapshot" page (original unseal keys needed, `-force`, isolation), the seal concepts page (loss of seal keys is unrecoverable) and the `operator raft` command page (`snapshot save` and `restore`; no snapshots for HA-only Raft). Removed: snapshot contents and version-compatibility claims, a quarterly rehearsal rule and an invented verify step.

Method: documentation only; no commands were run.
