---
id: computing-software.cryptography-implementation.applied-cryptography.database-tde-versus-application-encryption
name: database-tde-versus-application-encryption
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, transparent-data-encryption, tde, database-encryption, column-encryption, sql-server-tde, oracle-tde, mysql-keyring, always-encrypted, field-level-encryption]
level: practitioner
status: draft
description: "Decide between database TDE, column encryption and application-level encryption: what each protects against, key hierarchy, and engine-specific options."
sources: ["https://learn.microsoft.com/en-us/sql/relational-databases/security/encryption/transparent-data-encryption", "https://docs.oracle.com/en/database/oracle/oracle-database/19/asoag/introduction-to-transparent-data-encryption.html", "https://dev.mysql.com/doc/refman/8.0/en/innodb-data-encryption.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Database TDE versus application encryption

## Threats each layer stops
| Threat | Disk / volume encryption | TDE | Client-side column (Always Encrypted, CSFLE) | Application field encryption |
|---|---|---|---|---|
| Stolen disk or snapshot | Yes | Yes | Yes | Yes |
| Stolen DB backup file | No (backups are files) | Yes (if backup encrypted with TDE key) | Yes | Yes |
| DBA or SQL-level access | No | No | Yes | Yes |
| SQL injection reading rows | No | No | Partial (app holds keys) | Partial |
| Compromised app server | No | No | No | No |

TDE is a compliance and media-theft control, not protection from anyone who can query the database.

## Engine options
- **SQL Server TDE:** DEK per database, protected by a certificate in master or an EKM/Azure Key Vault key;
  back up the certificate and private key or restores fail. Always Encrypted moves keys to the client.
- **Oracle TDE:** keystore (wallet) or OKV/HSM, tablespace or column encryption; `ADMINISTER KEY MANAGEMENT` for
  rekey.
- **MySQL/MariaDB:** InnoDB tablespace encryption with keyring component (file, KMIP, cloud KMS).
- **PostgreSQL:** no TDE in community releases; use volume encryption, pgcrypto (keys in SQL, weak), or vendor
  distributions; prefer application encryption.
- **MongoDB:** encrypted storage engine (Enterprise/Atlas), CSFLE and Queryable Encryption on the client.

## Decision
- Need to defend against insiders/DB compromise: application or client-side encryption of the sensitive fields.
- Need media/backup protection with zero app change: TDE plus KMS-held master key.
- Both are often right: TDE for everything, app encryption for the few most sensitive fields.

## Gotchas
- TDE master key in a file next to the database defeats the point; use KMS/HSM.
- Key rotation in TDE often only re-encrypts the DEK, not the data; know which your engine does.
- Application encryption breaks indexing, sorting and LIKE; plan blind indexes or deterministic encryption.

## Verify
- [ ] Restoring a backup on a server without the key fails.
- [ ] Threat model states which layer covers which attacker.
