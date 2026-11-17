---
id: computing-software.systems-network-administration.wireshark.traffic-capture-and-analysis
name: traffic-capture-and-analysis
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, tcpdump, tshark, dumpcap, packet-capture, pcap, pcapng, bpf, capture-filter, display-filter, ring-buffer, follow-tcp-stream, tcp-analysis, retransmission, zero-window, rtt, latency, tls, tls-handshake, sni, sslkeylogfile, decryption, span-port, port-mirroring, network-tap, protocol-analysis, network-troubleshooting]
level: advanced
status: docs-checked
description: "Capture with tcpdump/dumpcap and analyse in Wireshark: BPF vs display filters, ring buffers, TCP analysis flags and RTT, TLS handshakes, SSLKEYLOGFILE."
sources:
  - https://www.wireshark.org/docs/wsug_html_chunked/
  - https://www.wireshark.org/docs/dfref/
  - https://www.tcpdump.org/manpages/tcpdump.1.html
  - https://www.tcpdump.org/manpages/pcap-filter.7.html
  - https://www.wireshark.org/docs/man-pages/dumpcap.html
  - https://wiki.wireshark.org/TLS
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Traffic capture and analysis — capture at the right point, then let Wireshark point at the fault

**Goal:** get a clean capture of the problem traffic without dropping packets or filling
the disk, and turn it into evidence: "the server took 900 ms to answer", "the client
sent a RST", "the firewall dropped the SYN-ACK".

## 1. Capture at the right point
- Capture as close to the symptom as possible, and ideally on both ends simultaneously: if the
  client sent it and the server never saw it, the path is guilty.
- On a switch, use a SPAN/mirror port or a TAP. On a VM, capture in the guest or on the vSwitch.
- Sync clocks (NTP) on both capture points before comparing timestamps.

## 2. Capture filters (BPF) vs display filters
They are different languages. Capture filters (libpcap/BPF, see pcap-filter) decide what is
saved; display filters (Wireshark syntax) decide what is shown.

| Goal | Capture filter (tcpdump/dumpcap) | Display filter (Wireshark) |
|---|---|---|
| One host | `host 192.0.2.10` | `ip.addr == 192.0.2.10` |
| One port | `tcp port 443` | `tcp.port == 443` |
| Exclude SSH | `not port 22` | `!(tcp.port == 22)` |
| DNS | `udp port 53` | `dns` |
| SYNs only | `tcp[tcpflags] & tcp-syn != 0` | `tcp.flags.syn == 1 && tcp.flags.ack == 0` |

Exclude your own SSH session when capturing remotely, or you capture yourself.

## 3. Capture commands
```bash
# Quick look, no name resolution, full packets
sudo tcpdump -i eth0 -nn -s 0 'host 192.0.2.10 and tcp port 443'
# Long-running ring buffer: 10 files x 100 million bytes, oldest overwritten
sudo tcpdump -i eth0 -nn -w cap.pcap -C 100 -W 10 'tcp port 443'
# dumpcap (ships with Wireshark): ring buffer of 10 files of about 100 MB each
dumpcap -i eth0 -f "tcp port 443" -b filesize:100000 -b files:10 -w cap.pcapng
```
In tcpdump `-C` is in millions of bytes and `-W` is the file count; in dumpcap `filesize` is
in kB and `files` makes a ring buffer (it needs another criterion such as `filesize` to decide
when to switch files). Use a ring buffer for intermittent problems and stop it right after the
user reports the event. tcpdump prints "packets dropped by kernel" at the end; if it is non-zero,
raise the buffer (`--buffer-size` in tcpdump, `-B` in dumpcap, in MiB for dumpcap) or filter harder.
Treat pcaps as sensitive: they can contain credentials, cookies and personal data.

## 4. Analyse TCP
1. Statistics > Conversations and Protocol Hierarchy to find the flow that matters.
2. Right-click > Follow > TCP Stream (`tcp.stream eq N`) to isolate one connection.
3. `tcp.analysis.flags` shows every packet the TCP analysis flagged. Key ones:
   - `tcp.analysis.retransmission` and `tcp.analysis.fast_retransmission`: the sender resent data.
   - `tcp.analysis.duplicate_ack`: duplicate acknowledgements, a sign the receiver saw a gap.
   - `tcp.analysis.zero_window`: the receiver advertised a zero window, so look at the receiving
     application before the network.
   - `tcp.flags.reset == 1`: find who sent the RST and when.
4. Latency split: in the 3-way handshake, the SYN to SYN-ACK time seen at the client approximates
   network RTT. Request to first response byte minus RTT approximates server think time. Add
   `tcp.time_delta` (time since previous frame in this TCP stream) as a column and sort.
   `tcp.analysis.ack_rtt` gives per-ACK RTT; Statistics > TCP Stream Graphs includes a Round Trip
   Time graph.

## 5. Inspect TLS
- Filter `tls.handshake.type == 1` (ClientHello) and read `tls.handshake.extensions_server_name`
  (SNI), offered versions and ciphers. Type 2 is ServerHello (chosen version and cipher).
- Failures show as a TLS Alert (`tls.alert_message`) or a TCP reset after the ClientHello.
- Key log file: a universal decryption mechanism that works even with Diffie-Hellman key exchange.
  Firefox, Chrome and curl write it when the `SSLKEYLOGFILE` environment variable is set to the
  absolute path of a writable file (set it before starting the application). In Wireshark go to
  Edit > Preferences > Protocols > TLS and set the (Pre)-Master-Secret log filename (`tls.keylog_file`).
- An RSA private key only works if the cipher suite is not (EC)DHE, the protocol is SSLv3 or
  (D)TLS 1.0-1.2 (not TLS 1.3), the key matches the server certificate and the session was not
  resumed.
- Delete the key log afterwards; it decrypts everything it covers.

## 6. Command-line analysis
```bash
tshark -r cap.pcapng -Y 'tcp.analysis.retransmission' -q -z conv,tcp
tshark -r cap.pcapng -Y 'dns.flags.rcode != 0' -T fields -e frame.time -e dns.qry.name -e dns.flags.rcode
```

## Verify
- [ ] Capture point(s) chosen deliberately; both ends captured where possible.
- [ ] Capture reports zero kernel-dropped packets.
- [ ] You can state the problem with packet numbers and timestamps.
- [ ] Network RTT vs server response time separated for the slow transaction.
- [ ] pcap files and TLS key logs are stored securely and deleted when done.

## Checked
2026-11-09. Read: tcpdump man page (`-C` in millions of bytes, `-W` filecount, `--buffer-size`,
"dropped by kernel", `-s`), pcap-filter man page (`tcpflags`, `tcp-syn`), dumpcap man page (`-b`
`filesize` in kB, `files` ring buffer needing another criterion, `-B` in MiB), the Wireshark
field references for tcp, tls and dns (every display-filter field named above), the User's
Guide statistics and expert chapters (Conversations, Protocol Hierarchy, TCP Stream Graphs
Round Trip Time), and the Wireshark wiki TLS page (key log file behaviour, RSA key limits,
preference name). Removed: NIC offload and checksum warnings, claims about mirror ports
dropping packets, the 1 percent retransmission rule of thumb, the firewall idle-timeout gloss on
RSTs, the "Calculate conversation timestamps" preference name, and the SNI-proxy explanation.
Method: docs-checked 2026-11-09 against the tcpdump, pcap-filter, dumpcap and wiki TLS pages and the Wireshark tcp, tls, dns field references.
