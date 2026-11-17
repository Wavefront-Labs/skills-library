---
id: computing-software.cybersecurity-defensive.keycloak.ldap-tls-and-failover
name: ldap-tls-and-failover
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, ldap, ldaps, truststore, failover]
level: practitioner
status: docs-checked
description: "Secure the Keycloak LDAP connection with ldaps and a server truststore, and configure failover with multiple space-separated URLs."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/user-federation/ldap.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ldap tls and failover
For a secure connection use an `ldaps://` Connection URL such as `ldaps://myhost.com:636`. Keycloak then communicates over SSL, and you must configure a truststore on the Keycloak server so it trusts the LDAP server's certificate (see the server guide's "Configuring a Truststore"). The `Use Truststore SPI` property is deprecated and should normally be left as `Always`.

Failover: enter several URLs in the *Connection URL* field as a space-separated list:
```
ldap://server1:389 ldap://server2:389
ldaps://server1:636 ldaps://server2:636
```
The Java JNDI provider tries each URL from left to right until a connection succeeds. This is sequential failover, not load balancing, and it happens at connection creation time. Do not use commas: `ldap://server1,ldap://server2` is a connection error, and a comma followed by a space silently discards the first URL. *Connection Timeout* (default 5000 ms) is spent on each unreachable URL before failover proceeds; a cleanly stopped server refuses immediately and fails over without delay.

Connection pooling is enabled by default for both plain and ssl protocols and is configured with system properties such as `com.sun.jndi.ldap.connect.pool.initsize`, `com.sun.jndi.ldap.connect.pool.maxsize` (too low may cause contention), `com.sun.jndi.ldap.connect.pool.timeout` and `com.sun.jndi.ldap.connect.timeout`, for example via `JAVA_OPTS_APPEND=-Dcom.sun.jndi.ldap.connect.pool.initsize=10 -Dcom.sun.jndi.ldap.connect.pool.maxsize=50`. Set `com.sun.jndi.ldap.connect.pool.debug` to `all` to trace pooling; restart the server after changing pool settings.

## Checked
2026-11-03. Confirmed against server_admin/topics/user-federation/ldap.adoc (secure connection, failover, connection pool sections). Removed (not on the page): the `--truststore-paths` option, the StartTLS statement, the handshake/Test connection gotchas, the vault reference advice and the Verify step.
Method: documentation only; no commands were run.
