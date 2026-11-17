---
id: computing-software.systems-network-administration.openldap.mdb-indexing
name: mdb-indexing
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, olcdbindex, index-types, idlexp, mdb, indexing]
level: practitioner
status: docs-checked
description: "Choose and change OpenLDAP MDB indexes: pres, eq, approx, sub, nolang and nosubtypes, objectClass eq, index_param failed log hints, idlexp and slapindex."
sources:
  - https://www.openldap.org/software/man.cgi?query=slapd-mdb&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
  - https://www.openldap.org/doc/admin26/slapdconfig.html
  - https://www.openldap.org/doc/admin26/tuning.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MDB indexing
Syntax: `index {<attrlist>|default} [pres,eq,approx,sub,special]` (slapd.conf), or `olcDbIndex:` in cn=config.

Examples:
```
index objectClass eq
index cn,sn pres,eq,sub
index default pres,eq
```
Facts:
- `sub` splits into `subinitial`, `subany`, `subfinal`. Specials: `nolang`, `nosubtypes`. There is no inequality keyword; inequality matches generally use no index, though some attributes support it via the equality index.
- By default an index on an attribute also covers every subtype (an `eq` index on `name` indexes `cn`, `sn` and others); `nosubtypes` turns that off.
- Always give `objectClass` an `eq` index, then index attributes used in filters (`cn`, `sn`, `givenname`, `mail`).
- Presence indexes are rarely worth it (only for attributes that are rare yet searched often); substring indexes are large. Unused indexes still have to be maintained and slow things down.
- Some indexes are mandatory for replication or ACL filters; check the replication chapter of the Admin Guide for the attributes.
- Each index slot holds up to 2^16 (65536) entries by default (`idlexp`, range 16 to 30); beyond that the slot collapses to a range and filters get slow. If `idlexp` is decreased, indexes must be rebuilt at once with slapd offline (`slapindex -q -t`); if increased, indexes must be rebuilt to benefit.
- Changing indexes in `slapd.conf` requires rebuilding them with `slapindex`; changing them through cn=config rebuilds online in a background task.

Watch the log for `index_param failed (18)`: a client used an equality filter on an attribute with no equality index. Many of these: add the index; one a month: may be ignorable.

## Checked
2026-11-08: confirmed against the slapd-mdb(5) man page, the Admin Guide slapd.conf chapter (index, idlexp) and the Tuning chapter (index_param failed (18), presence and substring guidance). Removed the unconfirmed claim that approximate indexes are large and the specific entryUUID/entryCSN names (not on the cited pages).
Method: documentation only; no commands were run.
