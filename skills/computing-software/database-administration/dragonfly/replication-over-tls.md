---
id: computing-software.database-administration.dragonfly.replication-over-tls
name: replication-over-tls
category: computing-software
field: database-administration
product: dragonfly
tags: [tls-replication, replication, openssl, pem-files, dragonfly]
level: advanced
status: docs-checked
description: "Secure Dragonfly primary-replica replication with TLS: certificates, tls_replication flag and the replica start command."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/replication.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Prerequisites:

1. Dragonfly configured for TLS, including a server certificate.
2. A way for the replica to authenticate to the primary: a password or client certificates.

Only `.pem` files are supported.

OpenSSL example for a server key and request, then sign with your CA:

```bash
openssl req -newkey rsa:4096 -nodes -keyout server-key.pem -out server-req.pem
openssl x509 -req -in server-req.pem -days 365 -CA ca-cert.pem -CAkey ca-key.pem -CAcreateserial -out server-cert.pem
```

`-nodes` leaves the key unencrypted; for production consider encrypting private keys and store them securely.

Primary:

```bash
dragonfly --tls --tls_key_file=server-key.pem --tls_cert_file=server-cert.pem --tls_ca_cert_file=ca-cert.pem
```

Replica on another port:

```bash
dragonfly --tls --tls_key_file=replica-client-key.pem --tls_cert_file=replica-client-cert.pem --tls_ca_cert_file=ca-cert.pem --tls_replication=true --port 6380
```

Then connect with `redis-cli --tls ...` and run `REPLICAOF PRIMARY_HOST 6379`.

If the server certificate is signed by a public CA, do not pass the CA flag on the replica.

## Checked

2026-11-04. Confirmed in the Replication page (Secure Replication sections): prerequisites, `.pem` only, OpenSSL commands, `-nodes` meaning, primary and replica start commands, `tls_replication`, `REPLICAOF`, public CA note. Nothing removed.

Method: documentation only; no commands were run.
