---
id: computing-software.networking-hardware-and-wireless.bind9.dynamic-update-and-journal
name: dynamic-update-and-journal
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, dynamic-update, journal, allow-update]
level: advanced
status: docs-checked
description: "BIND 9 dynamic DNS: allow-update or update-policy, the .jnl journal, freeze and thaw, and rndc sync."
sources:
  - https://bind9.readthedocs.io/en/latest/chapter6.html
  - https://bind9.readthedocs.io/en/latest/reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dynamic update and journal
Dynamic update is enabled per zone with `allow-update` or `update-policy`. Accepted updates are appended to a journal (`.jnl`) and merged into the zone file after up to 15 minutes. Transient files may appear as `.jnw` and `.jbk`.

Do not edit a dynamic zone file by hand while named runs:

```
rndc freeze example.com
# edit the file, raise the serial
rndc thaw example.com
```

`rndc sync [-clean]` writes the journal into the zone file at once (`-clean` also removes the journal). `update-policy local;` uses an automatically generated key named `local-ddns` for local `nsupdate -l`.

Limit journal growth with `max-journal-size`.

## Checked

2026-11-04. Read the Dynamic Update and Journal File chapter (15-minute delayed dump, .jnw and .jbk files, freeze/thaw), the rndc man page (sync -clean), and the update-policy local and max-journal-size entries. Nothing was removed.

Method: documentation only; no commands were run.
