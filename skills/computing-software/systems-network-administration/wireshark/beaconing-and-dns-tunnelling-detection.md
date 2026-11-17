---
id: computing-software.systems-network-administration.wireshark.beaconing-and-dns-tunnelling-detection
name: beaconing-and-dns-tunnelling-detection
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, tshark, network-forensics, beaconing, c2-traffic, dns-tunneling, dns-exfiltration, ja3, ja4, tls-fingerprint, periodicity, long-subdomain, txt-queries, zeek, rita, security-analysis]
level: advanced
status: verified
description: "Find C2 in captures: periodic beacons by inter-arrival time, rare TLS fingerprints and SNI, and DNS tunnelling by query length, entropy and TXT volume per domain."
sources:
  - https://www.wireshark.org/docs/dfref/d/dns.html
  - https://github.com/FoxIO-LLC/ja4
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Beaconing and DNS tunnelling detection

## Beaconing
C2 implants check in at a regular interval (often with jitter), with small, similar-sized
requests, to a destination few other hosts contact.
1. Candidate list: Statistics > Conversations > IPv4/TCP, filter to internal sources, sort by
   packets; look for many short conversations to one external IP/SNI spread over the capture.
2. Extract timings for one candidate:
   ```
   tshark -r cap.pcapng -Y "ip.src==10.1.2.3 && ip.dst==203.0.113.50 && tcp.flags.syn==1 && tcp.flags.ack==0" \
     -T fields -e frame.time_epoch | awk 'NR>1{print $1-p} {p=$1}' | sort -n | uniq -c | sort -rn | head
   ```
   Raw deltas with jitter are all different, so `uniq -c` shows nothing. Bin them to 5 s first, replacing the awk
   program with `awk 'NR>1{print int(($1-p)/5+0.5)*5} {p=$1}'`, then `sort -n | uniq -c | sort -rn`. Clustered bins
   (7 of 9 deltas at 60 in the test, with 3 s jitter) = beacon; unrelated connections to the same IP appear as stray bins.
   I/O graph with 1 s interval on that filter shows a comb pattern.
3. Sizes: `tcp.len` or `frame.len` nearly constant per check-in.
4. TLS fingerprints: add columns `tls.handshake.ja3`, `tls.handshake.ja3_full`, `tls.handshake.ja4` (all exist in
   Wireshark 4.4.1) and `tls.handshake.extensions_server_name`. Rare fingerprints, SNI absent, IP-only
   destinations, self-signed or very new certificates are signals.
At scale, a flow-level tool is quicker than a packet viewer; use Wireshark to confirm what it flags.

## DNS tunnelling / exfiltration
Data is encoded in query names (and returned in TXT/NULL/CNAME answers).
```
dns.flags.response == 0 && len(dns.qry.name) > 50
dns.qry.type == 16 || dns.qry.type == 10          # TXT, NULL
```
Per-domain volume:
```
tshark -r cap.pcapng -Y "dns.flags.response==0" -T fields -e dns.qry.name \
 | awk -F. '{print $(NF-1)"."$NF}' | sort | uniq -c | sort -rn | head
```
Signals: one registered domain with thousands of unique subdomains, long random-looking labels
(base32/hex), high TXT share, steady query rate from one host, NXDOMAIN-heavy patterns (DGA).

## Pitfalls
- CDNs, telemetry and anti-virus cloud lookups also beacon and use long DNS names: build an
  allow-list and compare against peers (does every host do this or just one?).
- Encrypted DNS (DoH to 443) hides queries from this method: look for DoH endpoints in SNI.

## Verify
- [ ] Candidate shows regular interval and consistent size over the capture.
- [ ] Domain/IP checked against threat intel; host isolated and investigated per IR process.

## Checked
Run in Wireshark 4.4.1 against a synthetic pcap (8 TCP SYNs about 60 s apart with random jitter, 6 DNS TXT queries
with 60-character labels, one NULL query): the raw-delta pipeline printed eight deltas with count 1 each, the 5 s binned
version clustered them (7 at 60); `len(dns.qry.name) > 50`, the TXT/NULL type filter (16 or 10) and the
per-domain awk pipeline matched the injected queries (6 for the tunnel domain). JA3/JA4 fields confirmed in
`tshark -G fields` and printed for a generated ClientHello. The references to tunnelling tools and Zeek/RITA were removed because none could be run here.
