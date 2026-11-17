---
id: computing-software.database-administration.postgresql.pam-and-radius-authentication
name: pam-and-radius-authentication
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, pam-authentication, radius, pg-hba-conf, client-authentication, external-authentication]
level: practitioner
status: docs-checked
description: "Authenticate PostgreSQL logins against PAM (system accounts, SSSD, LDAP via PAM) or RADIUS, with pg_hba setup, the PAM service file and failure modes."
sources:
  - https://www.postgresql.org/docs/18/auth-pam.html
  - https://www.postgresql.org/docs/18/auth-radius.html
  - https://www.postgresql.org/docs/devel/release-19.html
  - https://www.postgresql.org/docs/18/auth-pg-hba-conf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PAM and RADIUS authentication

Both are **password** methods: the client sends the cleartext password to the server, which forwards it to PAM/RADIUS. Always pair them with `hostssl` lines.

## PAM
```
# pg_hba.conf
hostssl all all 10.0.0.0/8 pam pamservice=postgresql
```
```
# /etc/pam.d/postgresql
auth     required pam_sss.so          # or pam_unix.so / pam_ldap.so
account  required pam_sss.so
```
- The role must still exist in PostgreSQL (`CREATE ROLE alice LOGIN;`); PAM checks the password only.
- PAM that reads `/etc/shadow` (for example `pam_unix.so`) fails, because the server runs as a non-root user; configure PAM to use LDAP or another method instead.
- `pam_use_hostname=1` passes the resolved client host name instead of the IP address to PAM modules (the `PAM_RHOST` item). Name resolution can delay logins, and most PAM configurations do not use this item.

## RADIUS
```
hostssl all all 10.0.0.0/8 radius radiusservers="10.1.1.5,10.1.1.6" radiussecrets="<SHARED_SECRET>" radiusports="1812" radiusidentifiers="postgresql"
```
- To list several servers, separate them with commas and surround the list with double quotes; they are tried in order, and the other options can then be per-server comma-separated lists. `radiusservers` and `radiussecrets` are required; the port defaults to 1812 and the NAS identifier to `postgresql`. The secret should be at least 16 characters.
- PostgreSQL sends an Authenticate Only Access Request and acts on Access Accept or Access Reject; RADIUS accounting is not supported.
- RADIUS authentication is removed in PostgreSQL 19: its release notes say only RADIUS over UDP was supported, which is unfixably insecure (checked against the 19 release candidate documentation; it is present in 18). Prefer LDAP, GSSAPI or certificates for new designs.

## Debug
```ini
log_connections = on
```
The server log shows why the login failed; on the host, the system authentication log shows the PAM side.

## Verify
```bash
psql "host=db1 sslmode=verify-full user=alice dbname=app" -c "SELECT current_user, ssl FROM pg_stat_ssl WHERE pid=pg_backend_pid()"
```

## Gotchas
- PAM and RADIUS only validate user name and password pairs; the role must already exist in the database.

## Checked
2026-10-25. Against PostgreSQL 18 documentation (REL_18_STABLE doc/src/sgml, branch head 2026-10-24; PostgreSQL 19 is still at release-candidate stage) and the PostgreSQL 19 release-candidate release notes: PAM Authentication section (`pamservice` default `postgresql`, `pam_use_hostname` and `PAM_RHOST`, `/etc/shadow` failure for a non-root server, user must already exist) and RADIUS Authentication section (Authenticate Only request, Accept or Reject, comma-separated quoted lists, `radiusservers`/`radiussecrets` required, default port 1812, default identifier `postgresql`, 16-character secret recommendation). Corrected: the previous text said RADIUS was only deprecated; the 19 release notes list its removal. Removed the `pam_faillock`, PgBouncer, 2FA-prompt and log-text claims, which the documentation does not give.
Method: documentation only; no commands were run.
