---
id: computing-software.cybersecurity-defensive.system-hardening.oracle-database-hardening
name: oracle-database-hardening
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [oracle-database-hardening, oracle, database-hardening, unified-auditing, dbsat, tde, listener-security]
level: advanced
status: draft
description: "Harden Oracle Database: default accounts, profiles, least privilege and PUBLIC grants, listener and network encryption, unified auditing, TDE, DBSAT and CPU patching."
sources: ["https://docs.oracle.com/en/database/oracle/oracle-database/19/dbseg/index.html", "https://www.oracle.com/database/technologies/security/dbsat.html", "https://www.cisecurity.org/benchmark/oracle_database", "https://www.oracle.com/security-alerts/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Oracle Database hardening

## Assess first: DBSAT
Oracle Database Security Assessment Tool (free) collects configuration and reports findings mapped to CIS,
STIG and GDPR:
```bash
./dbsat collect -n system/<pw>@//dbhost:1521/PDB1 pdb1_collect
./dbsat report -a -n pdb1_collect
./dbsat discover -c dbsat.config pdb1_discover     # sensitive data discovery
```
Work through High risk findings first.

## Accounts and profiles
- Lock and expire unused default accounts (`DBA_USERS_WITH_DEFPWD` lists accounts still on default passwords;
  sample schemas like SCOTT, HR should not exist in production).
- Schema-only accounts (no password, 18c+) for application schema owners: `ALTER USER app_owner NO AUTHENTICATION;`
- Profiles: `FAILED_LOGIN_ATTEMPTS`, `PASSWORD_LIFE_TIME`, `PASSWORD_REUSE_MAX`, `PASSWORD_VERIFY_FUNCTION
  ora12c_strong_verify_function`, `INACTIVE_ACCOUNT_TIME`.
- Separate named DBA accounts; restrict SYSDBA (password file, OS group membership) and audit its use.

## Least privilege
- Application runtime user gets object grants on the schema owner's tables (or via roles), not `DBA`,
  `RESOURCE` with unlimited tablespace, or `ANY` system privileges (`SELECT ANY TABLE`, `EXECUTE ANY PROCEDURE`).
- Revoke risky `PUBLIC` execute grants where not needed (CIS list includes `UTL_FILE`, `UTL_TCP`, `UTL_HTTP`,
  `UTL_SMTP`, `DBMS_JAVA`, `DBMS_SQL` review, `DBMS_RANDOM`...) after testing; network ACLs (DBMS_NETWORK_ACL_ADMIN)
  restrict outbound calls from PL/SQL.
- Privilege Analysis (`DBMS_PRIVILEGE_CAPTURE`, included in EE since 2018) records used privileges to trim
  grants.
- `O7_DICTIONARY_ACCESSIBILITY = FALSE` (default; parameter removed in 19c), `SEC_CASE_SENSITIVE_LOGON` default.

## Network and listener
- Listener on private interfaces; `ADMIN_RESTRICTIONS_LISTENER=ON`; valid node checking
  (`TCP.VALIDNODE_CHECKING=YES`, `TCP.INVITED_NODES`) in sqlnet.ora.
- Native network encryption (`SQLNET.ENCRYPTION_SERVER=REQUIRED`, AES256) or TLS (TCPS); `SQLNET.ALLOWED_LOGON_VERSION_SERVER=12a`
  to ban old password verifiers.
- Remove or restrict XDB HTTP/FTP ports if unused (`DBMS_XDB_CONFIG.SETHTTPPORT(0)`).

## Auditing
Unified Auditing with predefined policies (`ORA_SECURECONFIG`, `ORA_LOGON_FAILURES`, `ORA_ACCOUNT_MGMT`) plus
custom policies for sensitive tables; send to SIEM (Audit Vault or syslog via `UNIFIED_AUDIT_SYSTEMLOG`);
purge with `DBMS_AUDIT_MGMT`, protect the audit trail.

## Encryption
Transparent Data Encryption (Advanced Security option) for tablespaces, keystore in wallet/OKV/HSM; RMAN backup
encryption.

## Patching
Apply quarterly Critical Patch Updates / Release Updates; track Oracle security alerts.

## Verify
DBSAT report has no High findings; `DBA_USERS_WITH_DEFPWD` returns no open accounts; app user lacks `ANY`
privileges; unified audit records logon failures.
