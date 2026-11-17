---
id: computing-software.systems-network-administration.openldap.quick-start-cn-config
name: quick-start-cn-config
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, quick-start, first-entries, slapd-ldif, slapadd, cn-config]
level: intro
status: docs-checked
description: "Bring up a first OpenLDAP slapd with an MDB database via cn=config: edit slapd.ldif, slapadd it, start slapd, and load the first entries."
sources:
  - https://www.openldap.org/doc/admin26/quickstart.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# quick start with cn=config
Build: `./configure && make depend && make && make test`, then `make install` as root (default prefix `/usr/local`).

1. Edit the shipped `slapd.ldif` so it has an MDB database:
```
dn: olcDatabase=mdb,cn=config
objectClass: olcDatabaseConfig
objectClass: olcMdbConfig
olcDatabase: mdb
OlcDbMaxSize: 1073741824
olcSuffix: dc=example,dc=com
olcRootDN: cn=Manager,dc=example,dc=com
olcRootPW: secret
olcDbDirectory: /usr/local/var/openldap-data
olcDbIndex: objectClass eq
```
The `olcDbDirectory` must exist before slapd starts.

2. Import: `slapadd -n 0 -F /usr/local/etc/slapd.d -l /usr/local/etc/openldap/slapd.ldif`
3. Start: `/usr/local/libexec/slapd -F /usr/local/etc/slapd.d`
4. Check: `ldapsearch -x -b '' -s base '(objectclass=*)' namingContexts` should return `namingContexts: dc=example,dc=com`. Use single quotes.
5. Create `example.ldif` with a `dcObject`/`organization` entry for `dc=example,dc=com` and an `organizationalRole` for `cn=Manager`, then load it:
`ldapadd -x -D "cn=Manager,dc=example,dc=com" -W -f example.ldif`
6. Verify: `ldapsearch -x -b 'dc=example,dc=com' '(objectclass=*)'`

Gotcha: by default everyone except the super-user gets read access, and the sample uses a plaintext `secret` with no TLS. Restrict access with ACLs and read the Security Considerations, SASL and TLS chapters before production.

## Checked

2026-11-09. Confirmed against the OpenLDAP 2.6 Admin Guide quick-start chapter (build steps, MDB slapd.ldif entry, olcDbDirectory must exist, slapadd -n 0 -F, slapd -F, namingContexts check with single quotes, example entries, ldapadd and ldapsearch commands, default read access). Removed the unsourced advice to hash the password.

Method: documentation only; no commands were run.

