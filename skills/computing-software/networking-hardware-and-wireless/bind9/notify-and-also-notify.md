---
id: computing-software.networking-hardware-and-wireless.bind9.notify-and-also-notify
name: notify-and-also-notify
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, notify, also-notify, allow-notify]
level: practitioner
status: docs-checked
description: "BIND 9 NOTIFY: the notify option values, also-notify targets, and notify-source."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html
  - https://bind9.readthedocs.io/en/latest/chapter6.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# notify and also notify
When a zone changes, a primary sends NOTIFY(SOA) messages. `notify yes` (default) sends them to the servers in the zone's NS records, except the primary named in the SOA MNAME, plus any in `also-notify`. `primary-only` (older keyword `master-only`) limits sending to primary zones; `explicit` sends only to `also-notify` targets.

```
zone "example.com" {
    type primary;
    file "example.com.db";
    notify explicit;
    also-notify { /* secondary addresses */ };
};
```

`notify-source` sets the local source address, which must appear in the secondary's `primaries` or `allow-notify`. Use `allow-notify` on a secondary to accept NOTIFY from additional hosts.

## Checked

2026-11-04. Read the notify, also-notify, allow-notify and notify-source entries in the Administrator Reference Manual: notify values, MNAME exception, primary-only/master-only, explicit and notify-source requirement confirmed. Nothing was removed.

Method: documentation only; no commands were run.
