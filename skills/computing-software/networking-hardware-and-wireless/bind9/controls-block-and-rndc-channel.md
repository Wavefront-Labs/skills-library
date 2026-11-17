---
id: computing-software.networking-hardware-and-wireless.bind9.controls-block-and-rndc-channel
name: controls-block-and-rndc-channel
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, controls, rndc, control-channel]
level: practitioner
status: docs-checked
description: "Configure the BIND 9 controls block so rndc can reach named: inet address, port 953, allow list and keys."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html
  - https://bind9.readthedocs.io/en/latest/chapter4.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# controls block and rndc channel
The `controls` block defines the control channel `rndc` uses. Elements: `inet`, with default port 953; `allow` (an address match list); `keys` (key names permitted); and `read-only`. The unix socket option was removed.

```
controls {
    inet 127.0.0.1 allow { localhost; } keys { rndc_key; };
};
```

With no `controls` statement, named listens on 127.0.0.1 and ::1 and loads the key from `/etc/rndc.key`; an empty `controls { };` disables the channel.

## Checked

2026-11-04. Read the controls Block Definition in the Administrator Reference Manual: inet default port 953, allow, keys, read-only and the removed unix option confirmed. Replaced an unconfirmed key-matching sentence and a generic closing tip with the documented default-channel behaviour.

Method: documentation only; no commands were run.
