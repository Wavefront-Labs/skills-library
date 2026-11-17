---
id: computing-software.search-and-information-retrieval.apache-solr.enable-ssl-tls
name: enable-ssl-tls
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [ssl, tls, keystore, solr-ssl-variables, https]
level: practitioner
status: docs-checked
description: "Enable TLS for Solr: build a keystore with keytool (PKCS12, SAN entries), then set SOLR_SSL_* variables in solr.in.sh for key store, trust store, client auth and peer name."
sources:
  - https://solr.apache.org/guide/solr/latest/deployment-guide/enabling-ssl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# enable-ssl-tls

Generate a self-signed pair with the JDK `keytool`, for example `keytool -genkeypair -alias solr-ssl -keyalg RSA -keysize 2048 ... -keystore solr-ssl.keystore.p12 -storetype PKCS12 -ext SAN=DNS:localhost,IP:127.0.0.1`. The `-ext SAN=` list names every DNS name and IP allowed during hostname verification. The same keystore can act as truststore. Use `openssl pkcs12` to convert to PEM when clients need it.

Activate by uncommenting and editing `SOLR_SSL_*` in `bin/solr.in.sh` (or `bin\solr.in.cmd` on Windows). With the Linux service install, edit `/var/solr/solr.in.sh`.

Variables shown in the guide:
- `SOLR_SSL_ENABLED` (implicitly true if `SOLR_SSL_KEY_STORE` is set)
- `SOLR_SSL_KEY_STORE`, `SOLR_SSL_KEY_STORE_PASSWORD`
- `SOLR_SSL_TRUST_STORE`, `SOLR_SSL_TRUST_STORE_PASSWORD`
- `SOLR_SSL_NEED_CLIENT_AUTH`, `SOLR_SSL_WANT_CLIENT_AUTH`
- `SOLR_SSL_CHECK_PEER_NAME`

Passwords shown in the guide are placeholders. In SolrCloud, tell the cluster to use https before restarting nodes (the `urlScheme` cluster property).

## Checked

2026-11-04. Confirmed against Enabling SSL: keytool PKCS12 command with `-ext SAN=`, openssl PEM conversion, `SOLR_SSL_*` variables in `bin/solr.in.sh` or `bin\solr.in.cmd`, `/var/solr/solr.in.sh` for the service install, `urlScheme`. Removed the unsourced real-CA advice.

Method: documentation only; no commands were run.
