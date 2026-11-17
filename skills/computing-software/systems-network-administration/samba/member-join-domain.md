---
id: computing-software.systems-network-administration.samba.member-join-domain
name: member-join-domain
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, member-join-domain, net-ads-join, domain-member, security-ads, idmap]
level: practitioner
status: docs-checked
description: "Join a Samba host to an AD or NT4 domain as a member: smb.conf identity and idmap lines, net ads join, samba-tool domain join MEMBER, and the admin-to-root map."
sources:
  - https://wiki.samba.org/index.php/Setting_up_Samba_as_a_Domain_Member
  - https://www.samba.org/samba/docs/current/man-html/idmap_autorid.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# member join domain
smb.conf `[global]` identity (pattern from the idmap man pages, with the ranges the wiki suggests; names are examples; the realm is the DNS domain in uppercase):
```
security = ads
workgroup = SAMDOM
realm = SAMDOM.EXAMPLE.COM
idmap config * : backend = tdb
idmap config * : range = 3000-7999
idmap config SAMDOM : backend = rid
idmap config SAMDOM : range = 10000-999999
```
Choose the backend per idmap-backend-choice. The wiki says the default `*` range and the domain ranges must not overlap, and to add an idmap configuration for every trusted domain unless you use autorid.

Join:
- AD: `net ads join -U administrator`
- AD (Samba 4.15+): `samba-tool domain join samdom.example.com MEMBER -U administrator`
- NT4: `net rpc join -U administrator`

With `net ads join` the forward DNS record should be created; if the host has a fixed IP you must create the reverse PTR record yourself.

Verify: `wbinfo --ping-dc`.

Optional admin mapping (members only, never on a DC), in `[global]`:
`username map = /usr/local/samba/etc/user.map` with file content `!root = SAMDOM\Administrator`. Usually unnecessary; a `Domain Admins` member works instead. Do not log on to a member as Administrator after mapping it to root.

The join registers the host name in AD DNS, so `net` must be able to resolve the host name through DNS or a correct `/etc/hosts` entry.

## Checked
2026-11-04: smb.conf identity and ranges, join commands, the 4.15 samba-tool note, the username map steps and the DNS requirement compared with the Domain Member wiki page and the idmap man pages. Removed: a testparm step, a net ads testjoin check, and a failure-fixes line (clock skew, NT_STATUS_INVALID_PARAMETER, -S retry) that the cited pages do not state.
Method: documentation only; no commands were run.
