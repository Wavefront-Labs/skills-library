---
id: computing-software.database-administration.dragonfly.enable-tls
name: enable-tls
category: computing-software
field: database-administration
product: dragonfly
tags: [tls, tls-cert-file, tls-key-file, certbot, dragonfly]
level: practitioner
status: docs-checked
description: "Encrypt client connections to Dragonfly with --tls, a certificate and key, and a password, then connect with redis-cli --tls."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/using-tls.md
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/flags.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
For an internet-facing endpoint, protect data in transit with TLS.

The docs obtain a certificate with `certbot` (from Let's Encrypt) on an Ubuntu server with a DNS name pointing to it; the key and certificate end up in `/etc/letsencrypt/live/<domain>/`.

Start Dragonfly with TLS and a password:

```bash
export DFLY_PASS_TOKEN=<your_password>
sudo ./dragonfly --tls \
  --tls_key_file=/etc/letsencrypt/live/<domain>/privkey.pem \
  --tls_cert_file=/etc/letsencrypt/live/<domain>/fullchain.pem \
  --requirepass=${DFLY_PASS_TOKEN}
```

Connect:

```bash
redis-cli --tls -h <domain> -a ${DFLY_PASS_TOKEN}
```

TLS flags (all default off or empty):

| Flag | Purpose |
| --- | --- |
| `tls` | enable TLS |
| `tls_cert_file` | public certificate |
| `tls_key_file` | private key |
| `tls_ca_cert_file` | CA certificate to validate clients |
| `tls_ca_cert_dir` | directory of CA certificates; run `c_rehash` on it first |
| `tls_replication` | TLS for replication |

Related: client certificate authentication, certificate rotation without downtime, and on Kubernetes the Operator `tlsSecretRef` field.

## Checked

2026-11-04. Confirmed in the Dragonfly TLS guide (certbot, Ubuntu, key and certificate under `/etc/letsencrypt/live/`, start and connect commands) and the flags page (TLS flag descriptions and defaults, `c_rehash`). The docs state the live directory only; the per-domain subdirectory is the guide's example.

Method: documentation only; no commands were run.
