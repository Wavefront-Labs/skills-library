---
id: computing-software.systems-network-administration.samba.wbinfo
name: wbinfo
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, wbinfo, ping-dc, sid-lookup, winbind-queries, winbind]
level: practitioner
status: docs-checked
description: "Query winbindd with wbinfo: list users and groups, convert names, SIDs and IDs, check the trust secret, ping the DC, authenticate, and read online status."
sources:
  - https://www.samba.org/samba/docs/current/man-html/wbinfo.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# wbinfo
Exit status 0 on success, 1 on failure; if winbindd is not running it always fails.

| Task | Command |
|---|---|
| list users / groups | `wbinfo -u`, `wbinfo -g` (add `--domain='*'` for trusted domains) |
| name to SID / SID to name | `wbinfo -n name`, `wbinfo -s sid` |
| SID to UID / GID | `wbinfo -S sid`, `wbinfo -Y sid` |
| UID / GID to SID | `wbinfo -U uid`, `wbinfo -G gid` |
| check trust secret | `wbinfo -t [domain]` |
| change trust password | `wbinfo -c [domain]` |
| trusted domains | `wbinfo -m` |
| light DC check | `wbinfo -P` (`--ping-dc`) |
| is winbindd running | `wbinfo -p` |
| authenticate | `wbinfo -a user%password`, Kerberos: `wbinfo -K user%password` |
| user info | `wbinfo -i user` |
| group IDs of a user | `wbinfo -r username` |
| group SIDs of a user | `wbinfo --user-sids sid` |
| SID to DOMAIN\user | `wbinfo --sid-to-fullname sid` |
| connection state | `wbinfo --online-status [domain]` |
| current DC | `wbinfo --dc-info domain` |

`-n` defaults to the `workgroup` domain; prefix others with the separator (for example `CWDOM1/Administrator`). `-S` and `-Y` fail when the SID is not mapped by winbindd; `-U` and `-G` fail when the ID is outside the idmap range. `-r` is only reliable after the user has authenticated (otherwise it uses the machine account and can be incomplete). `-u`/`-g` do not allocate IDs for unseen objects. For third-party apps prefer `ntlm_auth` over `-a`.

## Checked

2026-11-04. Confirmed against the wbinfo(1) manual page: every option in the table, the exit status rule, the `*` domain form, -u/-g not allocating IDs, the -n default domain and CWDOM1 example, -P being lighter than -t, and the ntlm_auth advice. Corrected the mapping-failure sentence to match the page and added the -r caveat.
Method: documentation only; no commands were run.
