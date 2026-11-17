---
id: computing-software.cloud-infrastructure-engineering.longhorn.volume-encryption
name: volume-encryption
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [encryption, luks, cryptsetup, secret, storageclass]
level: advanced
status: docs-checked
description: "Encrypt Longhorn volumes with LUKS: dm_crypt and cryptsetup prerequisites, the crypto Secret keys, defaults and StorageClass node secrets."
sources:
  - https://longhorn.io/docs/1.13.0/advanced-resources/security/volume-encryption/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: create encrypted PVCs.

Prerequisites: load the `dm_crypt` kernel module and install `cryptsetup` on every worker node that can run an encrypted volume.

Secret keys:
- `CRYPTO_KEY_VALUE`: the passphrase
- `CRYPTO_KEY_CIPHER`: default `aes-xts-plain64`
- `CRYPTO_KEY_HASH`: default `sha256`
- `CRYPTO_KEY_SIZE`: default `256` bits
- `CRYPTO_PBKDF`: default `argon2i`
- `CRYPTO_PBKDF_FORCE_ITERATIONS`: Longhorn default `200000`
- `CRYPTO_PBKDF_MEMORY`: default `0`, ignored with PBKDF2

```yaml
stringData:
  CRYPTO_KEY_VALUE: "Your encryption passphrase"
```

StorageClass: set `encrypted: "true"` and reference the Secret from the node-side parameters, which are required: `csi.storage.k8s.io/node-stage-secret-name` and `-namespace`, `csi.storage.k8s.io/node-publish-secret-name` and `-namespace`, `csi.storage.k8s.io/node-expand-secret-name` and `-namespace`.

```yaml
csi.storage.k8s.io/node-stage-secret-name: "longhorn-crypto"
csi.storage.k8s.io/node-stage-secret-namespace: "longhorn-system"
```

Provisioner-side `csi.storage.k8s.io/provisioner-secret-*` parameters are treated as historical. `longhorn-csi-service-account` has a cluster-wide `get` grant on Secrets by default; Helm users can disable it with `csi.allowControllerSecretAccess=false`, but first remove historical provisioner-side parameters from StorageClasses or provisioning can fail. Node-side references must stay.

## Checked

2026-11-08. Read in full against https://longhorn.io/docs/1.13.0/advanced-resources/security/volume-encryption/ : requirements, Secret keys and defaults, StorageClass node-side parameters, service account Secret grant and the Helm opt-out. Nothing else was removed.

Method: documentation only; no commands were run.
