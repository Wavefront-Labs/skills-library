---
id: computing-software.systems-network-administration.openldap.cn-config-structure
name: cn-config-structure
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, cn-config, olcdatabase, dynamic-modules, slapd-d, olcmoduleload]
level: practitioner
status: docs-checked
description: "Read and edit the OpenLDAP cn=config tree: global entry, modules, schema, backends and databases, with olc attribute defaults and module loading."
sources:
  - https://www.openldap.org/doc/admin26/slapdconf2.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cn=config structure
Entries:
- `cn=config` (objectClass `olcGlobal`): global settings.
- `cn=module{N},cn=config` (`olcModuleList`): dynamic modules, only if built with `--enable-modules`.
- `cn=schema,cn=config` (`olcSchemaConfig`): built-in schema; children hold user schema.
- `olcBackend=<type>,cn=config`: per-backend settings.
- `olcDatabase={X}<type>,cn=config`: a database; overlays are its children. `frontend` holds settings applied to all databases; `config` always exists implicitly.

The `{X}` index fixes ordering and is generated automatically. Most attributes are the `olc` prefix plus the slapd.conf keyword. Never edit the LDIF files directly: use ldapadd/ldapmodify/ldapdelete on a running server, or slapadd/slapmodify offline.

Global defaults: `olcIdleTimeout` 0 (off), `olcLogLevel` stats, `olcSizeLimit` 500, `olcTimeLimit` 3600, `olcReadonly` FALSE.

Load a module:
```
dn: cn=module{1},cn=config
objectClass: olcModuleList
cn: module{1}
olcModulePath: /usr/local/lib:/usr/local/lib/slapd
olcModuleLoad: accesslog.la
```
Backend types include mdb, ldap, ldif, meta, monitor, sql, wt.

## Checked

2026-11-04. Confirmed against the OpenLDAP 2.6 Administrator's Guide slapd-config chapter and slapd-config(5): entry types and object classes (olcGlobal, olcModuleList needing --enable-modules, olcSchemaConfig, olcBackendConfig, olcDatabase={X}<type>), frontend and config databases created implicitly, automatic {X} indexes, never editing LDIF directly (ldapadd, ldapmodify, ldapdelete online; slapadd, slapmodify offline), defaults for idle timeout, log level stats, size and time limit, readonly, module example, overlay entries as children of a database entry. Removed the Verify command and the SASL-over-rootpw advice, which those pages do not state.

Method: documentation only; no commands were run.
