---
id: computing-software.cybersecurity-defensive.suricata.xbits-and-hostbits
name: xbits-and-hostbits
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [xbits, hostbits, ip-pair, bit-expiry]
level: advanced
status: docs-checked
description: "Track state per host, IP pair or transaction with xbits: actions, track options, expiry and suricatasc hostbit commands."
sources: ["https://docs.suricata.io/en/latest/rules/xbits.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# xbits and hostbits

`xbits:<set|unset|isset|isnotset|toggle>,<name>,track <ip_src|ip_dst|ip_pair>;` and, for transactions, `xbits:<set|isset>,<name>,track tx;`. An optional expire in seconds limits persistence.

- With `ip_src` or `ip_dst`, xbits and hostbits are the same.
- Request/response: a request sets a bit with `track ip_dst`, the response checks it with `track ip_src`.
- Host bits live in the Host table, pair bits in the IPPair table (watch memcap).
- Thread timing can make set and check order slightly unpredictable.

Manage with suricatasc: `add-hostbit <ip> <bit name> <expire in seconds>`, `remove-hostbit <ip> <bit name>`, `list-hostbit <ip>`.

Docs example: drop rules set a `badssh` bit on the source for 3600 seconds, and a third rule drops while `xbits:isset,badssh,track ip_src` holds.

## Checked

2026-11-08. Read in full the raw Suricata user guide source behind the cited URL (doc/userguide/rules/xbits.rst): syntax, tx tracking, notes, host and IPPair table settings, threading note, the unix socket hostbit commands, and the SSH blacklist example. Nothing removed.

Method: documentation only; no commands were run.
