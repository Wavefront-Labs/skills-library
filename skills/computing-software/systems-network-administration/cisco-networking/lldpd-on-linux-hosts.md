---
id: computing-software.systems-network-administration.cisco-networking.lldpd-on-linux-hosts
name: lldpd-on-linux-hosts
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [lldp, lldpd, lldpctl, lldpcli, linux, cdp, topology-discovery, server-cabling]
level: practitioner
status: docs-checked
description: "Run lldpd on Linux servers to see which switch port each NIC is cabled to and control what the host advertises: lldpcli queries, CDP, port ID, timers, receive-only."
sources:
  - https://lldpd.github.io/usage.html
  - https://manpages.debian.org/stable/lldpd/lldpcli.8.en.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# lldpd on Linux hosts

lldpd is a daemon that sends and receives LLDP frames; lldpcli queries and configures it. Together they answer
"which switch port is this NIC cabled to?" from the server side and advertise the host's identity to the switch.

## Query neighbours
```
lldpcli show neighbors
lldpcli show neighbors ports eth0 details
lldpcli show neighbors summary
lldpcli show statistics
lldpcli -f json show neighbors
lldpcli watch
```
- `summary` shows only the name and port description of each remote host; `details` shows everything available.
- `hidden` also shows remote ports hidden by the smart filter.
- `-f` selects the output format: plain (default), xml, json, json0 and keyvalue. json0 is more verbose but its
  structure does not change with the number of interfaces or neighbours, so it is easier to parse.
- `watch` reports neighbour changes as they happen; `limit X` exits after X events.
- `show statistics` reports LLDPDUs transmitted, received, discarded or unrecognised.
- `show interfaces` and `show chassis` describe the local side.

## Speak CDP and other protocols (daemon flags)
- `-c` enables CDP to deal with Cisco routers that do not speak LLDP. Repeating it sends CDPv1 packets even with no CDP
  peer, then CDPv2, and `-cccc` disables CDPv1 and enables CDPv2; `-ccccc` forces CDPv2.
- `-f` FDP, `-s` SONMP, `-e` EDP likewise.
- By default lldpd sends LLDP when an LLDP peer is detected or when there is no peer at all, and speaks any protocol
  from which it has received a frame. `-l` forces LLDP when only another protocol is seen.
- `-r` is receive-only: lldpd sends no frames and only listens to neighbours.
- `-I` restricts the interfaces used, with wildcards, `!` to exclude and `!!` to re-allow; for example
  `eth*,!eth1,!eth2`. Without it all physical interfaces are used.
- `-i` stops sending the LLDP-MED inventory TLVs, which the man page notes can carry sensitive information such as
  serial numbers.
- Where the daemon arguments are set depends on the distribution package (not covered by the pages checked).

## Configuration commands (lldpcli, also read from lldpd.conf and the lldpd.d directory at start)
```
configure system hostname web01.example.net
configure system description "web01 rack B3"
configure lldp portidsubtype ifname
configure system interface pattern eno*,ens*,!docker*,!veth*
configure lldp tx-interval 30
configure lldp tx-hold 4
configure ports eth0 lldp status rx-only
```
- Hostname defaults to the FQDN from `uname -n`; the value `.` uses the short hostname.
- Port ID: by default lldpd uses the MAC address as port identifier and the interface name as port description,
  unless the interface has an alias (then name is ID and alias is description). `portidsubtype` forces ifname,
  macaddress or a local value.
- `tx-interval` is the delay between LLDPDUs, range 1-3600 seconds, default 30. `tx-hold` range 1-100, default 4;
  TTL is the product, so 120 seconds by default.
- Port status: `rx-and-tx` (default), `rx-only`, `tx-only` or `disabled`. It does not override a daemon started
  with `-r`.
- `configure lldp fast-start enable` shortens the interval for a new neighbour; default 1 second, disabled after 4
  LLDPDUs until a new neighbour appears.
- `configure lldp agent-type` picks the destination MAC: default 01:80:c2:00:00:0e (nearest bridge); nearest
  non-TPMR bridge uses 01:80:c2:00:00:03; nearest customer bridge uses 01:80:c2:00:00:00.
- `lldpcli reset` discards runtime and file configuration changes and returns to the startup configuration; reread
  the files with `lldpcli -c <file> -c <dir>` to reload without restarting.

## Gotchas stated in the man page
- Cisco 2960 with a NIC that does VLAN hardware acceleration: LLDP frames may not arrive, probably because they are
  tagged (usually VLAN 1) and the NIC filters VLANs. Workarounds: `configure system interface promiscuous` (Linux
  only), disabling VLAN acceleration, or tagging VLAN 1 on each interface.
- With bond slaves, `configure system bond-slave-src-mac-type` sets the source MAC of LLDP frames: real, zero, fixed or
  local (default local). Some switches complain about zero or fixed.
- Different protocols from one port: a Nortel switch speaking LLDP behind a Cisco switch speaking CDP is visible
  because the Cisco switch forwards LLDP frames; the `-H` hide option filters this.

## Verify
- [ ] `lldpcli show neighbors` lists the expected switch and port for each cabled NIC.
- [ ] `lldpcli show statistics` shows frames received on that port.

## Checked
Checked 2026-11-08 against the lldpd usage page (lldpd 1.0.23 man pages) and the Debian lldpcli man page. Removed:
the apt/dnf/systemctl install steps, the /etc/default/lldpd location, ESXi and Proxmox advice, the Intel/Broadcom
firmware LLDP trap and ethtool flag, the claim that Cisco ships LLDP off, and the Cisco switch-side commands, none of
which are on those pages.
Method: documentation only; no commands were run.
