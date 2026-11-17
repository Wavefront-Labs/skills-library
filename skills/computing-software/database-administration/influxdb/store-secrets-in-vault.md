---
id: computing-software.database-administration.influxdb.store-secrets-in-vault
name: store-secrets-in-vault
category: computing-software
field: database-administration
product: influxdb
tags: [secrets, vault, secret-store, kv-v2, influxd]
level: advanced
status: docs-checked
description: "Switch InfluxDB OSS to a HashiCorp Vault secret store using --secret-store vault, --vault-addr and --vault-token; only KV v2 is supported."
sources:
  - https://docs.influxdata.com/influxdb/v2/admin/secrets/use-vault/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Steps from the docs: start a Vault server reachable from InfluxDB, give InfluxDB the Vault address and token, start `influxd` with the vault secret store, then manage secrets through the InfluxDB API.

- Only the Vault KV Secrets Engine version 2 API is supported. Enable it with `vault secrets enable kv-v2`.
- Provide the address with `--vault-addr` or `VAULT_ADDR`, and the token with `--vault-token` or `VAULT_TOKEN`. Your Vault may require other Vault settings.
- Start with the secret store option:

```sh
influxd --secret-store vault \
  --vault-addr=http://127.0.0.1:8200 \
  --vault-token=$VAULT_TOKEN
```

(Adapt the address to your Vault server.) Other `influxd` Vault options, which override the Vault environment variables, are `--vault-cacert`, `--vault-capath`, `--vault-client-cert`, `--vault-client-key`, `--vault-max-retries`, `--vault-client-timeout`, `--vault-skip-verify` and `--vault-tls-server-name`.

For local trials the docs use `vault server -dev`; they link to the Vault docs for installing and deploying Vault in development and production.

## Checked

Method: docs-checked 2026-11-09 against the InfluxDB v2 "Store secrets in Vault" page, article body (lines 574-630) read from the downloaded text.

Replaced: the `service influxdb start` example with the page's `influxd --secret-store vault` command. Removed the unconfirmed "production should use a real Vault" wording.
