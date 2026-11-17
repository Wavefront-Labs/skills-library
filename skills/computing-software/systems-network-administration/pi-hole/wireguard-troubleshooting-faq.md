---
id: computing-software.systems-network-administration.pi-hole.wireguard-troubleshooting-faq
name: wireguard-troubleshooting-faq
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [wireguard-dynamic-ip, wireguard-mtu, wireguard-dns-reset]
level: practitioner
status: docs-checked
description: "Fix common WireGuard problems with Pi-hole: dynamic server IP, resetting routes, broken DNS, low MTU and Pi-hole not listening on wg0."
sources: ["https://docs.pi-hole.net/guides/vpn/wireguard/faq/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# WireGuard troubleshooting

**Dynamic server IP.** Hostnames cannot be resolved during startup, which may cause a five-minute boot delay. Disable `auto wg0` in `/etc/network/interfaces` and start it later with `sudo ifup wg0`. If the IP changes while connected, reconnect with `sudo ifdown wg0 && sudo ifup wg0`; the guide shows a cron script that restarts the link when the resolved IP changes.

**Routes periodically reset.** NetworkManager users should mark WireGuard interfaces unmanaged in `/etc/NetworkManager/conf.d/unmanaged.conf`:

```text
[keyfile]
unmanaged-devices=interface-name:wg*
```

**Broken DNS after tunnelling everything.** `wg-quick` registers `DNS` entries through `resolvconf`. Network managers or DHCP clients that do not use `resolvconf` overwrite `/etc/resolv.conf`. Use software that supports `resolvconf`; on Ubuntu with `systemd-resolved`, make sure `systemd-resolvconf` is installed.

**Low MTU.** With an MTU below 1280, `wg-quick` may fail to create the interface. Set on the client:

```text
[Interface]
MTU = 1500
```

**Pi-hole not listening on wg0 after reboot.** If `wg0` is not up when `pihole-FTL` starts, delay FTL start with the `misc.delay_startup` setting (0 to 300 seconds, default 0). For example `sudo pihole-FTL --config misc.delay_startup 5`. The delay applies only within the first 180 seconds after boot.

**Checklist**

1. Match the symptom to the section above and apply that fix.

## Checked

2026-11-03. Read the Pi-hole WireGuard FAQ (dynamic IP and the five-minute boot delay, `ifup`/`ifdown` commands, NetworkManager unmanaged-devices file, resolvconf and systemd-resolvconf, MTU below 1280 and `MTU = 1500`, delayed FTL start) and the `misc.delay_startup` entry of the FTL configuration reference (0 to 300, default 0, only within 180 seconds of boot). The FAQ writes the key as `mic.delay_startup`, a typo: the reference confirms `misc.delay_startup`. Removed the generic checklist steps.

Method: documentation only; no commands were run.
