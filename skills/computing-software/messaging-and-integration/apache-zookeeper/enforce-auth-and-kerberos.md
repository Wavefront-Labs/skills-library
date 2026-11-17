---
id: computing-software.messaging-and-integration.apache-zookeeper.enforce-auth-and-kerberos
name: enforce-auth-and-kerberos
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, enforce-auth, kerberos, principal, canonicalizehostnames, sasl]
level: advanced
status: docs-checked
description: "Require authentication with enforce.auth.enabled and enforce.auth.schemes, and the kerberos.* principal-handling options and shutdown timeout defaults."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperAdmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enforcing authentication and Kerberos options

- `enforce.auth.enabled` (`zookeeper.enforce.auth.enabled`, 3.7.0): default false (disabled). When true the server accepts connections and requests only from clients authenticated with one of the schemes in `enforce.auth.schemes`; others cannot establish a session and get error code -124, and Java and C clients close the session without retrying.
- `enforce.auth.schemes` (3.7.0): comma-separated authentication schemes; a client must authenticate with at least one before any operation. Used only when `enforce.auth.enabled` is true.
- With `enforce.auth.enabled=true` and `enforce.auth.schemes=sasl`, `zookeeper.allowSaslFailedClients` is overruled.
- `sessionRequireClientSASLAuth` (3.6.0): default false; shorthand for `enforce.auth.enabled=true` with scheme sasl.

Kerberos:
- `kerberos.removeHostFromPrincipal` default false: strips the host, so `zk/myhost@EXAMPLE.COM` authenticates as `zk@EXAMPLE.COM`.
- `kerberos.removeRealmFromPrincipal` default false: strips the realm, so `zk/myhost@EXAMPLE.COM` authenticates as `zk/myhost`.
- `kerberos.canonicalizeHostNames` default false (3.7.0): canonicalises host names from `server.x` lines so CNAMEs can be used while SASL Kerberos between quorum members still works.
- `kerberos.shutdownTimeoutMs` default 5000 (3.9.7): how long shutdown waits for the Kerberos TGT renewal thread; 0 waits without a timeout.
- Register the SASL provider with `authProvider.1=org.apache.zookeeper.server.auth.SASLAuthenticationProvider`.

JAAS file layout and quorum SASL options are not detailed in the sections read; consult the Administrator's Guide and the ZooKeeper wiki SASL page before configuring them.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Administrator's Guide (authentication options). Removed: the "Verify" scenario about rejected and accepted clients (the page documents error code -124 but gives no test procedure).
