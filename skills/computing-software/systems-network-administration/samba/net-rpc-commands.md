---
id: computing-software.systems-network-administration.samba.net-rpc-commands
name: net-rpc-commands
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, net-rpc-commands, net-rpc, rpc-rights, net, privileges]
level: practitioner
status: docs-checked
description: "Use net rpc to join NT4-style domains, manage remote users, groups and shares, and list, grant or revoke privileges such as SeDiskOperatorPrivilege."
sources:
  - https://www.samba.org/samba/docs/current/man-html/net.8.html
  - https://wiki.samba.org/index.php/Setting_up_a_Share_Using_Windows_ACLs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# net rpc commands
```
net rpc join [PDC|BDC|MEMBER] [-U user%pass]
net rpc info
net rpc testjoin
net rpc getsid
net rpc user                       # list
net rpc user add <name> [password] [-F flags] [-C comment]
net rpc user delete|info <target>
net rpc user rename <old> <new>
net rpc group add <name> [-C comment]
net rpc group delete <name>
net rpc share add <name=serverpath> [-C comment] [-M maxusers]
net rpc share delete <sharename>
net rpc vampire [keytab|ldif]      # from a BDC against the PDC; not for AD
```
`net rpc getsid` stores the domain SID in `secrets.tdb`.

Rights (privileges): the net man page says `net rpc rights` has three options, list, grant and revoke. The wiki lists holders with:
`net rpc rights list privileges SeDiskOperatorPrivilege -U "SAMDOM\administrator"`
The wiki recommends granting to a group rather than individuals, and says the grant must be done on the Samba server that holds the share. Only holders of SeDiskOperatorPrivilege can configure the Share Permissions tab.

Target options: `-S server`, `-I ip`, `-w workgroup` (give one of these), `-U [DOMAIN\]user[%pass]`, `-P` (stored machine password), `--use-kerberos=desired|required|off`.

## Checked
2026-11-04: join, user, group, share, vampire, getsid, rights and connection options compared with the net man page; the rights list example and privilege notes compared with the Windows ACL share wiki page. Removed: a loopback gotcha neither page states; a `-k` note.
Method: documentation only; no commands were run.
