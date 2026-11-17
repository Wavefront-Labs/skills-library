---
id: computing-software.database-administration.oracle-database.profiles-and-password-policies
name: profiles-and-password-policies
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle, oracle-database, oracle-security, oracle-users, oracle-profiles, password-life-time, failed-login-attempts, password-verify-function, ora-28002, service-accounts]
level: practitioner
status: docs-checked
description: "Create Oracle profiles for humans and service accounts: password lifetime, lockout, verify functions, resource limits, and avoiding surprise ORA-28001 expiries in production."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/CREATE-PROFILE.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/dbseg/configuring-authentication.html
  - https://docs.oracle.com/en/error-help/db/ora-28001/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Profiles and password policies

**Goal:** people get rotating, strong passwords and lockout; application schemas
never expire in the middle of the night.

## The DEFAULT profile trap
Every user without an explicit profile gets `DEFAULT`. When a profile omits `PASSWORD_LIFE_TIME`
the documented default is 180 days, and for `PASSWORD_GRACE_TIME` 7 days (check `DBA_PROFILES` for what
your `DEFAULT` profile actually holds). An app account created and
forgotten expires after 180 days: logins warn with ORA-28002 then fail with
`ORA-28001: the password has expired`, often discovered as an outage.

## Separate profiles
```sql
CREATE PROFILE human_users LIMIT
  PASSWORD_LIFE_TIME 90 PASSWORD_GRACE_TIME 7
  PASSWORD_REUSE_MAX 10 PASSWORD_REUSE_TIME 365
  FAILED_LOGIN_ATTEMPTS 5 PASSWORD_LOCK_TIME 1/24          -- 1 hour
  PASSWORD_VERIFY_FUNCTION ora12c_verify_function
  INACTIVE_ACCOUNT_TIME 90                                  -- days; minimum 15
  IDLE_TIME 60;                                             -- minutes; needs RESOURCE_LIMIT=TRUE

CREATE PROFILE app_service LIMIT
  PASSWORD_LIFE_TIME UNLIMITED
  FAILED_LOGIN_ATTEMPTS UNLIMITED      -- or a high number: lockout of an app account = outage
  PASSWORD_VERIFY_FUNCTION ora12c_verify_function;

ALTER USER app_owner PROFILE app_service;
```
`ora12c_verify_function` is the Oracle-supplied default complexity check; a verify function must exist
in the SYS schema (or use your own). Rotate service passwords through a vault, not
by expiry.

## Find risk
```sql
SELECT username, account_status, expiry_date, profile, last_login
FROM dba_users WHERE account_status <> 'OPEN' OR expiry_date < SYSDATE + 30 ORDER BY expiry_date;
SELECT profile, resource_name, limit FROM dba_profiles WHERE profile IN ('DEFAULT','APP_SERVICE') ORDER BY 1,2;
```
Unlock / re-set: `ALTER USER app_owner IDENTIFIED BY "<pw>" ACCOUNT UNLOCK;`


## Gotchas
- Kernel limits (`IDLE_TIME`, `SESSIONS_PER_USER`) only enforce when `RESOURCE_LIMIT = TRUE` (the default); password limits are always enforced.
- A non-zero `PASSWORD_ROLLOVER_TIME` (minimum 1 hour; default 0 = disabled) allows old and new passwords concurrently for rotation; accounts in the window show `IN ROLLOVER` in `DBA_USERS`.

## Verify
No service account in `dba_users` with a non-null `expiry_date`; a test human
account locks after 5 bad passwords.

## Checked
2026-10-31. Confirmed in the 19c SQL Language Reference (CREATE PROFILE) and Database Reference
(`RESOURCE_LIMIT`, `DBA_USERS`, `DBA_PROFILES`) and the ORA-28001 / ORA-28002 error pages:
defaults for `PASSWORD_LIFE_TIME` (180 days), `PASSWORD_GRACE_TIME` (7 days), `PASSWORD_LOCK_TIME`,
`INACTIVE_ACCOUNT_TIME` (minimum 15), `PASSWORD_ROLLOVER_TIME`, `IDLE_TIME`,
`RESOURCE_LIMIT` default, the verify function example and the error texts. Removed: "since 11g",
`ora12c_strong_verify_function` and `utlpwdmg.sql` path, "12.2+" and "21c+" version gates, the CDB
common-profile note and the reuse-rule remark (not confirmed in the fetched pages).
Method: documentation only; no commands were run.
