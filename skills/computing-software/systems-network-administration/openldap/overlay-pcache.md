---
id: computing-software.systems-network-administration.openldap.overlay-pcache
name: overlay-pcache
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, pcache, proxy-cache, pcachetemplate, pcacheattrset, overlay]
level: advanced
status: docs-checked
description: "Cache search results from a remote LDAP server with the OpenLDAP pcache overlay: pcache, pcacheAttrset, pcacheTemplate, TTLs, bind caching and offline mode."
sources:
  - https://www.openldap.org/software/man.cgi?query=slapo-pcache&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
  - https://www.openldap.org/doc/admin26/overlays.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pcache proxy cache overlay
Placed on a `database ldap` or `database meta` proxy:
```
database ldap
suffix "dc=example,dc=com"
uri ldap://ldap.example.com/
overlay pcache
pcache mdb 100000 1 1000 100
pcacheAttrset 0 mail postaladdress telephonenumber
pcacheTemplate (sn=) 0 3600
pcacheTemplate (&(sn=)(givenName=)) 0 3600
```
Cache backing database (an mdb): `directory /var/tmp/cache`, `maxsize 1073741824`, and `index pcacheQueryid eq`.

Directives:
- `pcache <db> <max_entries> <numattrsets> <entry_limit> <cc_period>`: `entry_limit` must be at most `max_entries`; period in seconds.
- `pcacheAttrset <index> <attrs...>`: indexes 0 to numattrsets-1; supports `*`, `+`, `1.1`, `undef:` (not with mdb).
- `pcacheTemplate <filter template> <attrset> <ttl> [<negttl> [<limitttl> [<ttr>]]]`; extras default 0 (off).
- `pcacheMaxQueries` (10000), `pcacheValidate` (FALSE), `pcacheOffline` (FALSE), `pcachePersist` (FALSE), `pcachePosition head|tail` (tail).
- `pcacheBind <filter_template> <attrset> <ttr> <scope> <base>`: cache simple-bind credentials (hashed).

A query is cacheable only if its filter matches a template and its attributes fit the set.

Gotchas: cached data can lag the remote by the TTL (keep TTR below TTL); paged results are stripped; per-identity ACLs can leak between users (use `idassert-bind`); `pcachePersist` requires unchanged attrset and template config across restarts.

## Checked

2026-11-04. Confirmed against slapo-pcache(5): the pcache directive and its constraints (entry_limit at most max_entries), pcacheAttrset index range and the *, +, 1.1 and undef: forms (undef not with mdb), pcacheTemplate optional negttl, limitttl and ttr defaulting to 0, pcacheMaxQueries 10000, pcacheValidate off, pcacheOffline FALSE, pcachePersist FALSE with its caveat, pcachePosition tail, pcacheBind with hashed credentials, directory and maxsize for the cache database, the pcacheQueryid equality index, TTL-bounded inconsistency and TTR, paged results stripped, per-identity ACL leakage with idassert-bind advice. Removed the unconfirmed OR-versus-AND template remark and the rootdn requirement.

Method: documentation only; no commands were run.
