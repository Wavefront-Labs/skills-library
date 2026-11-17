---
id: computing-software.systems-network-administration.wireshark.export-objects-http-smb-tftp
name: export-objects-http-smb-tftp
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, tshark, export-objects, export-http-objects, export-smb-objects, tftp, imf, dicom, file-extraction, follow-stream, tcp-reassembly, malware-analysis, network-forensics]
level: practitioner
status: gated
description: "Pull transferred files out of captures with File > Export Objects (HTTP, SMB, TFTP, IMF, DICOM) and tshark --export-objects, with reassembly prerequisites and safe handling."
sources:
  - https://www.wireshark.org/docs/wsug_html_chunked/ChIOExportSection.html
  - https://www.wireshark.org/docs/man-pages/tshark.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Export Objects (HTTP, SMB, TFTP and more)

## GUI
File > Export Objects > HTTP | SMB | TFTP | IMF (email) | DICOM | FTP-DATA (all six exporters are in tshark 4.4.1:
`tshark --export-objects help`).
The list shows packet number, host, content type, size and filename; filter by text, then
Save or Save All. Double-check the packet number to jump to the transfer.

## CLI (repeatable, scriptable)
```
mkdir -p ./objs
tshark -r cap.pcapng --export-objects http,./objs
tshark -r cap.pcapng --export-objects smb,./objs      # also: tftp, imf, dicom, ftp-data  (gated: unconfirmed, source is paywalled or blocked) for smb
# non-standard ports need -d, e.g. -d tcp.port==2121,ftp
sha256sum ./objs/*                      # hash before anything else touches them
```

## Prerequisites for complete files
- TCP reassembly on: Preferences > Protocols > TCP > "Allow subdissector to reassemble TCP
  streams" (default on), and HTTP "Reassemble HTTP bodies spanning multiple segments" and
  "Reassemble chunked transfer-coded bodies" / "Uncompress entity bodies".
- The capture must contain every segment. Packet loss on the capture side (dropped packets,
  snaplen too small) yields truncated objects: check `capinfos` and the TCP analysis flags for
  "previous segment not captured".
- **HTTPS**: objects only after TLS decryption (SSLKEYLOGFILE). HTTP/2 DATA over decrypted TLS is exported by the same
  `http` exporter (tested on 4.4.1 with a Node HTTP/2 server, PNG recovered and a 404 stream listed as a zero-length
  object); HTTP/3 was not tested here.
- SMB2/3 encryption (SMB 3 with encryption on) hides content; only metadata is visible (gated: unconfirmed, source is paywalled or blocked).

## Handling suspicious files
- Treat exported objects as live malware: export on an analysis VM, no auto-open, hash and
  submit hashes (not files) to reputation services unless policy allows sample upload.
- Filenames from HTTP can be crafted (path traversal-like names); Wireshark sanitises, but
  extract into an empty directory.

## When Export Objects is not enough
Protocols without an exporter (custom TCP): Follow TCP
Stream > "Show data as Raw" > Save as, then carve (see tcp-reassembly-and-file-carving). FTP data connections are
exported by `ftp-data` as long as the capture includes the data port (a capture filter of only port 21 loses it).

## Verify
- [ ] Exported file size equals Content-Length / SMB file size.
- [ ] Hash matches the server-side file if available.

## Checked (2026-10-22)
- Ran on Wireshark 4.4.1 with loopback captures I generated (Python http.server, a minimal FTP server and SMTP server, Node http2 server): `--export-objects http` recovered a PNG whose sha256 matched the served file, a chunked-transfer copy (identical hash) and a Content-Encoding gzip body already decompressed (1100 bytes from 41 on the wire); `--export-objects ftp-data` produced `img.png` (named from RETR, 109 bytes) and `--export-objects imf` produced `t.eml`; `--export-objects help` lists dicom, ftp-data, http, imf, smb, tftp. Exporting HTTP/2 over TLS with a key log returned `img.png` and `missing`.
- Reassembly prefs `http.desegment_body`, `http.dechunk_body`, `http.decompress_body`, `tcp.desegment_tcp_streams` are all TRUE by default in `tshark -G defaultprefs`.
- TFTP: a scapy-built RRQ plus 3 DATA/ACK blocks (1090 bytes) exported by `--export-objects tftp` as `cfg.bin`, byte-identical to the source.
- Not run: SMB and DICOM exports (no SMB/DICOM capture could be generated here; Windows loopback SMB is not visible to Npcap); only the exporter names were confirmed. The skill is therefore `gated`.
