---
id: computing-software.cloud-infrastructure-engineering.openbao.auto-unseal-and-recovery-keys
name: auto-unseal-and-recovery-keys
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, auto-unseal, recovery-keys, rotate-keys, kms]
level: advanced
status: docs-checked
description: "OpenBao auto-unseal dependency risk, recovery key init flags, delayed recovery shares and rotating unseal or recovery keys."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/concepts/seal.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Auto-unseal and recovery keys

With auto-unseal a trusted device or service (cloud KMS, HSM) protects the unseal key; OpenBao asks it to decrypt the root key at startup. Init then yields **recovery keys**, not unseal keys.

- Recovery keys authorize sensitive operations such as generating a root token. They cannot unseal a node alone.
- After an API seal, re-unsealing uses recovery key shares.

## Init flags

`recovery-shares`, `recovery-threshold`, `recovery-pgp-keys` (API: `recovery_shares`, `recovery_threshold`, `recovery_pgp_keys`). Setting `recovery_shares=0` in `sys/init` delays generation; create them later through the `sys/rotate/recovery` endpoints, which need root or `sudo`.

## Rotation

```
bao operator rotate-keys
bao operator rotate-keys -target=recovery
```

The first rotates the unseal key; `-target=recovery` rotates recovery keys and can change share counts or PGP recipients. Both are authorized by a threshold of recovery keys.

## Warning

Auto-unseal is a strict dependency. If the KMS key becomes unavailable or is permanently deleted, the cluster cannot be recovered, even from backups. Restrict who can manage the seal, for example with AWS Service Control Policies.

## Checked

2026-11-04. Confirmed against the Seal/Unseal concepts page: auto-unseal delegation, recovery keys as authorization only, recovery-shares, recovery-threshold and recovery-pgp-keys, recovery_shares=0 delayed generation with sys/rotate/recovery needing root or sudo, rotate-keys and -target=recovery, and the strict dependency warning with AWS Service Control Policies. Nothing removed.

Method: documentation only; no commands were run.
