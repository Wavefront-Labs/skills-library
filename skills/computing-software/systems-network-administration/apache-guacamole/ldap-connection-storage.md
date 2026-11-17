---
id: computing-software.systems-network-administration.apache-guacamole.ldap-connection-storage
name: ldap-connection-storage
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, ldap, guacconfiggroup, ldap-schema, ldap-config-base-dn, guacconfigprotocol, guacconfigparameter, openldap, ldapadd]
level: advanced
status: draft
description: "Store Guacamole connections in LDAP as guacConfigGroup entries: install the OpenLDAP schema with ldapadd, attributes, membership, ldap-config-base-dn, and AD schema notes."
sources:
  - https://guacamole.apache.org/doc/gug/ldap-auth.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Connections stored in LDAP

Database storage is the recommended approach, but connections can live in LDAP.

1. Install the schema (OpenLDAP, run as root):
```
ldapadd -Q -Y EXTERNAL -H ldapi:/// -f schema/guacConfigGroup.ldif
```
Verify with `ldapsearch` on `cn=schema,cn=config` and look for `cn={4}guacConfigGroup` (the number depends on your server). Other servers use `guacConfigGroup.schema` (RFC-2252 compliant). For Active Directory, apply the standards-compliant schema file through AD's own schema-update process.
2. Set `ldap-config-base-dn` in `guacamole.properties` (omit it and connections are not read from LDAP).
3. Create one `guacConfigGroup` entry per connection (extends `groupOfNames`):
- `guacConfigProtocol` (required once), e.g. `vnc`, `rdp`
- `guacConfigParameter` (repeatable), form `name=value`
- optional once each: `guacConfigProxyHostname`, `guacConfigProxyPort`, `guacConfigProxyEncryption` (`NONE` or `SSL`)
- `member`: users allowed to use it; groups under `ldap-group-base-dn` can be added through `seeAlso`.

Example parameter values: `hostname=10.0.0.10`, `port=5900`.

Parameter tokens like `${LDAP_...}` become available when `ldap-user-attributes` is set (apache-guacamole.parameter-tokens).

Verify: a member sees the connection on login; a non-member does not.
