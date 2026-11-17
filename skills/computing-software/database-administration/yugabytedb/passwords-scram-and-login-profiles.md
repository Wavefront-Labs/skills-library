---
id: computing-software.database-administration.yugabytedb.passwords-scram-and-login-profiles
name: passwords-scram-and-login-profiles
category: computing-software
field: database-administration
product: yugabytedb
tags: [passwords, scram-sha-256, md5-migration, password-encryption, login-profiles, ysql-enable-profile, failed-login-attempts, passwordcheck]
level: practitioner
status: docs-checked
description: "Migrate YSQL passwords from md5 to SCRAM-SHA-256 and lock accounts after failed logins with login profiles and ysql_enable_profile."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/secure/authentication/password-authentication.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/secure/enable-authentication/ysql-login-profiles.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Passwords, SCRAM and login profiles

**SCRAM migration.** `scram-sha-256` (RFC 7677) is the default for new universes. It is a challenge-response scheme that prevents password sniffing and supports storing passwords in the most secure hashed form; md5 prevents sniffing but gives no protection if an attacker obtains the hashes. Passwords live in `pg_authid`.
1. Set `--ysql_pg_conf_csv=password_encryption=scram-sha-256`.
2. Add matching HBA rules, e.g. `--ysql_hba_conf_csv='host all all 0.0.0.0/0 scram-sha-256,host all all ::0/0 scram-sha-256'`.
3. Have every user reset their password so it is stored as SCRAM.
All new or changed passwords are stored as SCRAM; existing ones stay md5 until changed. During the transition keep both md5 and scram rules in `ysql_hba_conf_csv` (the page's example: `host all all 0.0.0.0/0 md5,host all all ::0/0 md5,host all all 0.0.0.0/0 scram-sha-256,host all all ::0/0 scram-sha-256`), and remove the md5 rules once all passwords are migrated. An md5 rule falls back to SCRAM automatically for users whose stored password is SCRAM.
Audit progress as a superuser (only superusers can read `pg_authid`) by checking `rolpassword LIKE 'SCRAM-SHA-256%'` versus `'md5%'` for roles with `rolcanlogin`; for each md5 role use `ALTER ROLE` or `\password` to set a new password. The `passwordcheck` extension can enforce strong passwords on `CREATE ROLE` and `ALTER ROLE`, but only for passwords given in plain text.
Lost admin password: restart yb-tserver with `--ysql_hba_conf_csv` containing `host all yugabyte 0.0.0.0/0 trust,host all all 0.0.0.0/0 md5,host all yugabyte ::0/0 trust,host all all ::0/0 md5`, run `ALTER ROLE yugabyte WITH PASSWORD '...'`, then roll the flag back and restart.

**Login profiles** lock accounts after failed attempts.
- Start tservers with `--ysql_enable_profile=true` (with `--ysql_enable_auth=true`).
- `CREATE PROFILE myprofile LIMIT FAILED_LOGIN_ATTEMPTS 3;` (`PASSWORD_LOCK_TIME` is optional and timed locking is not supported yet; a locked role stays locked until an administrator unlocks it). View profiles in `pg_yb_profile` and per-role state in `pg_yb_role_profile`.
- `ALTER ROLE myuser PROFILE myprofile;` to attach, `ALTER ROLE myuser NOPROFILE;` to detach.
- Only superusers create or drop profiles and assign roles.
- There is no default profile; roles with no profile have unlimited attempts.
- Detach roles with `NOPROFILE` before `DROP ROLE`. Unlock with `ALTER ROLE myuser ACCOUNT UNLOCK` (and `ACCOUNT LOCK` locks a role manually); a successful login or an unlock resets the failed-attempt count to 0. If every role including administrators is locked, restart the cluster with `--ysql_enable_profile` off, create a new superuser, restart with it on, and unlock from the new superuser (profile commands do not run while the flag is off).
- Limits: a profile cannot be changed with `ALTER PROFILE` (create a new one); profiles apply only to challenge-response methods, so they are ignored for trust, reject, peer and similar methods; with cluster SSL mode `allow` or `prefer`, one login attempt can count as two failures.

## Checked

2026-11-04. Confirmed against the Password authentication page (SCRAM default for new universes, md5 versus SCRAM, ysql_pg_conf_csv and ysql_hba_conf_csv steps, md5 fallback, migration rules and audit query, passwordcheck, password reset procedure) and the YSQL login profiles page (ysql_enable_profile, CREATE PROFILE syntax and optional untimed PASSWORD_LOCK_TIME, ALTER ROLE PROFILE/NOPROFILE, ACCOUNT LOCK/UNLOCK, superuser-only, no default profile, lockout recovery, catalog tables and limitations). Removed 'salted verifier' (the page does not say it) and added the unlock, recovery and limitation details.

Method: documentation only; no commands were run.
