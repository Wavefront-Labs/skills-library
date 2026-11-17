---
id: computing-software.systems-network-administration.samba.idmap-ad
name: idmap-ad
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, idmap-ad, schema-mode, ad-backend, rfc2307, idmap, winbind]
level: advanced
status: docs-checked
description: "Configure the Samba idmap_ad backend: schema_mode, unix_primary_group, unix_nss_info, all_groupmem, allow/deny OUs, and prerequisites in AD."
sources:
  - https://www.samba.org/samba/docs/current/man-html/idmap_ad.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# idmap ad
Read-only backend: you must add `uidNumber` to users and `gidNumber` to groups in AD beforehand. Only users with a `uidNumber` whose primary group has a `gidNumber` are mapped.

| Option | Default | Meaning |
|---|---|---|
| `range` | not stated | IDs stored in AD outside it are ignored |
| `schema_mode` | `rfc2307` | also `sfu`, `sfu20` |
| `unix_primary_group` | `no` | yes: primary group from `gidNumber` |
| `unix_nss_info` | `no` | yes: shell and home from LDAP |
| `all_groupmem` | `no` | return all members, even without `uidNumber` |
| `deny ous` / `allow ous` | none | OU filters; deny evaluated first |

Example:
```
[global]
workgroup = CORP
idmap config * : backend = tdb
idmap config * : range = 1000000-1999999
idmap config CORP : backend = ad
idmap config CORP : range = 1000-999999
```
`ad` is never the default backend; the writable `*` range must not overlap `CORP`. With trusts, resolve ID conflicts beforehand (resolution order is not guaranteed).

Set `unix_nss_info = yes` to take shell and home from AD; otherwise `template shell`/`template homedir` apply.

## Checked
2026-11-04: the option table, defaults, OU filter order and the example compared with the idmap_ad man page. Removed: a Domain Admins gidNumber gotcha the page does not state.
Method: documentation only; no commands were run.
