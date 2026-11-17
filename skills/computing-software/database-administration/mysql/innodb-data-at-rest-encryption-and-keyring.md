---
id: computing-software.database-administration.mysql.innodb-data-at-rest-encryption-and-keyring
name: innodb-data-at-rest-encryption-and-keyring
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mysql-security, innodb-tablespace-encryption, mysql-keyring, component-keyring-file, binlog-encryption, master-key-rotation, encryption-at-rest, tde]
level: advanced
status: draft
description: "Encrypt InnoDB tablespaces, redo/undo logs and binlogs at rest in MySQL 8 with a keyring component, rotate the master key, and back it up so restores work."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/innodb-data-encryption.html
  - https://dev.mysql.com/doc/refman/8.4/en/keyring-component-installation.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# InnoDB data-at-rest encryption

**Goal:** stolen disks or backup files are unreadable without the keyring, and
losing the keyring is planned for.

## Keyring component (8.4: plugins removed, components only)
1. Global manifest next to the mysqld binary, `mysqld.my`:
   ```json
   { "components": "file://component_keyring_file" }
   ```
2. Component config `component_keyring_file.cnf` in the plugin dir:
   ```json
   { "path": "/var/lib/mysql-keyring/component_keyring_file", "read_only": false }
   ```
3. Restart; check `SELECT * FROM performance_schema.keyring_component_status;`.
Production: use a KMS-backed keyring (Enterprise `component_keyring_kmip`/AWS/
Hashicorp, or Percona's Vault component) rather than a file on the same host.

## Encrypt
```ini
[mysqld]
default_table_encryption = ON         # new schemas/tables encrypted by default
innodb_redo_log_encrypt = ON
innodb_undo_log_encrypt = ON
binlog_encryption = ON
```
```sql
ALTER TABLE appdb.customers ENCRYPTION = 'Y';     -- rebuilds the table (online, INPLACE copy)
ALTER SCHEMA appdb DEFAULT ENCRYPTION = 'Y';
ALTER TABLESPACE mysql ENCRYPTION = 'Y';          -- system tables
SELECT space, name, encryption FROM information_schema.innodb_tablespaces;   -- Y / N
```

## Key rotation
Each tablespace key is encrypted with a master key; rotating the master key only
re-encrypts tablespace keys (fast):
```sql
ALTER INSTANCE ROTATE INNODB MASTER KEY;
ALTER INSTANCE ROTATE BINLOG MASTER KEY;
```

## Gotchas
- **Back up the keyring with every backup** (separately). A physical backup
  of encrypted tablespaces without the matching master key is unrecoverable.
  XtraBackup needs `--keyring-file-data`/component config to back up and prepare.
- Keyring file on the same disk as the data protects little against host compromise.
- Encrypting existing big tables is a full rebuild: plan I/O and disk space.
- Logical dumps (mysqldump) are plaintext; encrypt them separately.

## Verify
The `information_schema.innodb_tablespaces` query shows `encryption = Y` for target
tablespaces; `strings <table>.ibd | grep <known-value>` finds nothing.
