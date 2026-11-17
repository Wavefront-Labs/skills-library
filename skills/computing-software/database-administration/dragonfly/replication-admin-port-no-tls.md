---
id: computing-software.database-administration.dragonfly.replication-admin-port-no-tls
name: replication-admin-port-no-tls
category: computing-software
field: database-administration
product: dragonfly
tags: [no-tls-on-admin-port, admin-port, replication, private-network, dragonfly]
level: advanced
status: docs-checked
description: "Use plaintext replication over a Dragonfly admin port inside a private network while keeping TLS on client ports."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/replication.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When primary and replica are on the same private network you may keep TLS for external connections but allow plaintext replication through the admin port.

Primary:

```bash
dragonfly --tls --tls_key_file=server-key.pem \
          --tls_cert_file=server-cert.pem \
          --tls_ca_cert_file=ca-cert.pem \
          --port 6379 -admin_port=6380 --no_tls_on_admin_port=true
```

Replica:

```bash
dragonfly --tls --tls_key_file=replica-client-key.pem \
          --tls_cert_file=replica-client-cert.pem \
          --tls_ca_cert_file=ca-cert.pem \
          --port 6381 -admin_port=6382
```

Connect to the replica's admin port and point at the primary's admin port:

```bash
redis-cli -p 6382
dragonfly> REPLICAOF PRIMARY_HOST 6380
```

Result: replication does **not** use TLS, but connections to ports 6379 and 6381 still require TLS.

Flag reference: `no_tls_on_admin_port` defaults to false; `admin_port` (default 0) enables admin access to the console on that port and serves both HTTP and RESP.

## Checked

2026-11-04. Confirmed in the Replication page (non-TLS admin port section) and the flags page (`admin_port`, `no_tls_on_admin_port`). Removed the claim that 0 disables the admin console; the flags page only gives the default of 0.

Method: documentation only; no commands were run.
