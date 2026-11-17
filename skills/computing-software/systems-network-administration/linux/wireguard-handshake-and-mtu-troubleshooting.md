---
id: computing-software.systems-network-administration.linux.wireguard-handshake-and-mtu-troubleshooting
name: wireguard-handshake-and-mtu-troubleshooting
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, wireguard, wg-show, wireguard-handshake, mtu, allowedips, endpoint, persistentkeepalive]
level: practitioner
status: docs-checked
description: "Debug WireGuard tunnels: reading wg show (latest handshake, transfer), no-handshake causes, AllowedIPs routing mistakes, NAT keepalive, MTU blackholes and kernel debug logs."
sources:
  - https://www.wireguard.com/quickstart/
  - https://man7.org/linux/man-pages/man8/wg.8.html
  - https://man7.org/linux/man-pages/man8/wg-quick.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WireGuard troubleshooting

## Read wg show
```bash
wg show wg0
# prints the interface, then each peer with endpoint, allowed ips, latest handshake and transfer counters
wg show wg0 latest-handshakes ; wg show all dump      # script-friendly
```
WireGuard tries to be as silent as possible when not in use, so a missing handshake gives no error message.

## No handshake ("latest handshake" missing)
- UDP port blocked: `tcpdump -ni eth0 udp port 51820` on both ends — packets leaving? arriving?
- Wrong public key on either side (`wg show wg0 public-key` vs peer config), wrong endpoint/port.
- Behind NAT with no inbound path: the NATed side must initiate; `PersistentKeepalive` (1-65535 s, off by default; the man page cites 25 s as an example) keeps the NAT mapping alive.

## Handshake OK but no traffic
- **AllowedIPs**: the addresses from which incoming traffic for the peer is allowed and to which outgoing traffic for the peer is directed (wg(8)). Check that the packet source and destination fall inside the right peer's list.
- Routes: the `wg` tool does not set addresses or routes (use `ip address` and `ip route`); `wg-quick up` does set up addresses and routes, while manual setups need e.g. `ip route add 192.168.50.0/24 dev wg0`.
- Forwarding for site-to-site: `net.ipv4.ip_forward=1`, firewall forward rules, NAT/masquerade or return routes on the LAN.
- `net.ipv4.conf.*.rp_filter=1` (strict) can discard asymmetric traffic.

## MTU
`wg-quick` determines the MTU automatically from the endpoint addresses or the default route unless `MTU =` is set in the config. Symptoms of a too-large MTU: small pings work but large transfers stall.
Test with `ping -M do -s <MTU-28> 10.8.0.1` (payload = MTU minus 20 IP and 8 ICMP header bytes), lower `MTU =` if it fails, or clamp MSS on the forwarder.

## Kernel debug
```bash
modprobe wireguard && echo module wireguard +p > /sys/kernel/debug/dynamic_debug/control   # per the WireGuard quickstart; needs dynamic debug support in the kernel
dmesg -w | grep wireguard
```

## Verify
- [ ] `latest handshake` is recent while traffic flows; large transfers succeed; `transfer` counters increase both ways.

## Checked

Date: 2026-10-25. Documentation release: wg(8) and wg-quick(8) (WireGuard/wireguard-tools master), the WireGuard quickstart page (wireguard.com), kernel ip-sysctl.rst, ping(8), read 2026-10-25.
Confirmed: `wg show` subcommands including latest-handshakes and dump; AllowedIPs definition; `PersistentKeepalive` range, default off and the 25 s example; wg-quick MTU auto-detection and the `MTU` key; the dynamic_debug command; `rp_filter` values; `ping -M do`.
Removed as unconfirmed: the sample peer output, the 1420 default and its explanation, the "last overlapping AllowedIPs wins" rule, the clock and duplicate-key remarks, the 2-minute handshake threshold, example kernel log strings, and the wireguard.com/netns link.

Method: documentation only; no commands were run.
