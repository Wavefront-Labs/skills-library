---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-shamir-unseal
name: vault-shamir-unseal
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, shamir-unseal, vault-unseal, seal-status]
level: practitioner
status: docs-checked
description: "Unseal Vault nodes with vault operator unseal using a threshold of key shares, per node, and reseal in an emergency."
sources: ["https://developer.hashicorp.com/vault/docs/concepts/seal"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A sealed Vault can reach storage but cannot decrypt it; only unseal and status calls work. Each node needs its own threshold of shares, supplied by different people if you want split custody.

```sh
vault operator unseal      # prompts for a share; repeat until threshold met
vault status
vault operator seal        # emergency: drops the root key from memory
```

The process is stateful, so shares may be entered from different machines. A node stays unsealed until sealed, restarted or hit by an unrecoverable storage error.

Gotchas: restarts (including patching and autoscaling replacements) re-seal Shamir nodes, so a manual unseal step is a recurring operational dependency and an availability risk; consider auto unseal for production. Shares typed on the CLI can end up in shell history; use the interactive prompt, not arguments. After `vault operator seal`, unsealing needs the shares again, and that is the intended response to a suspected intrusion.

## Checked

2026-11-03. Confirmed against the Vault seal concepts page (only unseal and status operations before unsealing, stateful unseal process, each node needs the threshold, API seal remains sealed until restart or unseal) and the `operator unseal` and `operator seal` command pages (shares in shell history, in-memory root key discarded). Removed: an invented verify step.

Method: documentation only; no commands were run.
