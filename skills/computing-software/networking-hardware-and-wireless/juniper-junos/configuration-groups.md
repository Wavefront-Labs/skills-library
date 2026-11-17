---
id: computing-software.networking-hardware-and-wireless.juniper-junos.configuration-groups
name: configuration-groups
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, apply-groups, groups, configuration-groups, wildcard]
level: practitioner
status: draft
description: "Reuse Junos configuration with groups and apply-groups, including wildcard groups and apply-groups-except."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Configuration groups and apply-groups
Goal: stamp common config onto many interfaces or neighbors without repetition.

```
set groups UPLINK interfaces <ge-*> mtu 9192
set groups UPLINK interfaces <ge-*> unit 0 family inet6
set interfaces ge-0/0/1 apply-groups UPLINK
set interfaces ge-0/0/2 apply-groups UPLINK
set apply-groups GLOBAL
set groups GLOBAL system ntp server 192.0.2.10
show interfaces ge-0/0/1 | display inheritance
```

- Names in `<>` are wildcards, `*` matches any chars; groups can be applied at any hierarchy level.
- `apply-groups-except NAME` opts a stanza out.
- `display inheritance` shows inherited values with the group source; add `no-comments` for clean output.
- `junos-defaults` is a built-in group you can inspect with `show groups junos-defaults`.

Gotcha: explicit config on the object overrides group values, and group values do NOT appear in a plain `show`. Troubleshooting without `display inheritance` leads to chasing invisible settings.

## Verify
- `show interfaces ge-0/0/1 | display inheritance` prints the MTU with a `## 'UPLINK'` comment.
