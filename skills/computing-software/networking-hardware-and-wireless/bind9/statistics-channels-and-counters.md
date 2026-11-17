---
id: computing-software.networking-hardware-and-wireless.bind9.statistics-channels-and-counters
name: statistics-channels-and-counters
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, statistics-channels, json, xml]
level: practitioner
status: docs-checked
description: "Enable the BIND 9 statistics channel over HTTP, JSON and XML endpoints, and the statistics file written by rndc stats."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html
  - https://bind9.readthedocs.io/en/latest/chapter9.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# statistics channels and counters
Enable the HTTP statistics channel:

```
statistics-channels {
    inet 127.0.0.1 port 8053 allow { 127.0.0.1; };
};
```

The default port is 80. It needs libxml2 or json-c at build time. Endpoints include `/xml`, `/json`, and `/json/v1/server`, `/zones`, `/net`, `/mem`, `/traffic`, `/xfrins`, `/status`.

`rndc stats` writes a text file. It begins with `+++ Statistics Dump +++ (timestamp)`, has sections such as `++ Name Server Statistics ++`, lists non-zero counters only, and ends with `--- Statistics Dump ---`. Counters include `Requestv4`, `ReqEdns0`, `ReqTSIG`, `NotifyOutv4` and `SOAOutv4`. `rndc reset-stats <counter-name ...>` resets the named counters.

## Checked

2026-11-04. Read the statistics-channels entry, the Statistics File section and the rndc man page. Confirmed port 80 default, libxml2/json-c requirement, endpoints, dump markers, zero counters omitted. Fixed rndc reset-stats, which takes counter names rather than clearing everything.

Method: documentation only; no commands were run.
