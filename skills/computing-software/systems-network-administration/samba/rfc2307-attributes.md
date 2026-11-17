---
id: computing-software.systems-network-administration.samba.rfc2307-attributes
name: rfc2307-attributes
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, rfc2307-attributes, rfc2307, addunixattrs, uidnumber, gidnumber, idmap]
level: practitioner
status: docs-checked
description: "Store Unix IDs in Samba AD: provision with use-rfc2307, add uidNumber and gidNumber via samba-tool addunixattrs, and how winbind uses them on a DC."
sources:
  - https://wiki.samba.org/index.php/Setting_up_Samba_as_an_Active_Directory_Domain_Controller
  - https://wiki.samba.org/index.php/Configuring_Winbindd_on_a_Samba_AD_DC
  - https://www.samba.org/samba/docs/current/man-html/samba-tool.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rfc2307 attributes
- Provision with `--use-rfc2307` to enable the NIS extensions (ADUC Unix Attributes tab). Joining DCs add `--option='idmap_ldb:use rfc2307 = yes'` when the others were provisioned that way.
- Add IDs from the CLI:
  - `samba-tool user addunixattrs USERNAME UID [--gid-number] [--unix-home] [--login-shell] [--gecos]`
  - `samba-tool group addunixattrs GROUPNAME GIDNUMBER`
  Example from the man page: `samba-tool user addunixattrs User1 10001`.

On an AD DC, winbindd reads `uidNumber` and `gidNumber` from AD. They are not added automatically; objects without them get IDs generated locally in `private/idmap.ldb`.

If you set an AD ID after a local one exists, winbindd uses it only after the cache expires or after `net cache flush`, and you must fix file ownership manually.

On domain members the `ad` idmap backend uses these attributes (see idmap-ad); the wiki says they are not added automatically when users or groups are created, so add them yourself. The ID numbers generated on a DC (the 3000000 range) are not RFC2307 attributes and cannot be used on Unix domain members; choose a different range for your own numbers.

When `--gid-number` is not given, `user addunixattrs` uses the gidNumber of `Domain Users`, so that group must have one.

## Checked

2026-11-04. Confirmed against the samba-tool(8) manual page: user and group addunixattrs syntax, options, defaults and the User1 example; against the Samba wiki pages for the DC, winbindd on a DC and the domain member: --use-rfc2307, the idmap_ldb option, IDs read from AD, local generation in idmap.ldb, net cache flush after cache expiry, no automatic attributes, the 3000000 range note. Removed the unconfirmed claims about unmapped users and a Domain Admins gidNumber.
Method: documentation only; no commands were run.
