---
id: computing-software.messaging-and-integration.debezium.sqlserver-ssl-encrypted-connections
name: sqlserver-ssl-encrypted-connections
category: computing-software
field: messaging-and-integration
product: debezium
tags: [sql-server, ssl, encryption, jdbc]
level: practitioner
status: docs-checked
description: "Configure driver.encrypt, trustServerCertificate and trust store for SQL Server connections, and when not to trust certificates."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/sqlserver.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
JDBC connections to SQL Server use SSL encryption by default. Tune it with `driver.`-prefixed pass-through properties.

Enforce encryption with certificate validation:

```json
"driver.encrypt": true,
"driver.trustServerCertificate": false,
"driver.trustStore": "/path/to/trust-store",
"driver.trustStorePassword": "password-for-trust-store"
```

If SSL is not enabled on the database, or you intentionally want an unencrypted connection, disable it:

```json
"driver.encrypt": false
```

For a known self-signed certificate in non-production, you can encrypt and skip certificate path validation:

```json
"driver.encrypt": true,
"driver.trustServerCertificate": true
```

Do not use automatic trust in production. It skips certificate chain and host name validation and leaves connections open to man-in-the-middle attacks. Use it only in testing and development.

The `driver.` prefix passes a property to the database driver (prefix stripped), so other driver options can be set the same way.

Related connection properties: `database.instance` names a SQL Server named instance, but if both `database.port` and `database.instance` are set, `database.instance` is ignored. `database.names` names the databases to capture.

Check: start the connector with validation on and confirm it connects without certificate errors in the log.

## Checked

2026-11-08. Confirmed against the Debezium page connectors/sqlserver (read in part: Encrypting connections, pass-through driver properties, database.instance, database.port and database.names rows). Removed the naming of a specific JDBC driver, which the page does not give.

Method: documentation only; no commands were run.
