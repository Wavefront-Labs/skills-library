---
id: computing-software.database-administration.cassandra.tls-and-audit
name: tls-and-audit
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, client-encryption, internode-encryption, audit-logging, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Securing transport"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/managing/operating/security.html", "https://cassandra.apache.org/doc/latest/cassandra/managing/operating/auditlogging.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS encryption and audit logging

Goal: encrypt traffic and record access.
- Configure `server_encryption_options` (internode) and `client_encryption_options` with keystore and truststore settings. Internode encryption is off (`internode_encryption: none`) until set to `rack`, `dc` or `all`.
- For client connections, `enabled: true` with `optional: false` requires all clients to use TLS; both `true` lets encrypted and unencrypted clients share the port.
- Since Cassandra 4, SSL certificates hot-reload when the files are updated, and `nodetool reloadssl` triggers it.
- Audit logging is new in 4.0, configured under `audit_logging_options` in `cassandra.yaml` (`enabled: false` by default), and can also be switched at runtime with `nodetool`.
- Audit logs are written per node.
Verify: clients connect over TLS and plain connections are rejected when `enabled` is true and `optional` is false.

## Checked

2026-11-02. Checked against the Security page (encryption options, hot reloading, reloadssl, optional) and the Audit Logging page (4.0, audit_logging_options, enabled default, per-node logs, runtime enable). Removed: `require_client_auth` wording and the `nodetool status` verify step (not confirmed).

Method: documentation only; no commands were run.
