---
id: computing-software.systems-network-administration.linux.mac-address-cloning-and-mtu-settings
name: mac-address-cloning-and-mtu-settings
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, cloned-mac-address, mtu-setting, mac-address, jumbo-frames, nmcli, pmtu]
level: practitioner
status: docs-checked
description: "Set MAC addresses and MTU on Linux interfaces: NetworkManager cloned-mac-address modes, systemd-networkd and ip link, jumbo frames end to end, and path-MTU testing."
sources:
  - https://networkmanager.dev/docs/api/latest/settings-802-3-ethernet.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.link.html
  - https://man7.org/linux/man-pages/man8/ip-link.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# MAC address and MTU settings

## MAC address
Temporary:
```bash
ip link set dev ens18 down; ip link set dev ens18 address 52:54:00:12:34:56; ip link set dev ens18 up
```
NetworkManager (persistent per connection):
```bash
nmcli con mod office ethernet.cloned-mac-address 52:54:00:12:34:56   # fixed value
nmcli con mod home-wifi wifi.cloned-mac-address stable                # hashed MAC from connection.stable-id and a machine-dependent key
nmcli con mod cafe wifi.cloned-mac-address random                     # new random MAC on each connect
nmcli con mod office ethernet.cloned-mac-address permanent            # permanent hardware address
nmcli con up office
```
- `preserve` leaves the device MAC untouched on activation; `stable` creates a hashed MAC from `connection.stable-id` and a machine-dependent key, so the address stays the same across reconnects. Wi-Fi also accepts `stable-ssid`.
systemd-networkd / udev link file:
```ini
# /etc/systemd/network/10-lan.link
[Match]
PermanentMACAddress=aa:bb:cc:dd:ee:ff
[Link]
MACAddress=52:54:00:12:34:56
MTUBytes=9000
```
Active-backup bonds set all slaves to the same MAC at enslavement unless `fail_over_mac` is changed (kernel bonding docs). Duplicate MACs on one segment cause address conflicts.

## MTU
```bash
ip link set dev ens19 mtu 9000                 # temporary
nmcli con mod storage 802-3-ethernet.mtu 9000  # persistent
ip -d link show ens19                          # -d: details
```
Rules for jumbo frames:
- Every hop on the L2 segment (NIC, switch ports, bridges, VLAN parents, the peer) must allow it.
- Overlays subtract their headers from the underlay MTU: for an IPv4 underlay of 1500, VXLAN costs 50 bytes (1450) and GRE 24 (1476).

## Test path MTU
```bash
ping -M do -s 8972 192.0.2.20      # 9000 - 20 IP - 8 ICMP header; -M do sets DF, so a smaller path MTU makes it fail
ping -M do -s 1472 example.com     # standard 1500 path
tracepath example.com              # reports the path MTU (pmtu) as it discovers it
```
Symptoms of MTU black holes: connections open but stall on large transfers while small pings work. Fix the MTU or clamp MSS (`iptables -t mangle -A FORWARD -p tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu`, which clamps to path MTU minus 40 for IPv4).

## Verify
- [ ] `ip link` shows the intended MAC and MTU after reboot.
- [ ] Don't-fragment ping at the full payload size succeeds to the peer.

## Checked

Date: 2026-10-25. Documentation release: NetworkManager settings reference text and libnm headers (NetworkManager main); systemd.link(5) (systemd main); ip-link(8); bonding.rst; ping(8)/tracepath(1) and iptables-extensions(8), read 2026-10-25.
Confirmed: `ethernet.cloned-mac-address` and `wifi.cloned-mac-address` values (preserve, permanent, random, stable; wifi also stable-ssid) and their meanings; `[Match] PermanentMACAddress=`, `[Link] MACAddress=`, `MTUBytes=`; `ip link set ... address|mtu`; fail_over_mac default (none: all slaves share one MAC); `--clamp-mss-to-pmtu` (path MTU minus 40 for IPv4); `ping -M do`; overhead figures are arithmetic for an IPv4 underlay.
Removed as unconfirmed: `wifi.scan-rand-mac-address` (not an NM connection setting in the reference read), the maxmtu grep, WireGuard and IPsec overhead figures, VLAN/bridge MTU rules, and the "first enslaved NIC" bond MAC claim.

Method: documentation only; no commands were run.
