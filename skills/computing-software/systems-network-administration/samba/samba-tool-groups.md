---
id: computing-software.systems-network-administration.samba.samba-tool-groups
name: samba-tool-groups
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, samba-tool-groups, group-add, group-management, samba-tool, active-directory]
level: practitioner
status: docs-checked
description: "Manage AD groups with samba-tool group: add, delete, list, add and remove members, list members with filters, rename and add Unix gidNumber."
sources:
  - https://www.samba.org/samba/docs/current/man-html/samba-tool.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# samba tool groups
```
samba-tool group add GROUPNAME
samba-tool group delete GROUPNAME
samba-tool group list
samba-tool group addmembers GROUPNAME MEMBERS
samba-tool group removemembers GROUPNAME MEMBERS
samba-tool group listmembers GROUPNAME [--full-dn] [--hide-expired] [--hide-disabled]
samba-tool group addunixattrs GROUPNAME GIDNUMBER [-H URL]
samba-tool group rename GROUPNAME [--force-new-cn] [--reset-cn] [--mail-address] [--samaccountname]
```
- `addunixattrs` adds RFC2307 Unix attributes (a `gidNumber`) to the group; the man page says to add `idmap_ldb:use rfc2307 = Yes` to smb.conf to use them for UID/GID mapping, and that the ID is set provided it is not already in use.
- `group create` is a deprecated synonym of `group add`; other subcommands: `edit --editor=EDITOR`, `move`, `show`, `stats`.

Examples:
- `samba-tool group listmembers "Domain Users" --hide-disabled`
- `samba-tool group addunixattrs "Unix Admins" 10000` (illustrative GID)

Check mapping on a member with `wbinfo -g` or `getent group "SAMDOM\Unix Admins"`.

## Checked

2026-11-04. Confirmed against the samba-tool(8) manual page: all group subcommands and options shown, listmembers filters, rename options, addunixattrs behaviour and its Group1 example, create as synonym. The wbinfo -g option is on the wbinfo(1) page and getent with DOMAIN\name is used on the Samba wiki member page. Removed the member-list format claim and the unconfirmed Domain Admins gidNumber warning.
Method: documentation only; no commands were run.
