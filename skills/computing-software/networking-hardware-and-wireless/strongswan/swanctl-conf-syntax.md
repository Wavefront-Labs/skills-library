---
id: computing-software.networking-hardware-and-wireless.strongswan.swanctl-conf-syntax
name: swanctl-conf-syntax
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, swanctl-conf, syntax, dot-notation, time-formats]
level: intro
status: docs-checked
description: "How swanctl.conf is organised: connections, secrets, pools and authorities sections, dot-notation placeholders, suffixes, and number and time formats."
sources:
  - https://docs.strongswan.org/docs/latest/swanctl/swanctlConf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# swanctl conf syntax
`swanctl.conf` lives in the swanctl configuration directory (usually `/etc/swanctl`) and feeds the `swanctl --load-*` commands. It provides connections, secrets and IP address pools (plus an authorities section for CA attributes). It uses strongswan.conf-style syntax; referencing sections and including other files are supported.

Options are documented in dot-notation with placeholders:

```
connections.<conn>.remote<suffix>.auth=...
connections.<conn>.children.<child>.local_ts=...
```

`<conn>` and `<child>` are arbitrary names. `<suffix>` is an optional extension to a section name; it can usually be omitted, except for e.g. secondary authentication rounds or several secrets of the same type. In a file:

```
connections {
    connection_a {
        remote { auth=... }
        children { child_1 { local_ts=... } }
    }
}
```

Integers are decimal or hexadecimal (`0x` prefix). Times are in seconds unless stated; the suffixes `s`, `m`, `h` and `d` convert, so a 4 hour rekey time can be written `4h`. Some global options take plain seconds or milliseconds, or floating-point values, and do not accept suffixes.

## Checked
2026-11-04. Confirmed against the strongSwan swanctl.conf reference overview: dot-notation placeholders, suffix rules, number formats, time suffixes s, m, h and d. Nothing removed.

Method: documentation only; no commands were run.
