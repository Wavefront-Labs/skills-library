---
id: computing-software.systems-network-administration.wireshark.port-scan-and-arp-poisoning-detection
name: port-scan-and-arp-poisoning-detection
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, tshark, network-forensics, port-scan-detection, arp-poisoning-detection, syn-scan, nmap-signatures, arp-duplicate-address-detected, gratuitous-arp, on-path-attack, expert-info, security-analysis]
level: practitioner
status: verified
description: "Recognise scans and ARP poisoning in captures: SYN/connect/UDP scan signatures, stats that expose a scanner, duplicate-address and gratuitous ARP evidence of MITM."
sources:
  - https://www.wireshark.org/docs/dfref/t/tcp.html
  - https://wiki.wireshark.org/ARP
  - https://nmap.org/book/man-port-scanning-techniques.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Detecting port scans and ARP poisoning

## Port scans
Signatures (TCP flags filters):
| Scan | Filter | Tells |
|---|---|---|
| SYN (half-open) | `tcp.flags.syn==1 && tcp.flags.ack==0 && tcp.window_size <= 1024` | nmap's raw TCP builder defaults the window to 1024 and its SYN probes carry a fixed option set (nmap source `tcpip.cc`, `scan_engine_raw.cc`) |
| Responses: closed | `tcp.flags.reset==1 && tcp.flags.ack==1` | many RST/ACK from one target |
| Responses: open | SYN/ACK followed by scanner's RST (no handshake completion) | |
| Connect scan | full handshake then immediate RST/FIN, many ports | |
| FIN/NULL/Xmas | `tcp.flags == 0x001` (FIN), `tcp.flags == 0x000` (NULL), `tcp.flags == 0x029` (FIN+PSH+URG, Xmas) | rarely legitimate |
| UDP scan | many `udp` to sequential ports + `icmp.type==3 && icmp.code==3` replies | |
| Ping sweep | `icmp.type==8` to many destinations; ARP requests for every address in a subnet | |

Fast triage:
- Statistics > Conversations > TCP: sort by Address A; one source with hundreds of
  conversations of 1-2 packets each to many ports = scanner.
- Statistics > Endpoints: a host with an abnormal number of peers.
- `tshark -r cap.pcapng -Y "tcp.flags.syn==1 && tcp.flags.ack==0" -T fields -e ip.src -e tcp.dstport | sort | uniq -c | sort -rn | head`
  then count distinct destination ports per source.

## ARP poisoning (on-path)
Evidence:
- Expert info / filter `arp.duplicate-address-detected` or `arp.duplicate-address-frame`:
  Wireshark noticed one IP claimed by two MACs. In 4.4.1 the Info column reads "Gratuitous ARP for 10.0.10.1
  (Reply) (duplicate use of 10.0.10.1 detected!)"; both fields matched once the second MAC announced the gateway IP.
- Unsolicited ARP replies (`arp.opcode == 2` with no matching request) repeating every few
  seconds, especially claiming the gateway IP.
- The gateway's IP mapping to a MAC whose OUI is a laptop/VM vendor rather than the router/firewall.
- After poisoning, victim traffic to the internet shows the attacker's MAC as `eth.dst` while
  `ip.dst` is external; TTL may drop by one if the attacker routes it.
```
arp.opcode == 2 && arp.src.proto_ipv4 == 10.0.10.1     # who claims the gateway?
eth.dst == <attacker-mac> && !(ip.dst == 10.0.10.0/24)
```
Benign lookalikes exist: any failover of a gateway address, a VM migration or NIC teaming can announce an IP from a
new MAC, so look for repetition and redirected traffic before escalating.

## Response
Identify the switch port of the attacker MAC (trace-host-to-switch-port) and shut it using your switch vendor's
procedure; then review the access-layer protections your switches offer against forged ARP.

## Verify
- [ ] Scanner IP, time window, target list and port range documented from the capture.
- [ ] Poisoning confirmed by two MACs for one IP plus redirected traffic, not just a single gratuitous ARP.

## Checked
Run in Wireshark 4.4.1 on a synthetic pcap: eight SYN probes with window 1024 (all matched the SYN filter; the
per-source count pipeline printed `10.9.9.9` ports), one FIN, one NULL and one FIN+PSH+URG packet matched
`0x001`, `0x000`, `0x029` exactly once each, eight RST/ACK replies matched, a forged gateway ARP from a second MAC
raised `arp.duplicate-address-detected`, the two gateway-claim filters compiled and matched. nmap's default window of
1024 read from `tcpip.cc` on GitHub (`else tcp->th_win = htons(1024); /* Who cares */`); the SYN probe option block
is `TCP_SYN_PROBE_OPTIONS` in `scan_engine_raw.cc`. Switch-side steps are left to the vendor's procedure.
