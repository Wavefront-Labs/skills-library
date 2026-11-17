---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.securityadmin-config-update
name: securityadmin-config-update
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, securityadmin-config-update]
level: advanced
status: docs-checked
description: "Apply OpenSearch Security plugin YAML changes (roles, mappings, internal users, config) with securityadmin.sh, an admin certificate and a backup first."
sources:
  - https://docs.opensearch.org/latest/security/configuration/security-admin/
  - https://docs.opensearch.org/latest/security/configuration/tls/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Update security config with securityadmin (OpenSearch)

**Goal:** load Security plugin configuration into the `.opendistro_security` index.
- Edits to files in `config/opensearch-security` are not applied automatically; run `plugins/opensearch-security/tools/securityadmin.sh` (`.bat` on Windows).
- Prerequisite: `plugins.security.ssl.http.enabled: true` in `opensearch.yml` (the script needs HTTP TLS).
- Admin certificate: list its DN under `plugins.security.authcz.admin_dn` (no wildcards or regex, no whitespace between DN parts). Node certificates cannot double as admin certificates.
- Load everything: `./securityadmin.sh -cd <CONFIG_DIR> -icl -nhnv -cacert <CA> -cert <ADMIN_CERT> -key <ADMIN_KEY>`. `-cd` is the config directory, `-icl` ignores the cluster name, `-nhnv` disables hostname verification, `-key` must be PKCS#8 (`-keypass` for a key password).
- Load one file: `-f <file> -t <type>` instead of `-cd`; types are `config`, `roles`, `rolesmapping`, `internalusers`, `actiongroups`. `-f` cannot be combined with `-cd`.
- Keystore form: `-ks <keystore> -kspass <pw> -ts <truststore> -tspass <pw>` (JKS or PKCS#12/PFX; `-kst`/`-tst` set the type).
- `-rev` resolves environment variables such as `${env.LDAP_PASSWORD}` before applying.
- `-rl` reloads the configuration and flushes the user and permission cache (cached for one hour by default).
- Defaults: host `localhost`, port 9200, cluster name `opensearch`; it refuses a red cluster unless `-arc`.
- Danger: loading a directory overwrites parts of the index, so users created through the REST API can be lost when you reload `internal_users.yml`. Back up first: `./securityadmin.sh -backup <DIR> -icl -nhnv -cacert ... -cert ... -key ...`.
- Failure mode: `-nhnv` skips hostname verification; the page uses it with self-signed demo certificates only.

## Verify
- [ ] Run `-backup` into a fresh directory and confirm the YAML files contain your change.

## Checked
Checked 2026-11-08 against the OpenSearch pages "Applying changes to configuration files" (securityadmin) and "Configuring TLS certificates" (admin_dn rules). Only OpenSearch was checked; the Elasticsearch page cited before does not apply to this plugin. Removed because not on the pages: the `hash.sh` password tool, the "demo certificates never in production" sentence, and the `GET _plugins/_security/api/roles` verify step.
Method: documentation only; no commands were run.
