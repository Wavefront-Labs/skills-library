---
id: computing-software.database-administration.postgresql.gssapi-kerberos-authentication
name: gssapi-kerberos-authentication
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, gssapi-authentication, kerberos, keytab, active-directory, pg-hba-conf, client-authentication]
level: practitioner
status: docs-checked
description: "Configure PostgreSQL GSSAPI (Kerberos/Active Directory) authentication: service principal, keytab, pg_hba gss lines, realm mapping and client tickets."
sources:
  - https://www.postgresql.org/docs/18/gssapi-auth.html
  - https://www.postgresql.org/docs/18/runtime-config-connection.html#GUC-KRB-SERVER-KEYFILE
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/ktpass
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/setspn
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GSSAPI / Kerberos authentication

## Prerequisites
- Server principal `postgres/<db-fqdn>@REALM` (service name `postgres` by default; clients change it with the libpq `krbsrvname` connection parameter). Clients must connect using the fully qualified host name that appears in the principal.
- Forward and reverse DNS consistent; clocks synchronised (NTP), as Kerberos requires.

## 1. Keytab
MIT KDC:
```bash
kadmin -q "addprinc -randkey postgres/db1.example.com"
kadmin -q "ktadd -k /etc/postgresql/krb5.keytab postgres/db1.example.com"
```
Active Directory (service account `svc-pg`):
```powershell
setspn -S postgres/db1.example.com svc-pg
ktpass /princ postgres/db1.example.com@EXAMPLE.COM /mapuser svc-pg /crypto AES256-SHA1 /ptype KRB5_NT_PRINCIPAL /pass * /out krb5.keytab
```
```bash
chown postgres:postgres /etc/postgresql/krb5.keytab && chmod 600 /etc/postgresql/krb5.keytab
```
```ini
# postgresql.conf
krb_server_keyfile = '/etc/postgresql/krb5.keytab'
```

## 2. pg_hba.conf
```
hostgssenc all all 10.0.0.0/8  gss include_realm=0 krb_realm=EXAMPLE.COM
host       all all 10.0.0.0/8  gss map=krb
```
- `include_realm=0` strips `@EXAMPLE.COM` so principal `alice@EXAMPLE.COM` logs in as role `alice`. The docs discourage it (backwards compatibility only): it is secure only in a single-realm setup with `krb_realm` set; an explicit `pg_ident.conf` map is recommended.
- `hostgssenc` matches only connections made with GSSAPI encryption; `host` + `gss` also matches connections without it. GSSAPI or TLS encryption is needed for the data to be encrypted.
- Mapping with pg_ident.conf: `krb  /^(.*)@EXAMPLE\.COM$  \1`.
- Roles must exist (`CREATE ROLE alice LOGIN;`); no password needed.

## 3. Client
```bash
kinit alice@EXAMPLE.COM
psql "host=db1.example.com dbname=app gssencmode=prefer"
klist                                 # should now show a postgres/db1... service ticket
```

## Troubleshooting
| Symptom | Likely cause |
|---|---|
| authentication fails, server principal not found | client connected by IP or alias instead of the FQDN in the principal |
| authentication fails after an AD password reset or a new `ktadd` | keytab outdated; re-export it |
| server cannot accept the security context | keytab unreadable by the server account, wrong `krb_server_keyfile` path, or encryption-type mismatch |
| works in psql, fails from the app | the app's OS user has no ticket cache; use a keytab-based client login (`kinit -kt`) |

Set `log_connections = on` and read the server log for the failure detail.

## Gotchas
- Kerberos proves identity only; still restrict by CIDR and grant least privilege.
- Behind a load balancer/VIP, every name clients use needs an SPN in the keytab.

## Checked
2026-10-25. Against PostgreSQL 18 documentation (REL_18_STABLE doc/src/sgml, branch head 2026-10-24; PostgreSQL 19 is still at release-candidate stage): GSSAPI Authentication section (service principal format `servicename/hostname@realm`, `krb_server_keyfile`, separate keytab recommendation, MIT `kadmin` example, `include_realm`, `krb_realm`, `map`), `hostgssenc` record type, libpq `krbsrvname` and `gssencmode`, and Microsoft's `ktpass` and `setspn` command references (switch spellings `/princ`, `/mapuser`, `/crypto AES256-SHA1`, `/ptype KRB5_NT_PRINCIPAL`, `/pass *`, `/out`; `setspn -S` checks for duplicate SPNs). Corrected: the service name is changed with the libpq `krbsrvname` parameter, not a server `krb_srvname` setting; ktpass switches use `/`. Removed the 5-minute clock-skew figure, the `KRB5_TRACE` tip and the quoted error strings, which the documentation does not give.
Method: documentation only; no commands were run.
