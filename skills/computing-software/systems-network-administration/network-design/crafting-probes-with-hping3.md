---
id: computing-software.systems-network-administration.network-design.crafting-probes-with-hping3
name: crafting-probes-with-hping3
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, network-tools, hping3, packet-crafting, firewall-testing, tcp-ping]
level: practitioner
status: docs-checked
description: "Use hping3 to craft TCP/UDP/ICMP probes: TCP SYN ping through ICMP-blocking firewalls, testing rules with specific flags and ports, traceroute by port, and MTU probing."
sources:
  - https://linux.die.net/man/8/hping3
  - https://github.com/antirez/hping
  - https://www.kali.org/tools/hping3/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Crafting probes with hping3

hping3 builds custom packets from the command line; needs root. Use only on networks you are
authorised to test.

## Common uses
```
hping3 -S -p 443 -c 3 www.example.com          # TCP SYN "ping": SA reply = open, RA = closed
hping3 -A -p 80 -c 3 10.0.0.5                  # ACK probe: RST back = unfiltered by stateless ACL
hping3 --udp -p 53 -c 3 10.0.0.53              # UDP; ICMP port unreachable = closed
hping3 -1 -c 3 10.0.0.1                        # ICMP echo
hping3 -S -p 443 --traceroute www.example.com  # traceroute with TCP/443 (passes firewalls allowing 443)
hping3 -S -p 22 -s 5050 -k 10.0.0.5            # fixed source port (match a specific rule)
hping3 -1 -d 1472 -y 10.0.0.1                  # -y sets DF; data size for MTU probing
hping3 -S -p 80 -i u10000 -c 1000 10.0.0.5     # 100 pps for latency/loss measurement
```
Flags: `-S` SYN, `-A` ACK, `-F` FIN, `-R` RST, `-P` PSH, `-U` URG; `-a` spoof source (lab only).

## Reading results
- `flags=SA` -> port open; `flags=RA` -> closed; nothing -> filtered.
- RTT per reply gives latency through ICMP-blocking paths (TCP SYN latency to an open port).
- Compare `-S` vs `-A` responses to infer stateful vs stateless filtering.

## Cautions
- Do not flood (`--flood`) production; it is a DoS tool as well.
- IDS/IPS will flag crafted scans; coordinate with security.

## Verify
- [ ] Test plan lists each probe, expected result per firewall policy, and observed result.

## Checked
2026-10-28. Confirmed against the hping3 man page: firewall testing, traceroute-like use, path MTU discovery, `--interval` with `uX` microsecond form, `--flood` (sends as fast as possible), reply format `flags=RA`, TCP flag options. Removed: the alternative-tools line (not in the sources). SYN/ACK versus RST/ACK meaning is standard TCP behaviour.
Method: documentation only; no commands were run.
