---
id: computing-software.devops-ci-cd.rundeck.vault-key-storage-plugin
name: vault-key-storage-plugin
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, hashicorp-vault, vault-storage, key-storage-backend, approle]
level: advanced
status: docs-checked
description: "Store Rundeck Key Storage data in HashiCorp Vault with the vault-storage provider: install the plugin, rundeck-config.properties settings, auth backends and TLS options."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/manual/key-storage/storage-plugins/vault.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Install: Enterprise bundles the plugin. Community: build it with `./gradlew clean build`, drop `rundeck-vault-plugin-<version>.jar` into `libext/`, restart.

Config in `rundeck-config.properties` (restart required). For an existing Vault, the page recommends removing Rundeck's default `keys` storage path first:

```properties
rundeck.storage.provider.1.type=vault-storage
rundeck.storage.provider.1.path=keys
rundeck.storage.provider.1.config.prefix=someprefix
rundeck.storage.provider.1.config.secretBackend=mybackend
rundeck.storage.provider.1.config.address=https://vaulturl.site
rundeck.storage.provider.1.config.token=tokenvalue
rundeck.storage.provider.1.config.storageBehaviour=vault
```

Auth: `config.authBackend` defaults to `token`; allowed `approle`, `cert`, `github`, `token`, `userpass`. Matching keys: `token`; `username` and `password`; `approleId`, `approleSecretId`, `approleAuthMount`; `githubToken`; `certAuthMount` (default `cert`).

TLS has two independent parts, each either JKS or PEM:
- client cert for `authBackend=cert`: `keyStoreFile` plus `keyStoreFilePassword`, or `clientPemFile` plus `clientKeyPemFile` (unencrypted key)
- server trust: `trustStoreFile` plus `trustStoreFilePassword`, or `pemFile`

Production cert auth typically needs both.

Enterprise Namespace: leave blank or `root/` for root.

## Checked

2026-11-04: install steps, quick-start properties, auth backend values and keys, certAuthMount default, TLS options and namespace note confirmed against the Vault Key Storage plugin page. Removed the unsourced Verify line.
Method: documentation only; no commands were run.
