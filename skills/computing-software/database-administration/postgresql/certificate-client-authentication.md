---
id: computing-software.database-administration.postgresql.certificate-client-authentication
name: certificate-client-authentication
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, client-authentication, cert-authentication, clientcert, mtls, x509, pg-hba-conf, verify-full]
level: advanced
status: docs-checked
description: "Authenticate PostgreSQL clients with X.509 client certificates (cert method or clientcert=verify-full), including CN mapping, CRLs and certificate rotation."
sources:
  - https://www.postgresql.org/docs/18/auth-cert.html
  - https://www.postgresql.org/docs/18/ssl-tcp.html#SSL-CLIENT-CERTIFICATES
  - https://www.postgresql.org/docs/18/auth-pg-hba-conf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Client certificate authentication

**Goal:** services log in with a certificate instead of a password, and revoking
the cert locks them out.

## Server prerequisites
TLS enabled plus `ssl_ca_file = 'client-ca.crt'` (the CA that signs client
certs). Optional `ssl_crl_file` / `ssl_crl_dir` for revocation (CRL entries are checked when either is set). Without `ssl_ca_file`, client certificate verification is not performed.

## Two ways to use client certs (pg_hba.conf)
```
# 1. Cert IS the authentication: CN must equal the DB user (or map via pg_ident)
hostssl  appdb  app_svc  10.0.0.0/8  cert
# 2. Cert required AND a password: belt and braces
hostssl  appdb  all      10.0.0.0/8  scram-sha-256 clientcert=verify-full
```
`clientcert` can be set on any `hostssl` line. `verify-ca` checks the certificate
chain; `verify-full` also requires CN == user name (after mapping). The `cert` method
is effectively `trust` with `clientcert=verify-full`, so adding `clientcert` to it is redundant.

## Mapping CNs to roles
When CNs are hostnames or service ids, use pg_ident.conf:
```
# MAPNAME   SYSTEM-USERNAME              PG-USERNAME
svcmap      /^(.*)\.svc\.example\.com$   \1
```
and `hostssl appdb all 10.0.0.0/8 cert map=svcmap`. `clientname=CN` is the default;
`clientname=DN` matches the whole Distinguished Name instead (best used with a map).

## Client side
Issue the client certificate from your CA with its CN set to the role name (or a mapped name).
Client: `sslmode=verify-full sslcert=app_svc.crt sslkey=app_svc.key sslrootcert=server-ca.crt`.
The private key file must not allow access to world or group (for example `chmod 0600`),
unless it is owned by root with group read (`0640`).

## Gotchas
- The server re-reads the SSL files on configuration reload (`pg_reload_conf()`);
  if an error is found during a reload the files are ignored and the old SSL
  configuration stays in use.
- Short-lived certificates reduce reliance on CRLs; automate renewal.
- A superuser line with `cert` still lets anyone holding that cert in: keep
  superuser access to local socket + peer.

## Verify
```sql
SELECT pid, client_dn, client_serial FROM pg_stat_ssl WHERE client_dn IS NOT NULL;
```
Connecting without a certificate to a `cert` line must fail.

## Checked
2026-10-25. Against PostgreSQL 18 documentation (REL_18_STABLE doc/src/sgml, branch head 2026-10-24; PostgreSQL 19 is still at release-candidate stage): client-authentication chapter (Certificate Authentication: CN compared to the requested user name, `map`, `cert` equivalent to trust with `clientcert=verify-full`; `clientcert` on `hostssl` lines with `verify-ca` and `verify-full`; `clientname=CN|DN`), server SSL chapter (Using Client Certificates, CRL checking via `ssl_crl_file`/`ssl_crl_dir`, SSL files re-read on reload), `ssl_ca_file` default behaviour, libpq key-file permission rule and the `pg_stat_ssl` columns `client_dn` and `client_serial`. Removed the PG14 version gate, the openssl signing commands, the quoted error text and the claim about expired CRL files, which the documentation does not give.
Method: documentation only; no commands were run.
