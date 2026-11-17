---
id: computing-software.database-administration.oracle-database.centrally-managed-users-with-active-directory
name: centrally-managed-users-with-active-directory
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, centrally-managed-users, cmu, active-directory, ldap-directory-access, global-users, kerberos, dsi-ora]
level: advanced
status: docs-checked
description: "Authenticate Oracle 18c+ users against Active Directory with centrally managed users (CMU): dsi.ora, AD service account, wallet, and mapping AD users and groups."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/dbseg/configuring-oracle-database-microsoft-active-directory-integration.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/dbseg/configuring-authorization-centrally-managed-users.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Centrally managed users (CMU) with Active Directory

CMU (18c+) lets the database talk directly to AD (no Oracle Internet Directory / Enterprise User
Security). AD users log in with AD password, Kerberos or certificates, mapped to exclusive
database users or shared schemas by AD group, and AD groups map to database roles.

## Prepare AD
- Create an AD service account for the database (e.g. `svc-oradb`) with read access to users and groups;
  for password authentication it needs to read the Oracle password verifier.
- Password auth: run `opwdintg.exe` on every Windows domain controller (OS language must be English). It installs the Oracle password filter, extends the AD schema once (irreversible unless the schema was backed up), adds the `orclCommonAttribute` verifier attribute and creates the verifier groups `ORA_VFR_MD5`, `ORA_VFR_11G`, `ORA_VFR_12C`; reboot the DC afterwards. Not needed for Kerberos or SSL (certificate) authentication.

## Configure the database host
`dsi.ora` identifies the AD servers (use it instead of `ldap.ora` for CMU). It is searched for in the PDB's wallet location first, then fallback directories; Oracle advises keeping it outside `$ORACLE_HOME`. Format is `host:port:sslport`, fully qualified names:
```
DSI_DIRECTORY_SERVERS = (dc1.corp.example.com:389:636, dc2.corp.example.com:389:636)
DSI_DEFAULT_ADMIN_CONTEXT = "DC=corp,DC=example,DC=com"   # optional: search base; Oracle recommends omitting it unless you must limit the search scope
DSI_DIRECTORY_SERVER_TYPE = AD                           # must be upper case AD
```
Wallet with the service account credentials and the AD CA certificate:
```bash
orapki wallet create -wallet $ORACLE_BASE/admin/ORCL/wallet -auto_login
mkstore -wrl $ORACLE_BASE/admin/ORCL/wallet -createEntry ORACLE.SECURITY.USERNAME svc-oradb
mkstore -wrl $ORACLE_BASE/admin/ORCL/wallet -createEntry ORACLE.SECURITY.DN "CN=svc-oradb,OU=Svc,DC=corp,DC=example,DC=com"
mkstore -wrl $ORACLE_BASE/admin/ORCL/wallet -createEntry ORACLE.SECURITY.PASSWORD "<SECRET>"
orapki wallet add -wallet $ORACLE_BASE/admin/ORCL/wallet -trusted_cert -cert ad_root_ca.cer
orapki wallet display -wallet $ORACLE_BASE/admin/ORCL/wallet
```
```sql
-- in each PDB (not the CDB root); valid values PASSWORD or NONE (PASSWORD needs the AD server certificate and wallet credentials)
ALTER SYSTEM SET LDAP_DIRECTORY_ACCESS = 'PASSWORD';
ALTER SYSTEM SET LDAP_DIRECTORY_SYSAUTH = YES SCOPE = SPFILE;       -- only if AD users get SYSDBA/SYSOPER etc.; restart or reopen the PDB
```

## Map users and groups
```sql
-- exclusive mapping
CREATE USER jsmith IDENTIFIED GLOBALLY AS 'CN=John Smith,OU=Staff,DC=corp,DC=example,DC=com';
-- shared schema by AD group (DN of the group)
CREATE USER app_readers IDENTIFIED GLOBALLY AS 'CN=ora-readers,OU=Groups,DC=corp,DC=example,DC=com';
-- AD group -> role
CREATE ROLE dba_ad IDENTIFIED GLOBALLY AS 'CN=ora-dbas,OU=Groups,DC=corp,DC=example,DC=com';
```
An exclusive mapping overrides shared mappings; if several shared mappings match, the schema with the lowest USER_ID wins, so keep one mapping per user. SYSOPER/SYSBACKUP and similar cannot be granted through global roles, only to a schema.
Check how a session was mapped: `SELECT SYS_CONTEXT('USERENV','IDENTIFICATION_TYPE') FROM dual;` (GLOBAL EXCLUSIVE or GLOBAL SHARED).

## Troubleshooting
- Check `dsi.ora`, the wallet entries (`orapki wallet display`) and DC reachability on the SSL port first. Wallet changes take effect without a restart.
- Password login needs the password filter on every DC; Kerberos and SSL do not.

## Verify
An AD user in the mapped group connects, gets the mapped role, and disabling them in AD blocks the next login.

## Checked
Date 2026-10-22. Oracle Database 19c Security Guide (Configuring the Oracle Database-Microsoft Active Directory
Integration; Configuring Authorization for Centrally Managed Users, via search summary). Confirmed: dsi.ora parameters and
format, wallet entries ORACLE.SECURITY.USERNAME/DN/PASSWORD, LDAP_DIRECTORY_ACCESS values PASSWORD/NONE,
LDAP_DIRECTORY_SYSAUTH, opwdintg.exe behaviour, exclusive vs shared mapping precedence, IDENTIFICATION_TYPE values.
Corrected: wallet is created with `orapki wallet create -auto_login`; `SSL` is not a documented LDAP_DIRECTORY_ACCESS value;
DSI_DEFAULT_ADMIN_CONTEXT is optional. Removed unconfirmed ORA error meanings, the 28033 event, login string forms.
Not stated in the pages read: the release that introduced CMU (the 18 documentation set contains the page).
Method: documentation only; no commands were run.
