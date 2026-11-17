---
id: computing-software.systems-network-administration.samba.member-nsswitch-services
name: member-nsswitch-services
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, member-nsswitch-services, nsswitch, winbindd-service, domain-member, winbind]
level: practitioner
status: docs-checked
description: "Wire winbind into NSS on a Samba domain member and start the right services: nsswitch.conf lines, initgroups, and which daemons to run."
sources:
  - https://wiki.samba.org/index.php/Setting_up_Samba_as_a_Domain_Member
  - https://www.samba.org/samba/docs/current/man-html/smbcontrol.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# member nsswitch services
`/etc/nsswitch.conf`:
```
passwd: files winbind
group:  files winbind
```
- Keep `files` first.
- Do not add `winbind` to `shadow`.
- If an `initgroups` line already exists, add `[success=continue] winbind` to it; do not create the line if absent.

Services on a domain member:
- start `smbd` and `winbindd`;
- `nmbd` is optional (only for network browsing);
- never start the `samba` service on a member.
Samba ships no init scripts; use the ones from your package.

Reload after config changes: `smbcontrol all reload-config` (the all destination reaches every running daemon including nmbd and winbind; reload-config can go to smbd, nmbd or winbindd).

If you compiled Samba, add symbolic links from the libnss_winbind library to the operating system's library path; packages usually create the link. Do not use the same user names in local `/etc/passwd` as in the domain.

Verify with `wbinfo --ping-dc`, `getent passwd "SAMDOM\demo01"`, `getent group "SAMDOM\Domain Users"` (see member-verify-winbind).

## Checked
2026-11-04: nsswitch lines and rules, service list, init script note, ping and getent checks compared with the Domain Member wiki page; reload-config and the all destination compared with the smbcontrol man page. Removed: the smbd -b LIBDIR and ldconfig steps and the template shell and homedir defaults, which are on a different wiki page.
Method: documentation only; no commands were run.
