---
id: computing-software.systems-network-administration.samba.samba-tool-users
name: samba-tool-users
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, samba-tool-users, user-add, user-management, samba-tool, active-directory]
level: practitioner
status: docs-checked
description: "Create, list, show, enable, disable, unlock, move and delete AD users with samba-tool user, including hide filters and attribute queries."
sources:
  - https://www.samba.org/samba/docs/current/man-html/samba-tool.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# samba tool users
```
samba-tool user add USERNAME [PASSWORD]
samba-tool user delete USERNAME
samba-tool user enable USERNAME
samba-tool user disable USERNAME [--remove-supplemental-groups]
samba-tool user unlock USERNAME
samba-tool user setpassword USERNAME
samba-tool user setexpiry USERNAME
samba-tool user list [--full-dn] [-b BASE_DN] [--hide-expired] [--hide-disabled] [--locked-only]
samba-tool user show USERNAME [--attributes=ATTRS]
samba-tool user move USERNAME NEW_PARENT_DN
samba-tool user addunixattrs USERNAME UID
```
- `user create` is a deprecated synonym of `user add`.
- `--remove-supplemental-groups` on disable removes all groups except the primary group.
- `--attributes` takes a comma-separated list.
- Example: `samba-tool user list --hide-disabled`.

Global options accepted by most subcommands: `-H|--URL`, `-U|--user`, `-s|--configfile`, `-d|--debuglevel`, `-N|--no-pass`, `--use-kerberos`.

Passwords must satisfy the domain policy (see password-policy). For Unix IDs see rfc2307-attributes.

The page does not list the option names for `setpassword` or `setexpiry`; use `--help`.

## Checked

2026-11-04. Confirmed against the samba-tool(8) manual page: all user subcommands listed, list filters (--hide-expired, --hide-disabled, --locked-only, --full-dn, -b), show --attributes, disable --remove-supplemental-groups, create as synonym, and the global options -H, -s, -d, -N, --use-kerberos. Removed the unconfirmed prompt-for-password bullet.
Method: documentation only; no commands were run.
