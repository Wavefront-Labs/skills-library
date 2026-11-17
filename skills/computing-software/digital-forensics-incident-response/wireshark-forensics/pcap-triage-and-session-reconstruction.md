---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.pcap-triage-and-session-reconstruction
name: pcap-triage-and-session-reconstruction
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [wireshark, tshark, pcap, pcapng, network-forensics, dfir, display-filters, follow-tcp-stream, export-objects, statistics-conversations, protocol-hierarchy, dns, http, tls, sni, ja3, ja4, beaconing, exfiltration, ioc-extraction, capinfos, editcap, mergecap, zeek]
level: practitioner
status: draft
description: "Triage a packet capture in Wireshark/tshark: size it up, find top talkers, reconstruct sessions, carve transferred files, pull DNS/TLS indicators, spot beaconing."
sources: ["https://www.wireshark.org/docs/wsug_html_chunked/", "https://www.wireshark.org/docs/dfref/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PCAP triage and session reconstruction with Wireshark

**Goal:** from a capture of unknown content, find the hosts and sessions that matter,
reconstruct what was said or transferred, and extract indicators (IPs, domains, hashes)
to pivot on — in a repeatable way you can write up.

## 1. Size it up before opening it
```bash
sha256sum case.pcapng > case.pcapng.sha256
capinfos case.pcapng          # duration, packet count, first/last packet time, snaplen
```
- A **snaplen** below full frame size (e.g. 96 bytes) means payloads are truncated —
  you can do flow analysis but not file carving.
- Captures over ~1–2 GB are painful in the GUI. Split or pre-filter:
  `editcap -c 1000000 big.pcapng part.pcapng` or
  `tshark -r big.pcapng -Y "ip.addr==10.0.0.5" -w host.pcapng`.

## 2. Overview (Statistics menu, or tshark)
```bash
tshark -r case.pcapng -q -z io,phs              # protocol hierarchy
tshark -r case.pcapng -q -z conv,tcp            # TCP conversations, bytes each way
tshark -r case.pcapng -q -z endpoints,ip
```
Look for: large outbound byte counts (exfil), protocols on unexpected ports (Wireshark
flags many via its heuristics; `Analyze › Decode As` to force one), long-lived
connections, and internal hosts talking to each other over SMB/RDP/WinRM (lateral movement).

## 3. Display filters that pay off
```
dns.flags.response == 0                      # all DNS queries
dns.qry.name contains "xyz"                  # a suspect domain
http.request                                 # HTTP requests (method, host, URI, UA columns)
http.request.method == "POST"
tls.handshake.type == 1                      # TLS ClientHello: SNI lives here
tls.handshake.extensions_server_name
tcp.flags.syn == 1 && tcp.flags.ack == 0     # connection attempts / scans
smb2 || dcerpc || kerberos                   # lateral-movement-ish traffic
frame.time >= "2026-09-03 14:00:00"          # time window (display timezone applies!)
```
Set `View › Time Display Format` to **UTC Date and Time of Day** so your notes match
other evidence. Add columns (right-click a field › Apply as Column) for `http.host`,
`tls.handshake.extensions_server_name`, `dns.qry.name`.

## 4. Reconstruct sessions
- Right-click a packet › **Follow › TCP Stream** (or HTTP/TLS/UDP Stream). Switch
  "Show data as" to Raw to save the byte stream; use the direction drop-down to see
  each side separately.
- **File › Export Objects › HTTP / SMB / TFTP / IMF / FTP-DATA** carves transferred
  files. Hash every exported file and treat it as live malware.
- tshark equivalent: `tshark -r case.pcapng --export-objects http,out/`.
- **TLS is opaque** without keys. If you have an `SSLKEYLOGFILE` from the client
  (or the server's RSA key for old non-PFS suites), set it under
  Preferences › Protocols › TLS. Otherwise work from metadata: SNI, certificate
  subject/issuer, JA3/JA4 fingerprint (JA4 via plugin/newer builds — check yours),
  timing and size.

## 5. Extract indicators in bulk
```bash
tshark -r case.pcapng -Y "dns.flags.response==0" -T fields -e frame.time_epoch -e ip.src -e dns.qry.name > dns.tsv
tshark -r case.pcapng -Y "tls.handshake.type==1" -T fields -e ip.dst -e tls.handshake.extensions_server_name | sort | uniq -c | sort -rn
tshark -r case.pcapng -Y http.request -T fields -e ip.src -e http.host -e http.request.uri -e http.user_agent
```
**Beaconing:** filter one host→destination pair and look at `frame.time_delta_displayed`
or the I/O graph: near-constant intervals (e.g. every 60 s ± jitter) with similar sizes
suggest C2. For long captures, Zeek logs (`conn.log`) plus a beacon-scoring tool scale
better than eyeballing.

## Gotchas
- Wireshark dissectors have had security bugs: open untrusted captures on an analysis
  VM, keep Wireshark updated, and don't run it as root (capture via `dumpcap` group).
- "TCP Previous segment not captured" and retransmission noise in a capture taken on
  a busy SPAN port often mean **dropped packets at capture**, not attacker behaviour.
- NAT and proxies hide the real internal host: correlate with proxy/firewall logs.

## Verify
- [ ] Capture hashed; capinfos recorded (time range, snaplen).
- [ ] Time display set to UTC before noting any timestamp.
- [ ] Each finding cites a filter or stream number someone else can reproduce.
- [ ] Exported files hashed and moved to the malware lab, not opened locally.
- [ ] Indicator list (IPs, domains, SNI, URIs, hashes) exported as text for pivoting.
