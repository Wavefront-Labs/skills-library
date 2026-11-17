---
id: computing-software.cybersecurity-defensive.keycloak.vault-secret-references
name: vault-secret-references
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, vault, secrets, key-resolver, smtp-password]
level: practitioner
status: docs-checked
description: "Reference external secrets from Keycloak configuration with the vault expression and choose key resolvers that keep realms isolated."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/vault.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vault secret references
Keycloak ships two Vault SPI implementations: a plain-text file-based vault and a Java KeyStore-based vault. Instead of typing a secret, enter `${vault.key}` in the field, where `key` is the secret name recognised by the vault. Supported fields: the realm SMTP password, the LDAP bind credential (LDAP user federation settings), the Client Secret in an OpenID Connect identity provider config, and the Client Secret of a confidential OpenID Connect client.

To prevent secrets leaking across realms, Keycloak combines the realm name with `key` to build the final entry name (a filename for the file vault, an alias for the KeyStore vault). A **key resolver** defines the combination. Configure resolvers with the `keyResolvers` property, a comma-separated list; for the file provider:
```
kc.sh start --spi-vault--file--key-resolvers=REALM_UNDERSCORE_KEY,KEY_ONLY
```
Resolvers run in the declared order; the first that finds a non-empty secret wins, and if none do Keycloak returns an empty secret. Available resolvers:
- `REALM_UNDERSCORE_KEY`: realm and key joined by an underscore; underscores in realm or key are escaped with another underscore (realm `master_realm`, key `smtp_key` gives `master__realm_smtp__key`).
- `KEY_ONLY`: ignores the realm and uses the key, escaping underscores (`my_secret` becomes `my__secret`). This removes realm isolation.
- `REALM_FILESEPARATOR_KEY`: realm and key joined by the platform file separator; the expression forbids characters that could cause path traversal.

If no resolver is configured for the built-in providers, Keycloak uses `REALM_UNDERSCORE_KEY`.

## Checked
2026-11-03. Confirmed against server_admin/topics/vault.adoc: expression, fields, resolver semantics, order and default. Removed: "rotate by updating the vault" and "missing entry fails mail" gotchas, the `${vault.smtp_password}` verify walkthrough and the "confirm for your version" hedge.
Method: documentation only; no commands were run.
