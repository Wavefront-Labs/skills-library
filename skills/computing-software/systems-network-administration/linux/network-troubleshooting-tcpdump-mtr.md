---
id: computing-software.systems-network-administration.linux.network-troubleshooting-tcpdump-mtr
name: network-troubleshooting-tcpdump-mtr
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, network-troubleshooting, tcpdump, mtr, netcat, nc, packet-capture, ss, ping, traceroute, nmap, curl, ethtool, mtu, path-mtu, conntrack, tshark, wireshark, dns-debug, latency, packet-loss, lpic-2, networking, sysadmin, arping, iperf3, nc-port-check, ip-neigh, tcpdump-filters]
level: practitioner
status: draft
description: "Work a Linux network problem layer by layer: link, addressing, routing, firewall, DNS, port reachability with nc/ss, path loss with mtr, and targeted tcpdump captures to read or hand to Wireshark."
sources:
  - https://www.tcpdump.org/manpages/tcpdump.1.html
  - https://www.tcpdump.org/manpages/pcap-filter.7.html
  - https://github.com/traviscross/mtr
  - https://man7.org/linux/man-pages/man8/ss.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network troubleshooting — bottom-up, with evidence, in under ten minutes

**Goal:** turn "the app can't reach X" into a specific broken layer with a capture that
proves it.

## 1. Ladder (stop at the first failure)
```bash
ip -br link; ethtool eth0 | grep -E 'Speed|Duplex|Link'     # L1/2: link up? 100/half = bad cable/port
ethtool -S eth0 | grep -iE 'err|drop|crc' | grep -v ' 0$'   # NIC counters
ip -br addr; ip route get 10.20.0.5                          # L3: which source IP/iface/gateway is chosen?
ping -c3 -W1 <gateway>; ip neigh                             # ARP: FAILED/INCOMPLETE = L2 problem
ping -c3 1.1.1.1; ping -c3 example.com                       # beyond gateway; DNS vs IP
getent hosts api.internal; resolvectl query api.internal     # DNS as the app sees it
nc -zv -w3 api.internal 443                                  # L4 reachability (TCP handshake only)
curl -sv --connect-timeout 5 https://api.internal/ -o /dev/null   # L7 incl. TLS; -k to isolate cert issues
ss -tnp state established '( dport = :443 )'                 # is the app actually connected?
```
Interpretations: `connect: No route to host` = ICMP unreachable (firewall REJECT or no
route); hang then timeout = DROP somewhere or asymmetric routing; `Connection refused`
= host reachable, nothing listening (or REJECT with tcp-reset). Check the server side with
`ss -tlnp | grep :443` and `nft list ruleset` / `iptables -S` / `firewall-cmd --list-all`.

## 2. mtr — where on the path packets die
```bash
mtr -rwzbc 100 api.internal         # report mode, 100 probes, show ASN, both names and IPs
mtr -rwc 50 -T -P 443 api.internal  # TCP probes to 443 when ICMP is deprioritised
```
- Loss that **starts at a hop and continues to the end** is real. Loss at one middle hop
  only (0 % after it) is ICMP rate-limiting on that router — ignore.
- `???` hops are routers that don't answer; fine if later hops respond.
- Run from both directions when possible; return paths differ.

## 3. tcpdump — capture only what matters
```bash
tcpdump -ni eth0 -c 50 'host 10.20.0.5 and port 443'
tcpdump -ni any -s0 -w /tmp/cap.pcap 'host 10.20.0.5 and not port 22'   # full packets to file
tcpdump -ni eth0 'tcp[tcpflags] & (tcp-syn) != 0 and tcp[tcpflags] & tcp-ack == 0'  # SYNs only
tcpdump -ni eth0 'icmp[icmptype] == icmp-unreach'                         # who sends unreachables
tcpdump -ni eth0 -vvv 'udp port 53'                                       # DNS queries/answers
tcpdump -ni eth0 'vlan and ...'                                           # tagged frames on a trunk
tcpdump -r /tmp/cap.pcap -nn 'tcp port 443' | head
```
- `-n` (no DNS), `-i any` (all interfaces, Linux cooked header — loses some L2 info), `-s0`
  full snaplen when writing, `-c` so you don't fill the disk, `-w` then analyse in Wireshark
  (`tshark -r cap.pcap -Y 'tcp.analysis.retransmission'`).
- Read the handshake: `[S]` → `[S.]` → `[.]`. Only `[S]` repeating = nothing comes back
  (drop/blackhole or no return route). `[R.]` after `[S]` = refused. `[S.]` seen on the
  server's capture but not the client's = return path broken.
- Capture on both ends simultaneously; the difference between them *is* the answer.
- Large flows stalling after the handshake: MTU. `ping -M do -s 1472 host` (1500 − 28);
  if `Frag needed` or silence, lower MTU or fix PMTUD (`ip link set eth0 mtu 1400` to test;
  `net.ipv4.tcp_mtu_probing=1` as a mitigation). VPNs/overlays are the usual culprit.
- Capturing in a container's namespace: `nsenter -t <pid> -n tcpdump -ni eth0 …`.

## 4. Other tools when the ladder points at them
- `ss -s`, `nstat -az | grep -iE 'retrans|listenoverflow|listendrops'` — kernel-level drops.
- `conntrack -L | grep 10.20.0.5`; `dmesg | grep conntrack` — NAT table full.
- `nmap -sS -p 1-1024 host` (needs root) / `nmap -sn 10.20.0.0/24` — what's listening / who's alive.
- `arping -I eth0 10.20.0.1` — duplicate IP (two MACs answer).
- `tc -s qdisc show dev eth0` — shaped/dropped at egress.
- `iperf3 -c host` — throughput vs expectation; half of nominal often = duplex or MTU.

## Failure modes
- Debugging from the wrong namespace/VRF (`ip vrf exec`, `ip netns exec`).
- Trusting `ping` through a firewall that drops ICMP but allows TCP (use `nc`/mtr -T).
- `tcpdump` on a bonded/bridged interface showing nothing: capture on the physical slave
  or use `-i any`.
- Forgetting rp_filter: packets arrive but are dropped silently when the reverse route
  points elsewhere — `sysctl net.ipv4.conf.all.rp_filter=2` or fix routing.

## Verify
- [ ] You can name the failing layer and the device (host, hop, firewall) responsible.
- [ ] A pcap or mtr report backs the claim and was shared with the owning team.
- [ ] After the fix, the original `curl`/`nc` test succeeds and loss in `mtr` is 0 % end-to-end.
