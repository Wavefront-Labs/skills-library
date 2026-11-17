---
id: computing-software.database-administration.elasticsearch.secure-settings-with-elasticsearch-keystore
name: secure-settings-with-elasticsearch-keystore
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, elasticsearch-setup, elasticsearch-keystore, secure-settings, reload-secure-settings, snapshot-credentials]
level: practitioner
status: docs-checked
description: "Store Elasticsearch secrets (S3 keys, TLS keystore passwords, LDAP bind) in elasticsearch-keystore, keep it identical across nodes, and reload reloadable settings live."
sources:
  - https://github.com/elastic/elasticsearch/blob/main/docs/reference/elasticsearch/command-line-tools/elasticsearch-keystore.md
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/security/secure-settings.md
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/deploy/self-managed/_snippets/systemd.md
  - https://github.com/elastic/elasticsearch/blob/main/docs/reference/elasticsearch/configuration-reference/s3-repository-settings.md
  - https://github.com/elastic/elasticsearch/blob/main/docs/reference/elasticsearch/configuration-reference/azure-repository-settings.md
  - https://github.com/elastic/elasticsearch/blob/main/docs/reference/elasticsearch/configuration-reference/gcs-repository-settings.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secure settings with elasticsearch-keystore

Sensitive settings must not go in `elasticsearch.yml`; they live in the per-node
`config/elasticsearch.keystore`, managed with the `elasticsearch-keystore` tool.

## Commands (run as the elasticsearch user, in ES_HOME or with ES_PATH_CONF set)
```bash
bin/elasticsearch-keystore list
bin/elasticsearch-keystore add s3.client.default.access_key
bin/elasticsearch-keystore add s3.client.default.secret_key
echo -n "$PW" | bin/elasticsearch-keystore add --stdin xpack.security.http.ssl.keystore.secure_password
bin/elasticsearch-keystore add-file gcs.client.default.credentials_file /tmp/gcs-sa.json
bin/elasticsearch-keystore remove s3.client.default.access_key
bin/elasticsearch-keystore show s3.client.default.access_key   # prints one setting's value
bin/elasticsearch-keystore passwd                         # password-protect the keystore
bin/elasticsearch-keystore has-passwd
```
A password-protected keystore needs the password at startup: a prompt when run interactively, or for systemd a protected file referenced by `ES_KEYSTORE_PASSPHRASE_FILE` (set with `systemctl set-environment`; the file may be deleted once Elasticsearch has started).

## Typical secure settings
- Snapshot repositories: `s3.client.<name>.access_key/secret_key`, `azure.client.<name>.key`,
  `gcs.client.<name>.credentials_file`.
- TLS: `xpack.security.transport.ssl.keystore.secure_password`,
  `xpack.security.http.ssl.truststore.secure_password` (the `ssl.*.secure_password` forms are preferred over the plain-text `password` settings).
- LDAP/AD realm bind password: `xpack.security.authc.realms.ldap.ldap1.secure_bind_password`.
- Only settings marked *Secure* in the configuration reference can be added to the keystore; the reference also marks which are *Reloadable*.

## Same on every node
Each node has its own keystore file; settings must be **added on every node** (config
management, or build images with the keystore). Mismatched values (e.g. a different S3 key on
one node) cause hard-to-trace failures such as snapshots failing only on some shards.

## Reloading without restart
Most secure settings take effect only after a restart. Settings marked **reloadable** (for example the S3, Azure and GCS repository client credentials; the docs also name watcher, monitoring and some realms) can be refreshed live. After changing them on every node, call the API once:
```
POST _nodes/reload_secure_settings
{ "secure_settings_password": "<keystore password if set>" }
```
The API re-reads the whole keystore but applies only reloadable settings; others need a node restart (a rolling restart). Configure secure settings before the `elasticsearch.yml` settings that need them.

## Gotchas
- Docker: mount secrets as files and use `add-file`; avoid baking secrets into images.
- `elasticsearch-keystore upgrade` upgrades the keystore's internal format; Elasticsearch also attempts this when you upgrade, but a bind-mounted keystore file is read-only and cannot be upgraded automatically. Back it up first.

## Verify
`elasticsearch-keystore list` shows the same entries on every node; after
`reload_secure_settings` the response reports no `reload_exception`, and
`POST _snapshot/<repo>/_verify` succeeds on all nodes.

## Checked

Checked 2026-10-25 against elastic/elasticsearch and elastic/docs-content `main` (Stack 9.x docs). Confirmed: keystore subcommands (`add`, `add-file`, `--stdin`, `remove`, `list`, `show`, `passwd`, `has-passwd`, `upgrade`); per-node keystore with identical values on every node; most settings need a restart, reloadable ones use `POST _nodes/reload_secure_settings` (with `secure_settings_password` if protected); `ES_KEYSTORE_PASSPHRASE_FILE` for systemd; setting names for S3 (`access_key`, `secret_key`), Azure (`key`), GCS (`credentials_file`) and the LDAP `secure_bind_password`. Removed unconfirmed claims: the `bootstrap.password` and Watcher entries, auto-creation of TLS passwords in 8.x, ECK `secureSettings`, and the 660 permission advice. The `_snapshot/<repo>/_verify` endpoint in Verify was not re-read.

Method: documentation only; no commands were run.
