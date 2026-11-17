---
id: computing-software.database-administration.oracle-database.native-network-encryption
name: native-network-encryption
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, oracle-net, sqlnet-encryption, native-network-encryption, sqlnet-ora, crypto-checksum, tcps, tls, data-in-transit, network-service-banner]
level: practitioner
status: draft
description: "Encrypt Oracle client-server traffic with native network encryption in sqlnet.ora or TLS (TCPS), choose REQUIRED vs REQUESTED, and verify sessions are encrypted."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/dbseg/configuring-network-data-encryption-and-integrity.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/dbseg/configuring-transport-layer-security-authentication.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Native network encryption (sqlnet.ora) and TLS

Two ways to encrypt Oracle Net traffic, both included in all editions since 12c
(Advanced Security licence no longer needed for network encryption):
- **Native network encryption (NNE)**: negotiated by Oracle Net on the normal TCP port;
  no certificates. Simple, but Oracle marks NNE as deprecated in 23ai in favour of TLS.
- **TLS (TCPS)**: standard TLS with certificates and wallets; required for many
  compliance regimes and for verifying server identity.

## Native network encryption
Server `sqlnet.ora` (in the DB home's / Grid home's `network/admin` used by the listener and server processes):
```
SQLNET.ENCRYPTION_SERVER = REQUIRED
SQLNET.ENCRYPTION_TYPES_SERVER = (AES256, AES192)
SQLNET.CRYPTO_CHECKSUM_SERVER = REQUIRED
SQLNET.CRYPTO_CHECKSUM_TYPES_SERVER = (SHA256, SHA384, SHA512)
```
Client side defaults are `ACCEPTED`, so most clients need no change. Negotiation matrix:
`REJECTED` / `ACCEPTED` / `REQUESTED` / `REQUIRED` on each side; a `REQUIRED` vs `REJECTED`
pair fails with `ORA-12660`. Roll out with server `REQUESTED` first, measure which
sessions are still unencrypted, then switch to `REQUIRED`.
Remove weak algorithms (DES, 3DES, RC4, MD5) from lists; 19.x RUs added
`SQLNET.ALLOW_WEAK_CRYPTO = FALSE` to enforce that.

## TLS (TCPS) outline
```bash
orapki wallet create -wallet /u01/app/oracle/wallet -auto_login
orapki wallet add -wallet /u01/app/oracle/wallet -dn "CN=db01.corp.local" -keysize 2048 -validity 730 -self_signed   # or import CA-signed cert
```
listener.ora: add `(ADDRESS = (PROTOCOL = TCPS)(HOST = db01.corp.local)(PORT = 2484))` and
`WALLET_LOCATION`; server sqlnet.ora:
```
WALLET_LOCATION = (SOURCE = (METHOD = FILE)(METHOD_DATA = (DIRECTORY = /u01/app/oracle/wallet)))
SSL_CLIENT_AUTHENTICATION = FALSE          # one-way TLS; TRUE for mutual TLS
SSL_VERSION = 1.2                          # or 1.3 on 23ai
```
Clients trust the CA (wallet or system store) and connect with `tcps://host:2484/service?ssl_server_dn_match=on`.
Register the TCPS endpoint in `LOCAL_LISTENER` so services are offered there.

## Verify per session
```sql
SELECT sid, network_service_banner FROM v$session_connect_info
WHERE sid = SYS_CONTEXT('USERENV','SID');
-- NNE: "AES256 Encryption service adapter for Linux" + "Crypto-checksumming service ... SHA256"
SELECT SYS_CONTEXT('USERENV','NETWORK_PROTOCOL') FROM dual;   -- tcps for TLS
-- unencrypted sessions estate-wide (NNE): sessions without an encryption banner
SELECT s.sid, s.username, s.machine, s.program FROM v$session s
WHERE s.type = 'USER' AND NOT EXISTS (SELECT 1 FROM v$session_connect_info c
  WHERE c.sid = s.sid AND c.network_service_banner LIKE '%Encryption service adapter%');
```

## Gotchas
- Very old clients (pre-11.2 JDBC thin) may not support AES/SHA-2 lists; upgrade drivers.
- JDBC thin needs `oracle.net.encryption_client` properties only if you want to force it client-side.
- Data Guard redo transport uses the same settings; encrypt it too.
- NNE does not authenticate the server: man-in-the-middle protection needs TLS with DN matching.

## Verify
- [ ] `network_service_banner` shows AES256 + SHA-2 (or protocol tcps) for app sessions.
- [ ] Server set to REQUIRED after a REQUESTED phase showed no unencrypted clients.
