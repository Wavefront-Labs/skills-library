---
id: computing-software.systems-network-administration.samba.net-groupmap-sam
name: net-groupmap-sam
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, net-groupmap-sam, groupmap, net-sam, net, local-groups]
level: advanced
status: docs-checked
description: "Map Unix groups to Windows groups with net groupmap and manage the local SAM with net sam: local and builtin groups, members, rights and account policy."
sources:
  - https://www.samba.org/samba/docs/current/man-html/net.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# net groupmap and sam
Group mapping:
```
net groupmap add {rid=INT|sid=STR} unixgroup=STR [type={domain|local}] [ntgroup=STR] [comment=STR]
net groupmap modify {ntgroup=STR|sid=SID} [unixgroup=STR] [comment=STR] [type={domain|local}]
net groupmap delete {ntgroup=STR|sid=SID}
net groupmap list [verbose] [ntgroup=STR] [sid=SID]
```
Local SAM:
```
net sam createbuiltingroup <NAME>
net sam createlocalgroup <NAME>
net sam deletelocalgroup <NAME>
net sam mapunixgroup <NAME>
net sam unmapunixgroup <NAME>
net sam addmem <GROUP> <MEMBER>
net sam delmem <GROUP> <MEMBER>
net sam listmem <GROUP>
net sam list <users|groups|localgroups|builtin|workstations> [verbose]
net sam rights list|grant <NAME> <PRIV>|revoke <NAME> <PRIV>
net sam show <NAME>
net sam set homedir|profilepath|comment|fullname|logonscript|homedrive|workstations <NAME> <VALUE>
net sam set disable|pwnotreq|autolock|pwnoexp <NAME>
net sam set pwdmustchangenow <NAME> [yes|no]
net sam policy list|show <policy>|set <policy> <value>
```
`createbuiltingroup` and `createlocalgroup` need a running winbindd with idmap allocation configured (the gid comes from the winbindd range). `mapunixgroup` makes an existing Unix group a domain group of the same name. `rights grant|revoke` take a name and one or more privileges. Policy values may be `forever`, `never`, `off` or a number.

Group mapping `type` is domain, local or builtin in the common options, though add and modify list only domain and local. `groupmap delete` removes the first match if several match.

Local SID: `net getlocalsid [DOMAIN]`, `net setlocalsid S-1-5-21-x-y-z`.

Example: `net groupmap list verbose`.

## Checked
2026-11-04: groupmap and sam subcommands, syntax and notes compared with the net man page. Removed: a verification line the page does not state.
Method: documentation only; no commands were run.
