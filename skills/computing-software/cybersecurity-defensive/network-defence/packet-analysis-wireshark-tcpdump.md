---
id: computing-software.cybersecurity-defensive.network-defence.packet-analysis-wireshark-tcpdump
name: packet-analysis-wireshark-tcpdump
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [network-security-monitoring, packet-analysis, wireshark, tcpdump, tshark, bpf-filters, display-filters, pcap, protocol-analysis]
level: practitioner
status: docs-checked
description: "Capture and analyse packets with tcpdump, tshark and Wireshark: capture filters, display filters, following streams and extracting files and indicators."
sources: ["https://www.tcpdump.org/manpages/tcpdump.1.html", "https://www.tcpdump.org/manpages/pcap-filter.7.html", "https://www.wireshark.org/docs/man-pages/tshark.html", "https://wiki.wireshark.org/TLS"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Packet analysis with Wireshark and tcpdump

**Goal:** capture the right traffic and answer specific questions (what was sent, to whom,
by which protocol) from packets.

## Capture
```
tcpdump -i eth0 -n -s 0 -w case123_%Y%m%d%H%M.pcap -G 300 -W 48 'host 10.1.2.3 and not port 22'
tshark -i eth0 -f "port 53" -w dns.pcap
```
- Capture filters are BPF (`host`, `net`, `port`, `tcp[tcpflags] & tcp-syn != 0`); keep them tight on busy links.
- `-s` sets the snaplen; `-G rotate_seconds` rotates the `-w` file (the name needs a strftime time format or each file overwrites the last); `-W filecount` limits the number of files; `-n` skips name resolution.
- tshark `-f` takes a capture filter (pcap syntax); display filters (`-Y`) are less efficient on busy live captures and can lose packets.
- Capture where the traffic is visible: the host itself, a SPAN/TAP, or cloud traffic mirroring.

## Display filters (Wireshark/tshark)
Display filters use Wireshark's own syntax, different from capture filters. Look up exact field
names (for example for HTTP, DNS, TLS, SMB2 or Kerberos) in the Wireshark display filter
reference rather than from memory, and test them on a known packet before relying on them.

## Analysis workflow
1. Get an overview from protocol hierarchy and conversation statistics (GUI, or tshark `-q -z io,phs`).
2. Find heavy talkers by endpoint byte counts.
3. Follow a stream to read a session.
4. Export transferred objects (hash them, analyse safely).
5. Use tshark `-T fields -e <field>` for bulk extraction (see the tshark field extraction skill).

## Gotchas
- Encrypted traffic shows metadata only (for example SNI, sizes, timing).
- Decrypting TLS needs session keys: a key log file (the `SSLKEYLOGFILE` variable, honoured by Firefox, Chrome and curl) or, in limited cases, an RSA private key, per the Wireshark TLS wiki.
- Captures contain credentials and personal data: handle as evidence, restrict access.
- Dropped packets on busy captures: check tcpdump's "dropped by kernel" count (reported when it exits, if the OS supplies it).

## Verify
- [ ] Capture file hashed and stored with case notes (where, when, filter used).
- [ ] Conclusions cite frame numbers.

## Checked
2026-11-01. Confirmed in the tcpdump man page (`-G`, `-W`, `-w` with strftime, `-s snaplen`, "dropped by kernel"), pcap-filter man page (`tcp[tcpflags]` with `tcp-syn`), tshark man page (`-f` capture filter, display filter cost, `-T fields`, `-z io,phs`) and the Wireshark TLS wiki (key log, RSA key limits). Removed: the display-filter table and SNI one-liner (field names not confirmed), GUI menu paths, `-nn`, TLS 1.3 certificate and ECH claims, and the CompTIA citation.
Method: documentation only; no commands were run.
