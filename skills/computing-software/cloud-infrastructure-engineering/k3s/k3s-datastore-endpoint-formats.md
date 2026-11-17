---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-datastore-endpoint-formats
name: k3s-datastore-endpoint-formats
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, datastore-endpoint, postgres, mysql, etcd-endpoints]
level: advanced
status: docs-checked
description: "Connection-string formats and TLS options for --datastore-endpoint with PostgreSQL, MySQL/MariaDB and etcd."
sources:
  - https://docs.k3s.io/datastore
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: point K3s at an external datastore. Parameters can be CLI flags or environment variables:

- --datastore-endpoint / K3S_DATASTORE_ENDPOINT: connection string.
- --datastore-cafile / K3S_DATASTORE_CAFILE: CA file to verify a datastore certificate signed by a custom CA.
- --datastore-certfile / K3S_DATASTORE_CERTFILE: client certificate; requires the keyfile too.
- --datastore-keyfile / K3S_DATASTORE_KEYFILE: client key.

Best practice from the docs: pass these as environment variables so credentials do not show in process info.

PostgreSQL:

```
postgres://username:password@hostname:port/database-name
```

A missing database name is created. With only `postgres://`, K3s connects to localhost as user postgres with password postgres and creates a database named kubernetes. Extra options: see godoc.org/github.com/lib/pq.

MySQL / MariaDB:

```
mysql://username:password@tcp(hostname:3306)/database-name
```

A missing database is created. With only `mysql://`, K3s uses the socket /var/run/mysqld/mysqld.sock as root with no password and creates a database named kubernetes. Known issue: you cannot set the tls parameter (for example skip-verify), although TLS itself works.

etcd (one or more comma-separated URLs):

```
https://etcd-host-1:2379,https://etcd-host-2:2379,https://etcd-host-3:2379
```

## Checked

2026-11-03: read docs.k3s.io datastore. Confirmed: the four datastore flags and environment variables, the PostgreSQL, MySQL/MariaDB and etcd connection string formats, default databases and the MySQL tls known issue.

Method: documentation only; no commands were run.
