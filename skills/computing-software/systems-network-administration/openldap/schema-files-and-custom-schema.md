---
id: computing-software.systems-network-administration.openldap.schema-files-and-custom-schema
name: schema-files-and-custom-schema
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, schema, attributetype, objectclass-definition, oid, objectidentifier, olcschemaconfig]
level: advanced
status: docs-checked
description: "Load OpenLDAP schema files and define custom attributeTypes and objectClasses: OID allocation, name prefixes, local.schema, objectIdentifier macros, cn=config schema entries."
sources:
  - https://www.openldap.org/doc/admin26/schema.html
  - https://www.openldap.org/doc/admin26/slapdconf2.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# schema files and custom schema
Distributed files (in `/usr/local/etc/openldap/schema`): `core.schema` (required), `cosine.schema`, `inetorgperson.schema`, `misc.schema`, `nis.schema`, `openldap.schema`. Load with `include` in slapd.conf; never modify them. In cn=config, user schema are children of `cn=schema,cn=config` (objectClass `olcSchemaConfig`) using `olcAttributeTypes` and `olcObjectClasses`.

Five steps: get an OID (a Private Enterprise Number from IANA gives `1.3.6.1.4.1.X`; keep a registry), pick a name prefix (`x-` for private use, descriptive like `x-com-Example`), create `local.schema` included after the others, define attribute types, then object classes.

```
objectIdentifier myOID 1.3.6.1.4.1.99999
attributetype ( myOID:3.1 NAME 'x-my-Photo'
    SYNTAX 1.3.6.1.4.1.1466.115.121.1.40 SINGLE-VALUE )
objectclass ( myOID:4.1 NAME 'x-my-PhotoObject' SUP top AUXILIARY
    MAY x-my-Photo )
objectclass ( myOID:4.2 NAME 'x-my-Person' SUP inetOrgPerson STRUCTURAL
    MUST ( x-my-UniqueName $ givenName ) MAY x-my-Photo )
```
`objectIdentifier <name> { <oid> | <name>[:<suffix>] }` defines reusable macros.

Gotchas:
- Do not use OIDs you were not assigned.
- Syntax length `{n}` is only a recommendation; slapd ignores it.
- slapd returns the first listed NAME, so list the preferred name first.
- Operational attributes cannot be extended without source changes.
- An octetString photo has no defined format; clients must agree.

## Checked

2026-11-04. Confirmed against the OpenLDAP 2.6 Administrator's Guide Schema Specification chapter and slapd-config(5): distributed schema files and the required core.schema, include usage, not modifying provided files, the five steps, IANA Private Enterprise Number giving 1.3.6.1.4.1.X, x- name prefix and the x-com-Example style, local.schema included after the others, ABNF-based attributetype and objectclass forms, octetString syntax OID 1.3.6.1.4.1.1466.115.121.1.40, first listed NAME returned, ignored {n} length, objectIdentifier macros, no extension of operational (system) schema without source changes, cn=schema,cn=config with olcSchemaConfig. The numeric OID in the example is a placeholder.

Method: documentation only; no commands were run.
