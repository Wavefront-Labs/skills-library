---
id: computing-software.systems-network-administration.samba.nmblookup
name: nmblookup
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, nmblookup, netbios, node-status, master-browser, wins]
level: practitioner
status: docs-checked
description: "Query NetBIOS names with nmblookup: broadcast and unicast lookups, node status by IP, master browser and WINS queries, name type suffixes, and resolve order."
sources:
  - https://www.samba.org/samba/docs/current/man-html/nmblookup.1.html
  - https://www.samba.org/samba/docs/current/man-html/smb.conf.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nmblookup
Options:
- `-M|--master-browser`: look up type 0x1d; for `-` use `nmblookup -M -- -` (queries `__MSBROWSE__`).
- `-R|--name-resolve ORDER`: quoted list of `lmhosts host wins bcast`; default order lmhosts, host, wins, bcast.
- `-S|--status`: node status after a successful lookup.
- `-A|--lookup-by-ip`: treat the argument as an IP and run node status.
- `-B|--broadcast ADDR`: query a broadcast address.
- `-U|--unicast ADDR`: unicast query; combine with `-R` for WINS.
- `-T|--translate`: reverse-DNS the results.
- `-f|--flags`: show response flags.
- `-r|--root-port`: bind UDP 137 (old Windows 95 bug; usually root).
- `-d 0-10` (default 1).

Name syntax: `NAME#<hex type>`, for example `'IRIX#1B'` (domain master browser); `'*'` returns all registered names in a broadcast area (quote it).

Examples:
```
nmblookup -A 192.168.1.10
nmblookup -B 192.168.1.255 '*'
nmblookup -U samba.org -R 'IRIX#1B'
```
smb.conf side: `name resolve order` default `lmhosts wins host bcast`; `wins support` default `no` (enable on one server only); `wins server` no default; `netbios name` defaults to the machine DNS name (max 15 chars).

## Checked

2026-11-04. Confirmed against the nmblookup(1) and smb.conf(5) manual pages: all options, the debug level range and default, name type syntax, the WINS example, name resolve order defaults, wins support, wins server, netbios name and the 15 character limit. Removed the unconfirmed claim that AD DCs run no nmbd.
Method: documentation only; no commands were run.
