---
id: computing-software.systems-network-administration.samba.samba-tool-computers-ous
name: samba-tool-computers-ous
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, samba-tool-computers-ous, computer-add, organizational-unit, samba-tool, contact]
level: practitioner
status: docs-checked
description: "Use samba-tool computer, ou and contact subcommands to add, list, show, move, rename and delete AD computers, organizational units and contacts."
sources:
  - https://www.samba.org/samba/docs/current/man-html/samba-tool.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# samba tool computers and ous
Computers:
```
samba-tool computer add COMPUTERNAME [--computerou=OU] [--description=TEXT] [--ip-address=IP] [--service-principal-name=SPN] [--prepare-oldjoin]
samba-tool computer delete COMPUTERNAME
samba-tool computer list
samba-tool computer move COMPUTERNAME NEW_PARENT_DN
samba-tool computer show COMPUTERNAME [--attributes=ATTRS]
samba-tool computer edit COMPUTERNAME [--editor=EDITOR]
```
`--ip-address` and `--service-principal-name` can be repeated (IPv4 makes an A record, IPv6 an AAAA). `computer create` is a deprecated synonym.

Organizational units:
```
samba-tool ou add OU_DN [--description]
samba-tool ou delete OU_DN [--force-subtree-delete]
samba-tool ou list [--full-dn]
samba-tool ou listobjects OU_DN [--full-dn]
samba-tool ou move OLD_OU_DN NEW_PARENT_DN
samba-tool ou rename OLD_OU_DN NEW_OU_DN
```
Contacts: `samba-tool contact add|list|show|delete|edit|move|rename`, with name options such as `--surname`, `--given-name`, `--mail-address`, `--ou`.

Example: `samba-tool ou add "OU=Servers,DC=samdom,DC=example,DC=com"` (illustrative DN).

`ou delete --force-subtree-delete` deletes the OU and all its children recursively; use it with care.

## Checked

2026-11-04. Confirmed against the samba-tool(8) manual page: computer add/delete/list/move/show/edit and their options, create as deprecated synonym, A/AAAA behaviour of --ip-address, all ou subcommands and options, contact subcommands and name options. Removed `-r|--recursive` from ou listobjects (not on the page) and the claim that ou delete fails on non-empty OUs (the page only documents --force-subtree-delete). The example DN is illustrative.
Method: documentation only; no commands were run.
