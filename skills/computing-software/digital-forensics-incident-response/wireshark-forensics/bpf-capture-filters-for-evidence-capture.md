---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.bpf-capture-filters-for-evidence-capture
name: bpf-capture-filters-for-evidence-capture
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [bpf-capture-filter, dumpcap, ring-buffer, tshark, dfir]
level: practitioner
status: verified
description: "Write BPF capture filters for targeted evidence capture: host/net/port syntax, excluding noise, VLAN and tunnel pitfalls, and testing filters before deployment."
sources: ["https://www.tcpdump.org/manpages/pcap-filter.7.html", "https://www.wireshark.org/docs/wsug_html_chunked/ChCapCaptureFilterSection.html", "https://www.wireshark.org/docs/man-pages/dumpcap.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BPF capture filters for evidence capture

**Goal:** capture only what matters (a suspect host, a C2 range) at sustainable volume, without
accidentally filtering out the evidence.

## Syntax essentials (pcap-filter)
```text
host 10.1.2.3                         # either direction
src net 10.1.0.0/16 and not dst net 10.0.0.0/8
host 10.1.2.3 and not port 445 and not port 3389
tcp port 443 or udp port 53
ether host 00:11:22:33:44:55          # MAC (useful with DHCP churn)
tcp[tcpflags] & (tcp-syn) != 0 and tcp[tcpflags] & tcp-ack == 0   # SYN only (scan detection)
vlan and host 10.1.2.3                # tagged traffic: 'vlan' shifts offsets for following primitives
```
Capture filters (BPF) differ from Wireshark display filters (`ip.addr == x`); they are not interchangeable.

## Deploy
```bash
dumpcap -i eth1 -f "host 10.1.2.3" -b filesize:1000000 -b files:50 -w /evid/suspect.pcapng
tcpdump -i eth1 -s 0 -w /evid/suspect_%Y%m%d%H%M.pcap -G 3600 'host 10.1.2.3'
```
- Validate syntax: `dumpcap -i <iface> -f 'host 10.1.2.3 and not port 445' -d` or `tcpdump -d '...'` (both print the compiled BPF; errors show up front).
- Test against an existing capture: `tcpdump -r sample.pcap 'filter' | head`.

## Pitfalls
- **VLAN tags / QinQ**: without `vlan` in the filter, tagged packets on a SPAN of a trunk may not match `host` primitives.
- **Tunnels/encapsulation** (IP-in-IP tested; GRE, VXLAN and ERSPAN follow from the same offset rule): inner IPs are not matched by `host`; filter on the outer header or capture all and filter later.
- **NAT**: capture point determines which IPs you see (pre- or post-NAT).
- Excluding "noisy" ports (e.g. 443) may exclude C2. Prefer volume control by host scope and ring buffers rather than protocol exclusion.
- `-s` snaplen: keep full packets (`-s 0` / default 262144) for file extraction.

## Document
Record the filter string, interface, capture point and start/end time in the collection log: a filtered capture is only evidence of what the filter allowed.

## Verify
After deployment, a quick read of the first file shows the expected hosts and no unexpected gaps.

## Checked
Every filter in the syntax block was compiled with `dumpcap -d` on Wireshark 4.4.1 and the program run against a
synthetic capture (plain, 802.1Q-tagged, IPv6, fragmented, IP-in-IP): `vlan and host` matched only the tagged frame,
`host X and vlan` was rejected, the SYN-only expression matched only the SYN, and an IP-in-IP packet matched `host`
only on its outer address. The `dumpcap -b filesize/-b files` deployment line ran with smaller values (see the
ring-buffer skill); the `tcpdump -G`, `-w` strftime, `-s 0` and `-d` options are as documented on the tcpdump man page
(not run here, tcpdump is Linux-oriented). The vlan offset rule is quoted in the pcap-filter man page.
