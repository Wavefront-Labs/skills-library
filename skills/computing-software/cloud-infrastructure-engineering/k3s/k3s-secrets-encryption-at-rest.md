---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-secrets-encryption-at-rest
name: k3s-secrets-encryption-at-rest
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, secrets-encryption, aescbc, encryption-config]
level: practitioner
status: docs-checked
description: "Enable Kubernetes secrets encryption at rest in K3s with --secrets-encryption and inspect the generated config."
sources:
  - https://docs.k3s.io/security/secrets-encryption
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: encrypt Secrets stored in the datastore.

Start the server with the flag the first time it runs:

```
curl -sfL https://get.k3s.io | sh -s - server --secrets-encryption
```

On first start K3s automatically generates an AES-CBC key, writes an encryption config file with that key, and passes the config to the Kubernetes API server as encryption-provider-config.

The generated file is /var/lib/rancher/k3s/server/cred/encryption-config.json. With the default provider it is an EncryptionConfiguration (apiserver.config.k8s.io/v1) for resource secrets, listing an aescbc key named aescbckey followed by an identity provider.

Constraint: secrets-encryption cannot be enabled on an existing server without restarting it.


Management: the bundled `k3s secrets-encrypt` tool can disable or enable encryption, add new keys, rotate and delete keys, and reencrypt secrets. See the secrets-encrypt CLI skills.

## Checked

2026-11-08. Read the full K3s Secrets Encryption page (docs/security/secrets-encryption.md in the k3s-io/docs repo). Confirmed: the install command, the generated AES-CBC key, the encryption config passed as encryption-provider-config, the config file path and its EncryptionConfiguration content, the restart constraint, and the secrets-encrypt tool capabilities. Removed the HA same-flag note and the server token backup note (not on the page).

Method: documentation only; no commands were run.
