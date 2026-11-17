---
id: computing-software.database-administration.elasticsearch.tls-setup-with-elasticsearch-certutil
name: tls-setup-with-elasticsearch-certutil
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, elasticsearch-security, elasticsearch-certutil, tls, transport-layer-ssl, http-ssl, certificate-rotation, pkcs12, xpack-security]
level: advanced
status: docs-checked
description: "Secure Elasticsearch transport and HTTP layers with TLS using elasticsearch-certutil (CA, node certs with SANs), keystore passwords, and rotation before expiry."
sources:
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/security/set-up-basic-security.md
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/security/set-up-basic-security-plus-https.md
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/security/same-ca.md
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/security/different-ca.md
  - https://github.com/elastic/elasticsearch/blob/main/docs/reference/elasticsearch/command-line-tools/certutil.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS with elasticsearch-certutil

**Goal:** node-to-node traffic is mutually authenticated and encrypted, clients
use HTTPS with a verifiable certificate.

8.x auto-configures security on first start of a fresh node (generated certs,
enrollment tokens). Use the manual path below for multi-node production
clusters, custom CAs, and rotation.

## Transport layer (required for any multi-node secured cluster)
```bash
bin/elasticsearch-certutil ca --out elastic-stack-ca.p12                 # keep the CA safe, off the nodes
bin/elasticsearch-certutil cert --ca elastic-stack-ca.p12 --out elastic-certificates.p12
```
Copy `elastic-certificates.p12` to each node's config dir.
```yaml
xpack.security.enabled: true
xpack.security.transport.ssl.enabled: true
xpack.security.transport.ssl.verification_mode: certificate
xpack.security.transport.ssl.client_authentication: required
xpack.security.transport.ssl.keystore.path: elastic-certificates.p12
xpack.security.transport.ssl.truststore.path: elastic-certificates.p12
```
```bash
bin/elasticsearch-keystore add xpack.security.transport.ssl.keystore.secure_password
bin/elasticsearch-keystore add xpack.security.transport.ssl.truststore.secure_password
```
`verification_mode: full` additionally checks hostnames/IPs in SANs: generate
per-node certs with `--dns`/`--ip` (or `certutil cert --in instances.yml`).

## HTTP layer
```bash
bin/elasticsearch-certutil http      # interactive: CSR for your corporate CA or sign with the stack CA; add all DNS names/IPs
```
```yaml
xpack.security.http.ssl.enabled: true
xpack.security.http.ssl.keystore.path: http.p12
```
Give clients (Kibana, Logstash, apps) the CA PEM (`elasticsearch-ca.pem` from the zip).

## Rotation
Certs from certutil are valid for 1095 days (`--days`, about 3 years) by default. Check:
```bash
curl -s -u elastic --cacert ca.pem https://localhost:9200/_ssl/certificates?pretty   # path, subject, expiry
```
Same-CA rotation: if you replace the certificate and key files on each node under the same filenames, Elasticsearch reloads them and starts using the new ones (if the keystore password changes, save under a new filename and follow the docs for the rolling restart). New CA: add it to every node's truststore first (trust both), update node certs with rolling restarts, then optionally remove the old CA.

## Gotchas
- Enabling TLS for transport on an existing cluster requires a full cluster restart: nodes using TLS cannot talk to nodes without it.
- Kibana's `elasticsearch.ssl.certificateAuthorities` must include the HTTP CA.

## Verify
`curl --cacert ca.pem -u elastic https://es1:9200/_cluster/health` succeeds;
`curl http://es1:9200` fails; logs have no `SSLHandshakeException`.

## Checked

Checked 2026-10-25 against elastic/docs-content and elastic/elasticsearch `main` (Stack 9.x docs). Confirmed: certutil `ca`, `cert --ca`, `http` modes and `--dns`/`--ip`/`--in`; default output `elastic-certificates.p12` and `--days` default 1095; `elasticsearch-ca.pem` in the HTTP zip; full cluster restart when enabling transport TLS; same-CA reload behaviour; different-CA trust-both procedure. The exact keystore setting names and `client_authentication` line follow the settings pattern but were not re-read line by line; the `_ssl/certificates` call is an API path that was not rechecked.

Method: documentation only; no commands were run.
