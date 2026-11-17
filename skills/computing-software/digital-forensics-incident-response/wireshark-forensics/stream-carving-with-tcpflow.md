---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.stream-carving-with-tcpflow
name: stream-carving-with-tcpflow
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [tcpflow, stream-reconstruction, pcap-carving, network-forensics, dfir]
level: practitioner
status: draft
description: "Reconstruct TCP streams to files at scale with tcpflow: per-direction flow files, BPF filtering, HTTP decoding scanners, the DFXML report, and carving payloads from flows."
sources: ["https://github.com/simsong/tcpflow", "https://manpages.debian.org/testing/tcpflow/tcpflow.1.en.html", "https://forensics.wiki/tcpflow/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Stream carving with tcpflow

Wireshark's Follow Stream works one stream at a time. `tcpflow` (Simson Garfinkel) writes every TCP stream in a capture to separate files, one per direction, so you can grep, hash and carve across thousands of flows.

## Basic use
```bash
mkdir flows && tcpflow -r cap.pcapng -o flows
tcpflow -r cap.pcapng -o flows 'host 203.0.113.50 and port 80'   # BPF filter
tcpflow -r cap.pcapng -o flows -e http -a                        # enable HTTP scanner / all scanners
```
Output file names encode the flow: `010.001.002.003.49812-203.000.113.050.00080` (source then destination, zero-padded), plus a `report.xml` (DFXML) listing each flow with start/end times, byte counts and packets.

## Useful options
- `-a` runs all post-processing scanners (HTTP decompression and body extraction, etc.); `-e http` enables just HTTP. HTTP bodies are written as separate files (`...-HTTPBODY-001.html`), gunzipped where possible.
- `-Fk` / `-Ft` name formats add timestamps or put flows in time-bucketed directories (check `tcpflow -h` for your version).
- `-c` prints to console; `-C` prints without headers; `-B` binary output; `-T` custom filename template, e.g. `-T %T_%A%C%c.%a-%B%D` (check the man page for supported tokens).

## Investigation recipes
- Find every flow containing a string: `grep -l -a "cmd.exe" flows/*`.
- Carve files out of flows: `foremost -i flows/<flow> -o carved/` or `binwalk -e`; useful for custom C2 protocols with embedded PE/ZIP.
- Size triage: `report.xml` byte counts, sorted, show the large outbound flows (exfiltration candidates).
- Hash all flow files for a manifest: `sha256sum flows/* > flows.sha256`.

## Comparison
- tcpflow: fast, scriptable, per-direction files, minimal protocol knowledge.
- Wireshark/tshark Export Objects: protocol-aware (HTTP, SMB, FTP-DATA), better for named files.
- Zeek file extraction: inline, with metadata logs.
- NetworkMiner: GUI, host-centric.

## Gotchas
- tcpflow does not reassemble UDP and handles missing segments by leaving gaps; mid-stream captures start mid-protocol.
- Very large captures create huge directory listings; filter by BPF or split the capture first.
- TLS flows produce ciphertext only.

## Verify
For a sample flow, the tcpflow output matches Wireshark's Follow TCP Stream (raw) for the same direction byte for byte.
