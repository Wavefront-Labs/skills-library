---
id: computing-software.database-administration.sql-server.column-encryption-with-symmetric-keys
name: column-encryption-with-symmetric-keys
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, encryptbykey, decryptbykey, cell-level-encryption, symmetric-key, database-master-key, certificate]
level: advanced
status: docs-checked
description: "Encrypt individual SQL Server columns with EncryptByKey: build the master key, certificate and symmetric key hierarchy, query encrypted data, and back up the keys."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/security/encryption/encrypt-a-column-of-data
  - https://learn.microsoft.com/en-us/sql/relational-databases/security/encryption/encryption-hierarchy
  - https://learn.microsoft.com/en-us/sql/t-sql/functions/encryptbykey-transact-sql
  - https://learn.microsoft.com/en-us/sql/t-sql/functions/decryptbykey-transact-sql
  - https://learn.microsoft.com/en-us/sql/t-sql/functions/decryptbykeyautocert-transact-sql
  - https://learn.microsoft.com/en-us/sql/relational-databases/security/encryption/restore-a-database-master-key
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Column-level encryption with symmetric keys

Cell-level encryption predates Always Encrypted: the engine encrypts, so DBAs with key access
can read plaintext. Use it when the threat is stolen backups/files of specific columns and
Always Encrypted's client changes are not possible.

## Key hierarchy
```sql
USE appdb;
CREATE MASTER KEY ENCRYPTION BY PASSWORD = '<STRONG_SECRET>';
CREATE CERTIFICATE cert_pii WITH SUBJECT = 'PII column key protector';
CREATE SYMMETRIC KEY sk_pii WITH ALGORITHM = AES_256 ENCRYPTION BY CERTIFICATE cert_pii;
```
The database master key is itself protected by the service master key, so the key opens
automatically on this instance.

## Encrypt a column
```sql
ALTER TABLE dbo.Customer ADD NationalId_enc varbinary(160);
OPEN SYMMETRIC KEY sk_pii DECRYPTION BY CERTIFICATE cert_pii;
UPDATE dbo.Customer
SET NationalId_enc = EncryptByKey(Key_GUID('sk_pii'), NationalId, 1, CONVERT(varbinary, CustomerId));
CLOSE SYMMETRIC KEY sk_pii;
-- after verifying: drop the plaintext column
```
The authenticator (third argument `1` turns it on, fourth argument here the primary key) stops whole-value substitution: an attacker copying a ciphertext
from one row to another. Use a unique, unchanging column, because if the authenticator value changes you can lose access to the data. Ciphertext is larger than plaintext; `EncryptByKey` returns `varbinary` of up to 8,000 bytes, so size the column generously.

## Read it
```sql
OPEN SYMMETRIC KEY sk_pii DECRYPTION BY CERTIFICATE cert_pii;
SELECT CustomerId,
       CONVERT(nvarchar(20), DecryptByKey(NationalId_enc, 1, CONVERT(varbinary, CustomerId))) AS NationalId
FROM dbo.Customer;
CLOSE SYMMETRIC KEY sk_pii;
```
`DecryptByKeyAutoCert(cert_ID('cert_pii'), NULL, col)` opens the key inline (handy in views).
Grant access with `GRANT CONTROL ON CERTIFICATE::cert_pii` and `GRANT VIEW DEFINITION ON SYMMETRIC KEY::sk_pii`.
`EncryptByKey` returns NULL if the key is not open or does not exist, and `DecryptByKey` returns NULL if the key is not open or the authenticator does not match: there is no error, so test as the application login.

## Searching
To search an encrypted column a common approach is an indexed hash column
(`HASHBYTES('SHA2_256', @salt + value)`); weigh what the hash leaks.

## Back up keys (or lose the data)
```sql
BACKUP MASTER KEY TO FILE = '<KEY_BACKUP_DIR>/appdb_dmk.key' ENCRYPTION BY PASSWORD = '<SECRET>';
BACKUP CERTIFICATE cert_pii TO FILE = '<KEY_BACKUP_DIR>/cert_pii.cer'
  WITH PRIVATE KEY (FILE = '<KEY_BACKUP_DIR>/cert_pii.pvk', ENCRYPTION BY PASSWORD = '<SECRET>');
```
To move the database master key to another server see the Restore a Database Master Key page (`RESTORE MASTER KEY` takes the backup file, its password and a new password); a restored key that was protected by the service master key is protected by the new instance's service master key.

## Verify
`SELECT * FROM sys.symmetric_keys;` and a decrypt round trip on a restored copy.

## Checked

2026-10-22. Documentation release checked: SQL Server 2025 (17.x) via learn.microsoft.com (ver17 pages; 2022 noted where relevant).
Confirmed: ENCRYPTBYKEY page for SQL Server 2025 (syntax key_GUID, cleartext, add_authenticator, authenticator; varbinary up to 8,000 bytes; NULL when the key is not open; authenticator rationale and the warning that changing it can lose access), DECRYPTBYKEY (NULL when key not open, authenticator must match), DECRYPTBYKEYAUTOCERT (CONTROL on the certificate and VIEW DEFINITION on the key), BACKUP MASTER KEY and RESTORE MASTER KEY pages. Removed as unconfirmed: the ciphertext-size formula pointer, the 'ciphertext is randomised' statement, the OPEN MASTER KEY / ADD ENCRYPTION BY SERVICE MASTER KEY recipe and the algorithm_desc/key_length column names.
Method: documentation only; no commands were run.
