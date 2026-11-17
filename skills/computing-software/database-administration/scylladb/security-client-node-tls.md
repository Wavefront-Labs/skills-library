---
id: computing-software.database-administration.scylladb.security-client-node-tls
name: security-client-node-tls
category: computing-software
field: database-administration
product: scylladb
tags: [tls, client-encryption, client-encryption-options, priority-string, cqlsh]
level: practitioner
status: docs-checked
description: "Enable client-to-node TLS in ScyllaDB: client_encryption_options, certificate, keyfile, truststore, CRL, GnuTLS priority strings and log check."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/security/client-node-encryption.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Client-to-node encryption (TLS)

Do this on every node, one at a time. On an existing cluster first run `nodetool drain` and stop ScyllaDB (skip for a brand-new cluster), then edit `/etc/scylla/scylla.yaml`:

```
client_encryption_options:
    enabled: true
    certificate: /etc/scylla/db.crt
    keyfile: /etc/scylla/db.key
    truststore: <path to a PEM-encoded trust store>   # optional
    certficate_revocation_list: <path to a PEM CRL>   # optional
    require_client_auth: <true or false>
    priority_string: SECURE128:-VERS-TLS1.0:-VERS-TLS1.1
```
- `enabled` defaults to false.
- `certificate` and `keyfile` are PEM files (self-signed or CA-issued).
- `truststore` is optional; if omitted the system trust store is used. With a self-signed certificate it must point to a PEM container with that authority.
- The CRL option name is spelled `certficate_revocation_list` in the documentation.

Priority strings (GnuTLS syntax) control TLS version and strength. Disable TLS 1.1 and lower with 128-bit minimum: `SECURE128:-VERS-TLS1.0:-VERS-TLS1.1`. Allow only TLS 1.2 and 1.3 with 128 and 192-bit ciphers: `SECURE128:+SECURE192:-VERS-ALL:+VERS-TLS1.2:+VERS-TLS1.3`.

Start ScyllaDB and verify with `journalctl _COMM=scylla`; look for `storage_service - Enabling encrypted CQL connections between client and node`.

Clients: cqlsh needs a generated cqlshrc file for SSL mode. cassandra-stress needs Java keystore and truststore built with `openssl pkcs12 -export` and `keytool -importkeystore` (always give a non-empty password).

## Checked

2026-11-09. Confirmed the procedure, option list and defaults, the misspelled CRL option, both priority strings, the log check and the cqlsh and cassandra-stress notes against the ScyllaDB client-to-node encryption page (read in full). The page leaves require_client_auth unspecified in its example, so it is shown as a placeholder.

Method: docs-checked 2026-11-09 against the ScyllaDB docs page operating-scylla/security/client-node-encryption.rst
