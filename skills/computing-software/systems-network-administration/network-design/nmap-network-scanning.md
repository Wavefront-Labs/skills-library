---
id: computing-software.systems-network-administration.network-design.nmap-network-scanning
name: nmap-network-scanning
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, network-tools, nmap, port-scan, host-discovery, service-detection, nse, syn-scan, udp-scan, firewall-verification, asset-discovery, ncat]
level: practitioner
status: docs-checked
description: "Use nmap for authorised discovery and firewall verification: host discovery, SYN/connect/UDP scans, version detection, useful NSE scripts, timing, port states."
sources:
  - https://nmap.org/book/man.html
  - https://nmap.org/book/man-port-scanning-techniques.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network scanning with nmap

Only scan networks you own or are authorised in writing to test; scans trip IDS alerts and
some fragile devices (old PLCs, printers) misbehave.

## Common jobs
```
nmap -sn 10.20.0.0/24                         # host discovery only (ARP on local LAN, ICMP/TCP elsewhere)
sudo nmap -sS -p 22,80,443,3389 10.20.0.0/24  # SYN scan of chosen ports (needs root)
nmap -sT -p- 10.20.5.10                       # full TCP connect scan, all 65535 ports
sudo nmap -sU --top-ports 50 10.20.5.10       # UDP: slow, results often open|filtered
nmap -sV -sC 10.20.5.10                       # service/version detection + default safe scripts
nmap -Pn -p 443 203.0.113.10                  # skip ping when ICMP is blocked
nmap -6 -sS 2001:db8::10
```
Output: `-oA scan-20261016` writes normal, grepable and XML (for ndiff/import).
Compare runs: `ndiff old.xml new.xml`.

## Port states
| State | Meaning |
|---|---|
| open | service answered (SYN/ACK) |
| closed | host answered RST: reachable, nothing listening |
| filtered | no answer or ICMP unreachable: firewall dropping |
| unfiltered | ACK scan: reachable but state unknown |
| open/filtered | UDP or FIN/NULL scans: no answer, could be either |
Firewall verification: from each zone, scan the targets of every rule; expected "open" for allowed
services and "filtered" for everything else. "closed" means the firewall let the packet through.

## Useful NSE scripts
`--script ssl-enum-ciphers -p 443` (TLS versions/ciphers), `ssh2-enum-algos`, `smb-protocols`
(SMBv1 still on?), `dns-recursion` (open resolver), `ntp-monlist`, `snmp-info`, `http-title`.

## Timing and politeness
`-T3` default; `-T4` on fast LANs; `--max-rate 100` and `--scan-delay` for fragile/WAN targets;
avoid `-T5`. Large sweeps: `--min-hostgroup` and split by subnet.

## Gotchas
- Without root, nmap falls back to `-sT` connect scans and cannot do ARP discovery details.
- Results through NAT/load balancers describe the front-end, not the server.

## Verify
- [ ] Written authorisation and scan window recorded.
- [ ] Results match the documented firewall policy; unexpected open ports ticketed.

## Checked
2026-10-28. Confirmed against the Nmap reference guide pages (host discovery, port scanning techniques, timing and performance, output, briefoptions) and nsedoc pages: `-sn`, `-Pn`, `-sS`/`-sT`/`-sU`, `--top-ports`, `-oA` (normal, XML and grepable), ndiff, the listed NSE scripts, `--max-rate`, `--scan-delay`, `--min-hostgroup`, `-T3` default, `-T4` for reasonably fast reliable networks, `-T5` as the most aggressive template, the connect-scan fallback without raw packet privileges, and default ARP discovery on a local Ethernet. Removed: the SYN-proxy gotcha (not in the sources).
Method: documentation only; no commands were run.
