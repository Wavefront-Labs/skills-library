---
id: computing-software.database-administration.oracle-database.tde-and-the-keystore
name: tde-and-the-keystore
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, oracle-security, oracle-tde, transparent-data-encryption, keystore, wallet, auto-login-keystore, wallet-root, tablespace-encryption, master-key-rotation, okv]
level: advanced
status: draft
description: "Set up Oracle TDE with WALLET_ROOT and a software keystore, encrypt tablespaces online, rotate master keys, and back up the keystore safely."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/asoag/configuring-transparent-data-encryption.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/asoag/managing-keystores-encryption-keys-tde.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# TDE and the keystore

**Goal:** datafiles, backups and redo of sensitive tablespaces encrypted at rest, with
a keystore that is backed up and opens automatically at startup. (Advanced Security
option licence on-prem; included in Oracle Cloud.)

## Configure the keystore location (19c style)
```sql
ALTER SYSTEM SET wallet_root = '/u01/app/oracle/admin/orcl/wallet' SCOPE = SPFILE;
-- restart, then
ALTER SYSTEM SET tde_configuration = 'KEYSTORE_CONFIGURATION=FILE' SCOPE = BOTH;
```
Keystore files then live in `<WALLET_ROOT>/tde/`. (`ENCRYPTION_WALLET_LOCATION` in
sqlnet.ora is deprecated.) `FILE` = software keystore; `OKV` = Oracle Key Vault;
`HSM`; `FILE|OKV` style for migration.

## Create keystore and master key
```sql
-- CDB root, as SYSKM or SYSDBA
ADMINISTER KEY MANAGEMENT CREATE KEYSTORE IDENTIFIED BY "<ks-pw>";
ADMINISTER KEY MANAGEMENT SET KEYSTORE OPEN IDENTIFIED BY "<ks-pw>" CONTAINER = ALL;
ADMINISTER KEY MANAGEMENT SET KEY IDENTIFIED BY "<ks-pw>" WITH BACKUP CONTAINER = ALL;
ADMINISTER KEY MANAGEMENT CREATE AUTO_LOGIN KEYSTORE FROM KEYSTORE IDENTIFIED BY "<ks-pw>";
-- or LOCAL AUTO_LOGIN: opens only on this host (cwallet.sso bound to the machine)
SELECT con_id, wrl_parameter, status, wallet_type, keystore_mode FROM v$encryption_wallet;
```
`status = OPEN`, `wallet_type = AUTOLOGIN` after restart. In united mode PDBs share the
CDB keystore; isolated mode (19c+) gives a PDB its own.

## Encrypt
```sql
CREATE TABLESPACE secure_data DATAFILE SIZE 10G ENCRYPTION USING 'AES256' ENCRYPT;
ALTER TABLESPACE users ENCRYPTION ONLINE USING 'AES256' ENCRYPT;    -- 12.2+, needs space for a copy
ALTER TABLESPACE users ENCRYPTION OFFLINE ENCRYPT;                  -- in place, tablespace offline (no extra space)
ALTER SYSTEM SET encrypt_new_tablespaces = ALWAYS;                  -- default CLOUD_ONLY
SELECT tablespace_name, encrypted FROM dba_tablespaces;
SELECT * FROM v$encrypted_tablespaces;
```
Column-level TDE (`ENCRYPT` on a column) exists but tablespace encryption is preferred:
no restrictions on indexes, and buffer cache holds decrypted blocks.
19c can encrypt SYSTEM/SYSAUX/UNDO too (fully encrypted database).

## Rotate and back up
```sql
ADMINISTER KEY MANAGEMENT SET KEY FORCE KEYSTORE IDENTIFIED BY "<ks-pw>" WITH BACKUP USING 'q4_2026';
ADMINISTER KEY MANAGEMENT BACKUP KEYSTORE USING 'pre_change' FORCE KEYSTORE IDENTIFIED BY "<ks-pw>";
```
Rotation re-encrypts tablespace keys only (fast). Copy `<WALLET_ROOT>/tde/*` to a secure
location separate from RMAN backups after every key change: an RMAN backup of an
encrypted tablespace is useless without the matching keystore, and storing them
together defeats the encryption.

## Data Guard and cloning
Copy the keystore (ewallet.p12 + cwallet.sso) to every standby **before** encrypting on
the primary; new keys must be copied again after rotation (or use OKV). For PDB
unplug/clone across CDBs, export/import keys (`EXPORT ENCRYPTION KEYS WITH SECRET`)
or use `KEYSTORE IDENTIFIED BY` clauses on `CREATE PLUGGABLE DATABASE`.

## Verify
- [ ] `v$encryption_wallet` OPEN / AUTOLOGIN on all instances and standbys.
- [ ] Target tablespaces show `ENCRYPTED = YES`.
- [ ] Keystore backup stored separately; a restore to another host with it was tested.
