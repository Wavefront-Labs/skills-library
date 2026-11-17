---
id: computing-software.database-administration.scylladb.security-node-to-node-tls
name: security-node-to-node-tls
category: computing-software
field: database-administration
product: scylladb
tags: [tls, internode-encryption, server-encryption-options, transitional, rolling-upgrade]
level: advanced
status: docs-checked
description: "ScyllaDB node-to-node TLS: server_encryption_options, internode_encryption values, and the three-step rolling migration without downtime."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/security/node-node-encryption.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Node-to-node encryption

Controlled by `server_encryption_options` in `scylla.yaml`:

```
server_encryption_options:
    internode_encryption: <none|rack|dc|all|transitional>
    certificate: <PEM certificate>
    keyfile: <PEM key>
    truststore: <PEM trust store>        # optional
    certficate_revocation_list: <PEM CRL>  # optional
    require_client_auth: false
    priority_string: <GnuTLS priority string>
```
`internode_encryption` values: `none` (default, nothing encrypted), `all` (everything), `dc` (between data centers only), `rack` (between racks), `transitional` (encrypts all outgoing traffic but accepts unencrypted incoming, for upgrades without downtime). `require_client_auth: true` demands client-side certificates (false by default). Restart each node to apply.

To move a live cluster to TLS with no downtime, do three passes, each a rolling restart:
1. Add a passive TLS listener with encryption still off: set `ssl_storage_port: 7001` and `server_encryption_options` with `internode_encryption: none` plus certificate and keyfile. Outgoing traffic stays unencrypted.
2. Change `internode_encryption` to `transitional`; outgoing traffic is now encrypted.
3. Change to `all`, `rack` or `dc`; this also enforces encryption on incoming traffic.

A self-signed chain can be built with openssl first. Finish each step on every node before starting the next.

## Checked

2026-11-09. Confirmed option names, internode_encryption values, require_client_auth default, restart requirement and the three-step migration against the ScyllaDB node-to-node encryption page (read in full). Removed the unsupported claim about what unrestarted nodes do.

Method: docs-checked 2026-11-09 against the ScyllaDB docs page operating-scylla/security/node-node-encryption.rst
