---
id: computing-software.networking-hardware-and-wireless.tailscale.linux-udp-gro-performance
name: linux-udp-gro-performance
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [udp-gro, ethtool, performance-tuning]
level: advanced
status: docs-checked
description: "Enable UDP GRO forwarding on the uplink device for subnet routers and exit nodes."
sources: ["https://tailscale.com/kb/1320"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Linux UDP GRO tuning

Goal: raise throughput on Linux subnet routers and exit nodes.

**Requirements.** Tailscale 1.54 or later with a Linux 6.2 or later kernel enables UDP throughput improvements using transport layer offloads.

**Command.** Find the network device used for internet routes and enable GRO forwarding:
```
NETDEVS=$(
  (ip -4 -o route get 8.8.8.8; ip -6 -o route get 2001:4860:4860::8888) 2>/dev/null |
    awk '{for (i = 1; i < NF; i++) if ($i == "dev") print $(i + 1)}' |
    sort -u
)
for NETDEV in $NETDEVS; do
  sudo ethtool -K "$NETDEV" rx-udp-gro-forwarding on rx-gro-list off
done
```
It looks up the IPv4 and IPv6 routes to the internet, extracts the device name after `dev`, and de-duplicates with `sort -u`. The two addresses are Google Public DNS, used only as well-known internet targets.

**Persistence.** `ethtool` changes do not survive reboot. Check `systemctl is-enabled networkd-dispatcher`; if it is enabled, add a script it runs each time the network connects. If both networkd-dispatcher and NetworkManager are enabled, follow only the NetworkManager steps. If neither is enabled, consider a oneshot systemd service.

**Direct connections.** To raise the chance of direct connections, expose a public IP, open a firewall port when needed, use the device connectivity guide, or add Tailscale Peer Relay servers.

**Checklist**

1. Version and kernel meet minimums.
2. Settings applied to the right device.
3. Made persistent.

## Checked

2026-11-09. Confirmed against the Tailscale Performance best practices page: the version and kernel minimums, the ethtool snippet and its explanation, persistence guidance for networkd-dispatcher and NetworkManager, and the direct connection advice. Nothing removed.

Method: docs-checked 2026-11-09 against tailscale.com/kb/1320 (Performance best practices), read in full.
