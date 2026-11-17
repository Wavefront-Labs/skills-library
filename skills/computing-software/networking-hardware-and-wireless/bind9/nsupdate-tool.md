---
id: computing-software.networking-hardware-and-wireless.bind9.nsupdate-tool
name: nsupdate-tool
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, nsupdate, ddns, prereq]
level: practitioner
status: docs-checked
description: "Send dynamic updates with nsupdate: key options -k, -y, -l, -g, and the server, zone, prereq, update, send and show commands."
sources:
  - https://bind9.readthedocs.io/en/latest/manpages.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nsupdate tool
`nsupdate` reads commands and sends one update request:

```
server ns1.example.com
zone example.com
update add www.example.com 300 A 192.0.2.10
send
```

Commands: `server`, `zone`, `key`, `prereq nxdomain|yxdomain|nxrrset|yxrrset`, `update add|delete`, `send`, `show`.

Authentication: `-k` key file, `-y` inline key (discouraged: the secret appears on the command line), `-l` local-host mode using the session key that named generates when a local primary zone sets `update-policy local`, `-g` for GSS-TSIG. DoT uses `-S`. `-y` and `-k` are mutually exclusive.

Prerequisite lines set conditions that must hold for the whole update request to succeed. A blank line or `send` sends the accumulated commands as one request. Do not hand-edit zones under dynamic control. The server must permit the update through `allow-update` or `update-policy`.

## Checked

2026-11-04. Confirmed against the nsupdate man page (options, input format, prerequisites) and the ARM session-keyname entry. Reworded the prerequisite and local-mode sentences and added the `-y` caveat.

Method: documentation only; no commands were run.
