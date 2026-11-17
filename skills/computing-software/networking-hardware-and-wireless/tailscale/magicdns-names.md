---
id: computing-software.networking-hardware-and-wireless.tailscale.magicdns-names
name: magicdns-names
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [magicdns, fqdn, ts-net]
level: practitioner
status: docs-checked
description: "Know how MagicDNS builds names, search domains and the full-domain rule for shared devices."
sources: ["https://tailscale.com/kb/1081"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# MagicDNS names

Goal: reach tailnet devices by name and know when the full name is required.

**Enabling.** MagicDNS registers DNS names for devices automatically. Tailnets created on or after October 20, 2022 have it enabled by default; otherwise turn it on in the DNS page of the admin console. With Tailscale v1.20 or later it does not require a DNS nameserver; older clients need at least one nameserver set.

**Name anatomy.** The fully qualified domain name is the machine name (editable) plus the tailnet DNS name, for example machine `monitoring` and tailnet `yak-bebop.ts.net` give `monitoring.yak-bebop.ts.net`. Renaming a device changes its entry. MagicDNS adds search domains, so these are equivalent:
```
ping monitoring
ping monitoring.yak-bebop.ts.net
```

**Rules and gotchas**

- Devices shared with you work only on Tailscale v1.4 or later and only by full domain name, for security.
- On macOS, `host` and `nslookup` bypass system resolution and will not resolve MagicDNS names even when `ping` does.
- Support for the legacy `*.beta.tailscale.net` name ended September 13, 2024; migrate to the `.ts.net` name and delete the old nameserver (Owner, Admin or IT admin).
- Find a device's full name on its page under Machines.
- Disabling MagicDNS network-wide uses the same DNS page toggle.

**Checklist**

1. Enabled.
2. Use the machine name locally, the full name for shared devices.
3. Legacy beta nameserver removed.

## Checked

2026-11-03. Read MagicDNS (kb/1081) and confirmed the 20 October 2022 default, v1.20 nameserver rule, shared-device full-name rule, macOS `host`/`nslookup` note and the 13 September 2024 beta nameserver end date. Nothing else was removed.

Method: documentation only; no commands were run.
