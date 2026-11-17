---
id: computing-software.cybersecurity-defensive.network-defence.file-carving-from-pcap
name: file-carving-from-pcap
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [network-security-monitoring, file-carving-pcap, wireshark-export-objects, tshark, zeek-file-extraction, networkminer, malware-sample-recovery]
level: practitioner
status: docs-checked
description: "Recover transferred files from packet captures for analysis: Wireshark Export Objects, tshark --export-objects, Zeek file extraction, NetworkMiner, hashing and safe handling."
sources: ["https://www.wireshark.org/docs/wsug_html_chunked/ChIOExportSection.html", "https://docs.zeek.org/en/master/frameworks/file-analysis.html", "https://www.netresec.com/?page=NetworkMiner", "https://www.wireshark.org/docs/man-pages/tshark.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# File carving from PCAP

When a host downloaded a payload or exfiltrated a file over a cleartext protocol, the bytes are in the
capture. TLS traffic needs decryption first: NetworkMiner states it does not decrypt, so files inside HTTPS
are not extracted unless you decrypt the traffic (for example with a TLS proxy) before analysis.

## Wireshark / tshark
GUI: File > Export Objects, choose the protocol. Wireshark scans that protocol's streams in the open capture
and exports the reassembled objects to disk (for HTTP: HTML documents, images, executables and other files);
for HTTP the filename is the final part of the URI, for IMF the email subject.
CLI:
```
tshark -r case.pcap --export-objects http,./out_http
tshark -r case.pcap -Y 'http.request.uri contains ".exe"' -T fields -e frame.time -e ip.src -e http.host -e http.request.uri
```
`--export-objects <protocol>,<destdir>` exports all objects of a protocol into a directory; run
`tshark --export-objects help` to list the available protocols. `-Y` applies a display filter and `-T fields`
with `-e` prints chosen fields.

## Zeek file extraction
Zeek raises file events (`file_new`, `file_over_new_connection`, `file_sniff`, `file_timeout`, `file_gap`,
`file_state_remove`) giving the connection, protocol and MIME type of a file. To extract, attach the
`Files::ANALYZER_EXTRACT` analyzer to a file, typically in a `file_sniff` handler:
```zeek
event file_sniff(f: fa_file, meta: fa_metadata)
    {
    Files::add_analyzer(f, Files::ANALYZER_EXTRACT,
                        [$extract_filename=fmt("file-%04d", ++idx)]);
    }
```
(declare a counter `idx` yourself). Extracted files are written under `FileExtract::prefix`, normally
`./extract_files/`. Zeek ships the `policy/frameworks/files/extract-all-files.zeek` script as a starting
point; filter by MIME type in production rather than extracting everything.

## NetworkMiner
Extracts files from FTP, HTTP, HTTP/2, IMAP, POP3, SMB, SMB2, SMTP, TFTP and several other protocols, plus
credentials and X.509 certificates; the free edition and Professional both list file extraction.

## After carving
- Hash (SHA256) immediately and record with the source frame, time and hosts (chain of custody).
- Analyse only in a malware lab; check reputation by hash before uploading a sample anywhere.
- Partial captures produce truncated files; compare size with the HTTP `Content-Length`.

## Verify
Carve a known test download from a lab host and confirm the hash matches the original.

## Checked
Checked 2026-11-09 against the Wireshark User's Guide Export Objects section, the tshark man page
(`--export-objects`, `-Y`, `-T fields`, `-e`), the Zeek file analysis framework page (events, extract
analyzer, `extract_files/`, extract-all-files policy script) and the NetworkMiner page (supported
protocols, HTTPS decryption FAQ). Removed as unconfirmed: the SMB tshark example, TLS key-log GUI path,
`zeek -C -r` and `hash-all-files`, the `files.log` contents, the `infected` zip password convention,
chunked/gzip and SMB encryption remarks, and the `tcp.analysis.lost_segment` tip.
Method: docs-checked 2026-11-09 against the pages named above.
