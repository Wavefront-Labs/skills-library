---
id: computing-software.cybersecurity-defensive.dex.dex-storage-etcd
name: dex-storage-etcd
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [etcd, storage, namespace, tls]
level: practitioner
status: docs-checked
description: "Configure Dex etcd v3 storage: endpoints, namespace prefix, username and password, and the ssl block with serverName, caFile, keyFile, certFile."
sources:
  - https://dexidp.io/docs/configuration/storage/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dex can persist state to etcd v3.

```yaml
storage:
  type: etcd
  config:
    endpoints:
      - http://localhost:2379
    namespace: my-etcd-namespace/
```

Options under `config`:

- `endpoints`: list of etcd endpoints to connect to.
- `namespace`: etcd namespace for the connection. All keys created by the etcd storage are prefixed with it, which is useful when you share the etcd cluster among several applications. Another approach for setting a namespace is an etcd proxy.
- `username`, `password`: etcd authentication.
- `ssl`: SSL setup for the etcd connection, with these options listed on the page: `serverName` (ensures the certificate matches the hostname the client connects to), `caFile` (path to the CA), `keyFile` (path to the private key) and `certFile` (path to the certificate).

TLS example (the docs list the ssl options without a full YAML example, so the nesting under `ssl` follows the Postgres and MySQL examples):

```yaml
storage:
  type: etcd
  config:
    endpoints: ["https://etcd.example.com:2379"]
    ssl:
      serverName: etcd.example.com
      caFile: /etc/dex/etcd-ca.pem
      keyFile: /etc/dex/etcd-key.pem
      certFile: /etc/dex/etcd-cert.pem
```

Gotcha: Dex saves signing keys and bcrypt'd passwords in its backing storage, so use both transport security and access controls (ACLs), whichever storage you choose.

## Checked

2026-11-08. Read in full: the Dex Storage documentation page (Etcd section and the opening security note). Confirmed: etcd v3, the example config, all listed options and their descriptions, etcd proxy alternative, storage security warning. The nested ssl YAML layout is an extrapolation and is flagged as such above.

Method: documentation only; no commands were run.
