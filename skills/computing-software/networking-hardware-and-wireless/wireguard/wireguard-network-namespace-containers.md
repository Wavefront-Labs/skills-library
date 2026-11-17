---
id: computing-software.networking-hardware-and-wireless.wireguard.wireguard-network-namespace-containers
name: wireguard-network-namespace-containers
category: computing-software
field: networking-hardware-and-wireless
product: wireguard
tags: [network-namespace, ip-netns, container-networking, docker, birthplace-namespace, wg-in-container]
level: advanced
status: docs-checked
description: "Give a container or namespace a WireGuard interface as its only network path, using the birthplace-namespace property."
sources: ["https://www.wireguard.com/netns/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# WireGuard as a container's only interface

A WireGuard interface remembers the network namespace where it was created, and its encrypted UDP socket always lives there, even after the interface is moved. So you can create wg0 in the host namespace, move it into a container namespace, and cleartext sent inside the container leaves encrypted from the host.

```bash
ip netns add container
ip link add wg0 type wireguard
ip link set wg0 netns container
ip -n container addr add 192.168.4.33/32 dev wg0
ip netns exec container wg setconf wg0 /etc/wireguard/wg0.conf
ip -n container link set wg0 up
ip -n container route add default dev wg0
```

Now the only way out of `container` is wg0. For Docker, pass the PID of a container process instead of a namespace name: `ip link set wg0 netns 879`.

Configure with `ip -n <ns>` and `ip netns exec <ns> wg ...` as above.

Verify: `ip -n container link` lists wg0 in the container namespace.

## Checked

2026-11-03. Confirmed: The container namespace command sequence, the Docker PID variant and the birthplace-namespace behaviour (as described later on the page) against the WireGuard routing and network namespaces page. Removed: the userspace TUN paragraph and the wg-quick / leak-prevention claims (not on the fetched text).

Method: documentation only; no commands were run.
