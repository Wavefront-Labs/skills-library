---
id: computing-software.systems-network-administration.samba.idmap-ldap
name: idmap-ldap
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, idmap-ldap, ldap-base-dn, ldap-backend, idmap, winbind]
level: advanced
status: docs-checked
description: "Store Samba SID to Unix ID mappings in LDAP with idmap_ldap: ldap_url, ldap_base_dn, ldap_user_dn, range, read only, and storing the bind secret."
sources:
  - https://www.samba.org/samba/docs/current/man-html/idmap_ldap.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# idmap ldap
Options:
- `ldap_base_dn`: default is the `ldap idmap suffix` value.
- `ldap_user_dn`: no default; falls back to the ldap passdb credentials, then an anonymous bind.
- `ldap_url`: default `ldap://localhost/`.
- `range = low - high`: the range the backend is authoritative for.
- `read only = yes`: mappings for that domain are read-only (the page's example uses it with a tdb default).

The `ldap_user_dn` password is not kept in smb.conf; store it with `net idmap secret '*' password` (the idmap_ldap page uses this form; the net man page lists `net idmap set secret <DOMAIN> <secret>`, used mainly for domains that use idmap_ldap).

Default backend for all domains:
```
idmap config * : backend      = ldap
idmap config * : range        = 1000000-1999999
idmap config * : ldap_url     = ldap://localhost/
idmap config * : ldap_base_dn = ou=idmap,dc=example,dc=com
idmap config * : ldap_user_dn = cn=idmap_admin,dc=example,dc=com
```
Read-only LDAP for one domain with a tdb default:
```
idmap config * : backend = tdb
idmap config * : range = 1000000-1999999
idmap config DOM1 : backend = ldap
idmap config DOM1 : range = 2000000-2999999
idmap config DOM1 : read only = yes
idmap config DOM1 : ldap_url = ldap://server/
```

## Checked
2026-11-04: options, defaults, secret handling and both examples compared with the idmap_ldap man page and the net man page (IDMAP SET SECRET). Nothing removed.
Method: documentation only; no commands were run.
