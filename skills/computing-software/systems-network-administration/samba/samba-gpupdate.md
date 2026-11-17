---
id: computing-software.systems-network-administration.samba.samba-gpupdate
name: samba-gpupdate
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, samba-gpupdate, apply-group-policies, gpupdate, winbind, group-policy]
level: advanced
status: docs-checked
description: "Apply Group Policy on Linux domain members with winbind and samba-gpupdate: apply group policies setting, force, rsop, unapply, timing and certificate enrolment."
sources:
  - https://wiki.samba.org/index.php/Group_Policy
  - https://www.samba.org/samba/docs/current/man-html/smb.conf.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# samba gpupdate
Enable on a winbind member in `[global]`:
`apply group policies = yes`
(the smb.conf default is `no`). For SSSD instead, install `oddjob-gpupdate`; `samba-gpupdate` must be installed either way.

Commands:
```
samba-gpupdate --force
samba-gpupdate --rsop
samba-gpupdate --unapply --target=Computer
samba-gpupdate --unapply --target=User -U<username>
```
- Only root can remove applied policy.
- Policies are enforced at a random interval between 90 and 120 seconds.
- Script policies create cron jobs; sudo policies write files under `/etc/sudoers.d`.

Certificate auto-enrolment (Samba 4.16+): add `kerberos method = secrets and keytab`, run `net ads keytab create`, install certmonger and cepces, set the CA host (a fully qualified name) in `/etc/cepces/cepces.conf`, then run `samba-gpupdate`. Check with `getcert list`. Certs land in `/var/lib/samba/certs`, keys in `/var/lib/samba/private/certs`.

Windows side: `gpupdate /force`, `/target:computer`, `/boot`. Windows has no feature to remove applied policy.

Policy authoring is in group-policy-gpo.

## Checked
2026-11-04: apply group policies, oddjob-gpupdate, the samba-gpupdate options, timing, cron and sudoers behaviour, certificate enrolment steps and Windows notes compared with the Group Policy wiki page; the apply group policies default compared with the smb.conf man page. Nothing removed.
Method: documentation only; no commands were run.
