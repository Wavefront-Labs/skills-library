---
id: computing-software.systems-network-administration.samba.group-policy-gpo
name: group-policy-gpo
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, group-policy-gpo, admx, gpo, samba-tool, group-policy]
level: advanced
status: docs-checked
description: "Administer Group Policy on a Samba AD DC: load ADMX templates, list, create, link, back up and restore GPOs, and deploy Linux policies with gpo manage."
sources:
  - https://wiki.samba.org/index.php/Group_Policy
  - https://www.samba.org/samba/docs/current/man-html/samba-tool.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# group policy gpo
ADMX templates (Samba's, copied to `<domain>/Policies/PolicyDefinitions` on SYSVOL; Microsoft's are also needed for Windows members):
```
samba-tool gpo admxload -U Administrator
samba-tool gpo admxload -U Administrator --admx-dir=/path/to/PolicyDefinitions/
samba-tool gpo admxload -H ldap://dc1.samdom.example.com -U Administrator
```
Use `-H` with multiple DCs so templates land on the right one.

GPO lifecycle:
```
samba-tool gpo listall -UAdministrator
samba-tool gpo create DISPLAYNAME
samba-tool gpo show GPO
samba-tool gpo setlink CONTAINER_DN GPO
samba-tool gpo dellink CONTAINER_DN GPO
samba-tool gpo setinheritance CONTAINER_DN block|inherit
samba-tool gpo backup GPO --tmpdir=DIR
samba-tool gpo restore DISPLAYNAME BACKUP_LOCATION
samba-tool gpo del GPO
```
`listall` shows the GUIDs other commands need.

Linux policy content (GUID is the target GPO):
```
samba-tool gpo manage scripts startup add {GUID} test_script.sh '-n'
samba-tool gpo manage files add {GUID} ./source.txt /usr/share/doc/target.txt root root 600
samba-tool gpo manage sudoers add {GUID} ALL ALL fakeu fakeg
samba-tool gpo manage openssh set {GUID} KerberosAuthentication Yes
```
Also `manage symlink`, `access`, `motd`, `issue`.

On Windows members use RSAT's Group Policy Management Console. Clients apply policy per samba-gpupdate.

## Checked
2026-11-04: ADMX loading, GPO lifecycle commands and options, manage subcommands and the RSAT note compared with the Group Policy wiki page and the samba-tool man page. Nothing removed.
Method: documentation only; no commands were run.
