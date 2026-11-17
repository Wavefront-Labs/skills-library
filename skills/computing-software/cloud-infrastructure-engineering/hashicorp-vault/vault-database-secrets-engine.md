---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-database-secrets-engine
name: vault-database-secrets-engine
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, database-secrets, dynamic-secrets, database-roles]
level: practitioner
status: docs-checked
description: "Configure the Vault database secrets engine with a connection, roles and TTLs, and rotate the root credential."
sources: ["https://developer.hashicorp.com/vault/docs/secrets/databases", "https://developer.hashicorp.com/vault/api-docs/secret/databases", "https://developer.hashicorp.com/vault/docs/secrets/databases/postgresql"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The engine creates a database user per request and removes it at lease expiry.

```sh
vault secrets enable database
vault write database/config/pg plugin_name=postgresql-database-plugin \
  connection_url="postgresql://{{username}}:{{password}}@db:5432/app" \
  allowed_roles=app username=vaultadmin password=@dbpass.txt
vault write -force database/rotate-root/pg
vault write database/roles/app db_name=pg \
  creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
  default_ttl=1h max_ttl=24h
vault read database/creds/app
```

Gotchas: root credential rotation applies to all plugins except MongoDB Atlas. A root account assigned to a static role breaks every user managed through that connection once it rotates. For connection string formats that need special characters unescaped (such as ADO with MSSQL or Azure SQL), set `disable_escaping=true` (Vault 1.10 or later).

## Checked

2026-11-03. Confirmed on the database secrets engine overview, database API and PostgreSQL plugin pages: `config/:name` with `plugin_name`, `connection_url`, `allowed_roles`; `rotate-root/:name`; roles with `db_name`, `creation_statements` using `{{name}}`, `{{password}}`, `{{expiration}}` and `VALID UNTIL`, `default_ttl`, `max_ttl`; `creds/:name`; `disable_escaping` from Vault 1.10. Removed: the unconfirmed claim that only Vault knows the admin password, privilege-sizing and revoke-by-prefix advice, per-app role advice, and the invented Verify step.

Method: documentation only; no commands were run.
