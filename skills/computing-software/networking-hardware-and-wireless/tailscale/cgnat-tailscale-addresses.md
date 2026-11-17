---
id: computing-software.networking-hardware-and-wireless.tailscale.cgnat-tailscale-addresses
name: cgnat-tailscale-addresses
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [cgnat, tailscale-ip, 100-64-0-0]
level: intro
status: docs-checked
description: "Why Tailscale uses the CGNAT range and what it means for conflicts."
sources: ["https://tailscale.com/kb/1015"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tailscale IP addresses

Goal: explain the 100.x.y.z addresses on a tailnet.

- Every device gets a unique Tailscale IP that stays the same wherever the device is. Moving from Wi-Fi to cellular does not change it.
- The addresses come from the CGNAT range `100.64.0.0/10` (100.64.0.0 through 100.127.255.255), special-use IPv4 space similar to private ranges.

**Why this range**

- It does not conflict with subnets commonly used for private networks such as `10.0.0.0/8` and `192.168.0.0/16`. Conflicts can still happen when Tailscale runs alongside other VPNs that use the same range.
- It is meant for intermediate traffic needing additional NAT before the public internet, which is exactly how Tailscale uses it.
- It is meant for internet service providers, not private networks, matching Tailscale acting as a provider building a shared network on the regular internet.

**Practical notes**

- Use the address in access rules (a Tailscale IP in `src` or `dst` selects only the device that owns it).
- Use `tailscale whois ip[:port]` to find the machine and user behind an address.
- Names via MagicDNS are easier than addresses.

**Checklist**

1. Check for other VPNs using 100.64.0.0/10.
2. Prefer MagicDNS names.
3. Use `tailscale whois` to identify an IP.

## Checked

2026-11-03. Read Tailscale IP addresses (kb/1015) and confirmed the `100.64.0.0/10` range, reasons for the choice and the `tailscale whois` use; reworded the whois syntax. Nothing else was removed.

Method: documentation only; no commands were run.
