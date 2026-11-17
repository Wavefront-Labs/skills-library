---
id: computing-software.systems-network-administration.linux.openldap-slapd-server-cn-config
name: openldap-slapd-server-cn-config
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, slapd, openldap-server, cn-config, olc, ldapmodify, slapcat, ldap-replication]
level: practitioner
status: draft
description: "Run an OpenLDAP server: install slapd, manage the cn=config (OLC) backend with ldapmodify, add schemas, indexes, ACLs, TLS, backups with slapcat and syncrepl replication."
sources:
  - https://www.openldap.org/doc/admin26/slapdconf2.html
  - https://www.openldap.org/doc/admin26/access-control.html
  - https://www.openldap.org/doc/admin26/replication.html
  - https://ubuntu.com/server/docs/install-and-configure-ldap
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# OpenLDAP server (slapd) with cn=config

**Goal:** a directory server you configure live through LDAP itself, never by editing `slapd.d` files by hand.

## Install
```bash
apt install slapd ldap-utils && dpkg-reconfigure slapd    # sets suffix dc=example,dc=com and admin pw
# RHEL family: openldap-servers ships in EPEL / use 389-ds as the Red Hat-supported server
systemctl enable --now slapd
ldapsearch -Q -LLL -Y EXTERNAL -H ldapi:/// -b cn=config dn   # root via SASL EXTERNAL over the unix socket
```
`cn=config` lives in `/etc/ldap/slapd.d` (Debian) or `/etc/openldap/slapd.d`. Hand edits break the CRC checksums; always change it with `ldapmodify -Y EXTERNAL -H ldapi:///`.

## Common changes (LDIF)
```ldif
# index.ldif - add equality indexes for lookups sssd does
dn: olcDatabase={1}mdb,cn=config
changetype: modify
add: olcDbIndex
olcDbIndex: uid,memberUid,uniqueMember eq
-
replace: olcDbMaxSize
olcDbMaxSize: 10737418240
```
```bash
ldapmodify -Y EXTERNAL -H ldapi:/// -f index.ldif
ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/ldap/schema/ppolicy.ldif   # schemas are added, never modified
```
- Database numbers (`{1}mdb`) vary; find them with `ldapsearch ... -b cn=config '(olcDatabase=*)' dn`.
- MDB `olcDbMaxSize` must exceed data size or writes fail with `MDB_MAP_FULL`.

## ACLs (olcAccess) - first match wins, order matters
```ldif
dn: olcDatabase={1}mdb,cn=config
changetype: modify
replace: olcAccess
olcAccess: {0}to attrs=userPassword by self write by anonymous auth by * none
olcAccess: {1}to * by dn.exact="cn=sssd,ou=svc,dc=example,dc=com" read by users read by * none
```

## TLS
Set `olcTLSCertificateFile`, `olcTLSCertificateKeyFile`, `olcTLSCACertificateFile` on `cn=config`; the key must be readable by the `openldap`/`ldap` user. Test with `ldapsearch -ZZ -H ldap://ldap.example.com -x -b '' -s base`. Require TLS with `olcSecurity: tls=1`.

## Backup and restore
```bash
slapcat -n 0 -l config.ldif          # config DB
slapcat -n 1 -l data.ldif            # data DB (safe while running on mdb)
# restore: stop slapd, empty the DB dir, slapadd -n 1 -F /etc/ldap/slapd.d -l data.ldif, chown -R openldap:
```

## Replication (syncrepl)
Load `syncprov` overlay on the provider; on the consumer add `olcSyncrepl: rid=001 provider=ldaps://ldap1 bindmethod=simple binddn=... credentials=... searchbase=dc=example,dc=com type=refreshAndPersist retry="60 +"`. Multi-provider needs `olcServerID` and `olcMultiProvider: TRUE` (2.5+) on every node.

## Verify
- [ ] `ldapwhoami -x -D uid=alice,... -W -ZZ` works; anonymous read of `userPassword` returns nothing.
- [ ] `contextCSN` matches on provider and consumer after a change.
