---
id: computing-software.systems-network-administration.apache-guacamole.ksm-vault
name: ksm-vault
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, vault, keeper-secrets-manager, ksm, ksm-config, ksm-token-mapping, secrets, keeper-notation, credential-injection]
level: advanced
status: docs-checked
description: "Pull connection secrets from Keeper Secrets Manager into Guacamole: ksm-config, ksm-token-mapping.yml, automatic KEEPER_ tokens, guacamole.properties.ksm and vault precedence."
sources:
  - https://guacamole.apache.org/doc/gug/vault.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vault integration (Keeper Secrets Manager)

KSM is the only vault the manual lists as currently supported. Install: `ksm/guacamole-vault-ksm-1.6.0.jar` from `guacamole-vault-1.6.0.tar.gz` into `GUACAMOLE_HOME/extensions/`; restart Tomcat. Docker: `KSM_ENABLED=true`.

Register:
1. In KSM create a shared folder holding the secrets Guacamole may see.
2. Create an application, assign the folder, keep read-only.
3. Generate a one-time token and convert it: `./ksm init default <one-time-token>`.
4. Put the base64 output in `ksm-config` (Docker `KSM_CONFIG`).

Manual mapping: `GUACAMOLE_HOME/ksm-token-mapping.yml`
```yaml
WINDOWS_ADMIN_PASSWORD: keeper://<RECORD_UID>/field/password
LINUX_SERVER_KEY: keeper://<RECORD_UID>/file/idrsa.pem
```
Use `${WINDOWS_ADMIN_PASSWORD}` in connection parameters. References may contain tokens such as `${USERNAME}` or `${CONNECTION_HOSTNAME}` (URL-encoded on substitution).

Automatic tokens: `${KEEPER_<CRITERIA>_<SECRET>}`
- Criteria: `USER` (username param), `SERVER` (hostname), `GATEWAY`, `GATEWAY_USER` (RDP gateway)
- Secret: `USERNAME`, `DOMAIN`, `PASSWORD`, `KEY`, `PASSPHRASE`
Only used when exactly one record matches; not for balancing groups.

Vault-backed properties: `guacamole.properties.ksm` with `keeper://` values, e.g. `mysql-password: keeper://<RECORD_UID>/field/password`.

Optional: `ksm-allow-user-config`, `ksm-allow-unverified-cert` (testing only), `ksm-api-call-interval` (ms), `ksm-strip-windows-domains` (false).

Precedence: application-wide vault, then connection group, then user vault.

Verify: a connection using `${KEEPER_USER_PASSWORD}` logs in without a stored password.

## Checked

2026-11-04. Confirmed against the Guacamole manual page vault: KSM as the supported vault, extension jar and install location, KSM_ENABLED and KSM_CONFIG, the KSM application and one-time token steps with ksm init, ksm-token-mapping.yml format, automatic KEEPER_ tokens with USER, SERVER, GATEWAY, GATEWAY_USER and the five secret types, unique-record and balancing-group limits, guacamole.properties.ksm, the optional ksm-* properties, and the vault priority order. Reworded: the claim that KSM is the only vault now matches the manual wording (currently supported).

Method: documentation only; no commands were run.
