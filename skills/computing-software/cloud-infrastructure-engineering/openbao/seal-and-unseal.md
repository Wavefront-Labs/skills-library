---
id: computing-software.cloud-infrastructure-engineering.openbao.seal-and-unseal
name: seal-and-unseal
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, seal, unseal, shamir, root-key]
level: practitioner
status: docs-checked
description: "How OpenBao sealing works: the key hierarchy, Shamir shares, per-node unseal, API sealing and when to avoid manual unseal."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/concepts/seal.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Seal and unseal

A new server starts sealed: it knows where storage is but cannot decrypt it. Until unsealed, only unseal and seal-status operations work.

## Key hierarchy

Data is encrypted by the encryption key (in the keyring); the keyring by the root key; the root key by the unseal key.

## Shamir (default)

The unseal key is split into shares; a threshold reconstructs it.

```
bao operator unseal
```

- Shares can be submitted one at a time, in any order, from different clients (the process is stateful).
- In a multi-node cluster every node must be unsealed separately with the threshold of shares.
- A node stays unsealed until you reseal it via the API, it restarts, or it hits an unrecoverable storage error.

## Sealing

Sealing through the API discards the root key from memory. One operator with root privileges is enough, which makes it a fast response to a suspected intrusion. Unsealing again needs the key shares.

## Gotcha

Manual Shamir unsealing is hard to automate; the docs recommend auto-unseal or static-key auto-unseal instead (see auto-unseal-and-recovery-keys).

## Checked

2026-11-04. Confirmed against the Seal/Unseal concepts page: sealed start state, key hierarchy, Shamir shares, stateful unseal in any order, per-node unsealing, the three ways a node leaves the unsealed state, API sealing by one root operator, and the recommendation of auto-unseal over manual Shamir. Nothing removed.

Method: documentation only; no commands were run.
