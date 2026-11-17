---
id: computing-software.database-administration.sql-server.force-encryption-and-tls-certificates
name: force-encryption-and-tls-certificates
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, sql-server-security, force-encryption, tls-sql-server, certificates, trustservercertificate, tds-8]
level: practitioner
status: docs-checked
description: "Encrypt SQL Server client connections with a proper TLS certificate, Force Encryption or strict TDS 8.0, and fix client errors from untrusted certificates."
sources:
  - https://learn.microsoft.com/en-us/sql/database-engine/configure-windows/configure-sql-server-encryption
  - https://learn.microsoft.com/en-us/sql/relational-databases/security/networking/tds-8
  - https://learn.microsoft.com/en-us/sql/database-engine/configure-windows/certificate-requirements
  - https://learn.microsoft.com/en-us/sql/linux/configure/mssql-conf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Force Encryption and TLS certificates

## Certificate requirements
Per Microsoft's certificate requirements:
- In the local computer certificate store (preferred) or the service account's store.
- Enhanced Key Usage = Server Authentication (1.3.6.1.5.5.7.3.1); Subject Alternative Name should list every name clients use
  (host name, FQDN, AG listener names, FCI virtual name).
- Created with `KeySpec = AT_KEYEXCHANGE`, i.e. a legacy Cryptographic Service Provider key; certificates from a Key Storage Provider
  (KeySpec 0) are not compatible, and a certificate meeting only some requirements but configured manually can stop SQL Server starting.
  Check with `certutil -v -store My "<thumbprint>"` (KeySpec = 1).
- The service account needs read access to the private key; current time within Valid from/to (SQL Server checks validity only when you configure it).
- AG: one certificate on all replicas with all replica and listener names in the SAN, or one per replica each including the listener names.
  FCI: certificate for the virtual server name on every node, and the thumbprint written to the instance's SuperSocketNetLib `Certificate` registry value.

## Configure (Windows)
SQL Server Configuration Manager > SQL Server Network Configuration > Protocols for
`<instance>` > Properties:
- **Certificate** tab: select the certificate. SQL Server Configuration Manager from SQL Server 2019 integrates certificate management
  (and can be used with earlier instances); a certificate whose subject differs from the host name must be imported manually into the store.
- **Flags** tab: `Force Encryption = Yes` (all clients) and, from SQL Server 2022, the option to force strict encryption (TDS 8.0).
Restart the service. If SQL Server falls back to its own certificate it logs "A self-generated certificate was successfully loaded for encryption."
Precedence: the certificate configured in Configuration Manager/registry, else a store certificate with the machine FQDN in the subject and
private-key access for the service account (used even if not selected), else a self-generated one.

Linux uses mssql-conf: `network.tlscert`, `network.tlskey` (files readable by the mssql account), `network.forceencryption 1`
(default 0), and `network.tlsprotocols` (comma-separated list of allowed protocols), then restart.

## Clients
`Encrypt` takes strict, mandatory (true/yes) or optional (false/no); strict uses TDS 8.0 and needs ADO.NET (Microsoft.Data.SqlClient) 5.1+, ODBC 18.1.2.1+,
OLE DB 19.2.0+, JDBC 11.2.0+ or PHP 5.10+. Driver defaults differ by version: check your driver's documentation.
The client must be able to verify the server certificate (trusted CA, name matches CN or a SAN):
```
Server=sql01.corp.example.com;Database=Sales;Encrypt=True;TrustServerCertificate=False;
Server=sql01.corp.example.com;Encrypt=Strict;HostNameInCertificate=sql01.corp.example.com;    -- TDS 8.0
```
If validation fails, fix the certificate or install the issuing CA on the client. `TrustServerCertificate=True` skips validation (not recommended);
with `Encrypt=strict` it cannot be used to accept any certificate: use `HostNameInCertificate` (ODBC 18: the setting names the trusted certificate file).
TDS 8.0 does the TLS handshake before any TDS message and supports TLS 1.3 (OS-dependent: Windows 11 / Server 2022 and later); `Encrypt=Mandatory` is not compatible with a TLS 1.3-only setup.

## Without your own certificate
Login packets are always encrypted. If no trusted certificate is available SQL Server generates a self-signed fallback certificate at startup
(SHA256 from SQL Server 2017; SHA1 before). With Force Encryption set, all traffic is then encrypted with it, but it does not protect against server
identity spoofing and clients that validate certificates will reject it.

## Gotchas
- AG listeners: the listener name must be in the certificate SAN on **every** replica.
- Expired certificates keep working once provisioned, but some clients (for example Power BI) check validity on every connection.
- A certificate with the FQDN in its subject and a readable private key is used automatically even if not selected; revoke the service account's access to an unwanted one.
- SQL Server 2025 adds TDS 8.0 support to Agent, sqlcmd, bcp, linked servers, replication and log shipping, some with breaking changes.

## Verify
```sql
SELECT DISTINCT encrypt_option FROM sys.dm_exec_connections WHERE net_transport <> 'Shared memory';
```
Microsoft's check: the result should be only `TRUE` (a `FALSE` row means an unencrypted connection).

## Checked
Date 2026-10-23. Documentation release: SQL Server 2025 pages for Certificate requirements, Encrypt connections by importing a certificate, TDS 8.0 and mssql-conf (TLS settings), 2017-2025.
Confirmed: certificate store, EKU, SAN, KeySpec and service-account requirements, AG/FCI guidance, Configuration Manager 2019 integration and 2022 strict option, self-signed fallback behaviour and message, certificate precedence, strict encryption driver versions and TLS 1.3 matrix, Linux `network.*` settings, the verification query. Removed unconfirmed claims: key size 2048, `Encrypt=Yes` default in ODBC 18/SqlClient 4.0, certificate-chain error text, TLS 1.0/1.1 disabling advice, renewal procedure and the sha1 hash error-log line.
Method: documentation only; no commands were run.
