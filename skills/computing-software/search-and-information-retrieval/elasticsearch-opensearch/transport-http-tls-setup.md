---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.transport-http-tls-setup
name: transport-http-tls-setup
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, transport-http-tls-setup]
level: advanced
status: docs-checked
description: "Generate a CA and node certificates with elasticsearch-certutil and enable xpack.security transport and HTTP TLS; OpenSearch plugins.security.ssl settings."
sources:
  - https://www.elastic.co/docs/deploy-manage/security/set-up-basic-security
  - https://www.elastic.co/docs/deploy-manage/security/set-up-basic-security-plus-https
  - https://docs.opensearch.org/latest/security/configuration/tls/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enable TLS for transport and HTTP

**Goal:** encrypted node-to-node and client traffic. Transport TLS is required by multi-node Elasticsearch clusters, and production-mode clusters will not start without it.

## Elasticsearch (self-managed)
- CA: `./bin/elasticsearch-certutil ca` (default output `elastic-stack-ca.p12`). The page recommends a dedicated CA for the transport layer.
- Node certificate: `./bin/elasticsearch-certutil cert --ca elastic-stack-ca.p12`, producing `elastic-certificates.p12`; copy it into `$ES_PATH_CONF` on every node.
- `elasticsearch.yml` for the shared-file setup: `xpack.security.transport.ssl.enabled: true`, `xpack.security.transport.ssl.verification_mode: certificate`, `xpack.security.transport.ssl.client_authentication: required`, `xpack.security.transport.ssl.keystore.path: elastic-certificates.p12`, `xpack.security.transport.ssl.truststore.path: elastic-certificates.p12`. For hostname verification use `verification_mode: full` with a different certificate per host matching its DNS name or IP.
- Passwords go in the secure keystore, for example `./bin/elasticsearch-keystore add xpack.security.transport.ssl.keystore.secure_password` (and the truststore equivalent).
- Enabling transport TLS needs a full cluster restart: TLS and non-TLS nodes cannot talk to each other.
- HTTPS: `./bin/elasticsearch-certutil http` (answer `n` to CSR to sign with your CA), copy `http.p12` into `$ES_PATH_CONF`, set `xpack.security.http.ssl.enabled: true` and `xpack.security.http.ssl.keystore.path: http.p12`, add `xpack.security.http.ssl.keystore.secure_password` to the keystore. Clients then connect with https and must trust the CA.
- Elasticsearch polls TLS files for changes (`resource.reload.interval.high`, default 5 seconds) and reloads them.
- Failure mode: the shared `.p12` acts as a cluster-membership key, and with the same file as keystore and truststore, an expired directly-trusted peer certificate is not rejected.

## OpenSearch
- Settings live in `opensearch.yml`. Transport (mandatory TLS) requires `plugins.security.ssl.transport.pemcert_filepath`, `pemkey_filepath` (PKCS #8) and `pemtrustedcas_filepath`, as paths relative to the config directory.
- REST TLS is optional: `plugins.security.ssl.http.enabled: true` (default false; then only HTTPS is allowed), plus `plugins.security.ssl.http.pemcert_filepath`, `pemkey_filepath`, `pemtrustedcas_filepath`.
- Keystore alternative: `keystore_filepath`, `truststore_filepath` (JKS or PKCS12/PFX, default JKS).
- `transport.ssl.enforce_hostname_verification` defaults to true; certificates must carry the node hostname in subject or SAN.
- Admin certificate DN goes in `plugins.security.authcz.admin_dn`; node DNs in `plugins.security.nodes_dn` unless the certificate has an OID in SAN.
- Passwords can use `_secure` suffixed settings (for example `plugins.security.ssl.http.pemkey_password_secure`).

## Verify
- [ ] `curl --cacert <CA_FILE> https://<host>:9200` is accepted (with credentials) over https.

## Checked
Checked 2026-11-08 against the Elastic pages "Set up transport TLS" and "Set up HTTPS in Elasticsearch" and the OpenSearch page "Configuring TLS certificates". Removed because the pages do not state them: the unconditional "use verification_mode full" advice (the page uses certificate for the shared file), "run securityadmin after TLS changes", and the expired-CA joining claim.
Method: documentation only; no commands were run.
