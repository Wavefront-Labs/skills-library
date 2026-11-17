---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.certificate-rotation
name: certificate-rotation
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, certificate-rotation]
level: advanced
status: docs-checked
description: "Replace node certificates before expiry with reloading, rolling restarts and a CA overlap."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-ssl.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ssl-tls.html
  - https://docs.opensearch.org/latest/security/configuration/tls/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rotate certificates

**Goal:** rotation without downtime.
- Track expiry: `GET /_ssl/certificates` (Elasticsearch; needs the `monitor` cluster privilege). It lists certificates from all TLS contexts, including every certificate in a configured keystore or truststore even if not in active use, but not those from the JRE default SSL context.
- Add a new CA to truststores first, roll the cluster, then issue new node certificates, roll again, then drop the old CA.
- Elasticsearch watches files configured in TLS-related node settings (certificates, keys, keystores, truststores) and reloads them when they change; polling follows `resource.reload.interval.high`, default 5 seconds.
- OpenSearch: set `plugins.security.ssl.certificates_hot_reload.enabled: true` in `opensearch.yml` and the nodes reload changed certificate and key files without a restart. Alternatively set `plugins.security.ssl_cert_reload_enabled: true` and call `PUT /_plugins/_security/api/ssl/transport/reloadcerts` (or `.../ssl/http/reloadcerts`) as a superadmin. By default replacement certificates must keep the same issuer/subject DN and SAN, and be stored at the same location.
- Failure mode: replacing CA and certs in one step splits the cluster.

## Verify
- [ ] `GET _ssl/certificates` shows new expiry dates on every node.

## Notes
- Try every request on a test index first; syntax and defaults differ between Elasticsearch and OpenSearch versions, so check the linked reference for yours.

## Checked
2026-11-08. Read the Elasticsearch Get SSL certificates API page, the Elasticsearch set-up-basic-security page (file monitoring and reload interval) and the OpenSearch TLS page (hot reload, Reload Certificates API, DN verification). Replaced the hedged OpenSearch restart/reload sentence with the documented settings and endpoints. The CA-overlap sequence is operational advice, not a documented claim.
Method: documentation only; no commands were run.
