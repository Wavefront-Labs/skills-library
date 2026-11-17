---
id: computing-software.networking-hardware-and-wireless.wireguard.wireguard-physical-namespace-whole-host-vpn
name: wireguard-physical-namespace-whole-host-vpn
category: computing-software
field: networking-hardware-and-wireless
product: wireguard
tags: [network-namespace, physical-namespace, wlan0, dhcpcd, wpa-supplicant, whole-host-vpn, ip-netns-exec]
level: advanced
status: docs-checked
description: "Move physical NICs into a namespace so the init namespace only sees wg0, then run captive-portal tools inside the physical one."
sources: ["https://www.wireguard.com/netns/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Whole-host VPN with a physical namespace

Inverse of the container setup: move eth0 and wlan0 into a namespace named `physical`, create wg0 in that namespace so its UDP sockets bind there, then move wg0 into the init namespace (PID 1) where it becomes the only interface.

```bash
ip netns add physical
ip link set eth0 netns physical
iw phy phy0 set netns name physical        # wireless moves by phy, not by wlan0
ip -n physical link add wg0 type wireguard
ip -n physical link set wg0 netns 1
wg setconf wg0 /etc/wireguard/wg0.conf
ip addr add 10.2.4.5/32 dev wg0
ip link set wg0 up
ip route add default dev wg0
```

Ordinary processes only see wg0; WireGuard's encrypted packets still leave through eth0/wlan0 because the socket lives in `physical`. Run the DHCP client and wpa_supplicant inside it: `ip netns exec physical dhcpcd -b eth0`, `ip netns exec physical wpa_supplicant -B -c/etc/wpa_supplicant/wpa_supplicant.conf -iwlan0`.

For a captive portal, run a single program in the physical namespace as your own user:

```bash
physexec() { sudo -E ip netns exec physical sudo -E -u \#$(id -u) -g \#$(id -g) "$@"; }
physexec chromium
```

The WireGuard page gives a full `wgphys up|down|exec` script, including how to move interfaces back on `down`. This replaces the classic routing-table approaches.

Verify: `ip link` in the init namespace shows lo and wg0 only; `ip -n physical link` shows the NICs.

## Checked

2026-11-03. Confirmed: The physical-namespace commands, iw phy move for wireless, namespace 1 as init, dhcpcd and wpa_supplicant in the physical namespace, the physexec function and the wgphys script against the WireGuard routing and network namespaces page. Removed: the claim that no exemption routes or fwmark rules are needed, replaced by the page's own framing.

Method: documentation only; no commands were run.
