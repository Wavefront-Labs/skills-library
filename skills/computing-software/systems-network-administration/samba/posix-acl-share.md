---
id: computing-software.systems-network-administration.samba.posix-acl-share
name: posix-acl-share
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, posix-acl-share, posix-acls, setfacl, file-sharing, domain-member]
level: practitioner
status: docs-checked
description: "Create a Samba share controlled by POSIX ACLs on a Unix domain member: share definition, chmod, setfacl with defaults, inherit acls, and valid users."
sources:
  - https://wiki.samba.org/index.php/Setting_up_a_Share_Using_POSIX_ACLs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# posix acl share
Not supported on a Samba AD DC; use Windows ACLs there.
```
[Demo]
       path = /srv/samba/Demo/
       read only = no
       map acl inherit = yes
       inherit acls = yes
```
Optional: `acl allow execute always = yes`, `valid users = +SAMDOM\"Domain Users"`, `hosts allow = 127.0.0.1 10.99.0.0/24`.

Commands:
```
mkdir -p /srv/samba/Demo/
smbcontrol all reload-config
chmod 2770 /srv/samba/Demo/
chown root:"Domain Users" /srv/samba/Demo/
setfacl -m group::--- /srv/samba/Demo/
setfacl -m default:group::--- /srv/samba/Demo/
setfacl -m group:"SAMDOM\Domain Admins":rwx /srv/samba/Demo/
setfacl -m group:"SAMDOM\Domain Users":r-x /srv/samba/Demo/
setfacl -R -m other::--- /srv/samba/Demo/
setfacl -m default:group:"SAMDOM\Domain Admins":rwx /srv/samba/Demo/
setfacl -m default:group:"SAMDOM\Domain Users":r-x /srv/samba/Demo/
setfacl -m default:other::--- /srv/samba/Demo/
```
SGID (2770) makes new files inherit the directory's group; the `default:` ACLs drive inheritance.

Limits: POSIX draft ACLs offer only None, Read, Write, Full; the `other` entry maps to Windows Everyone; CREATOR OWNER/GROUP principals need Windows ACLs. `invalid users` beats `valid users`; `hosts deny` beats `hosts allow` per this wiki (smb.conf says allow wins on conflict, so avoid conflicts).

## Checked
2026-11-04: share definition, chmod/setfacl commands, optional parameters and limits compared with the Setting up a Share Using POSIX ACLs wiki page; the hosts allow/deny conflict rule compared with the smb.conf man page. Nothing removed.
Method: documentation only; no commands were run.
