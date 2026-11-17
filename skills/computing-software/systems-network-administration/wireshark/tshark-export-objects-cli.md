---
id: computing-software.systems-network-administration.wireshark.tshark-export-objects-cli
name: tshark-export-objects-cli
category: computing-software
field: systems-network-administration
product: wireshark
tags: [tshark, tshark-export-objects, export-objects, http, smb, imf, file-extraction, forensics]
level: practitioner
status: verified
description: "Extract transferred files from captures in bulk with tshark --export-objects for HTTP, SMB, TFTP, IMF, DICOM and FTP-DATA, then hash and triage them safely."
sources:
  - https://www.wireshark.org/docs/man-pages/tshark.html
  - https://www.wireshark.org/docs/wsug_html_chunked/ChIOExportSection.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tshark --export-objects

The GUI's File > Export Objects for one capture at a time; tshark does it in scripts across many
files.

## Usage
```
mkdir -p out/http out/smb
tshark -r cap.pcapng -Q --export-objects http,out/http
tshark -r cap.pcapng -Q --export-objects smb,out/smb
tshark -r cap.pcapng -Q --export-objects imf,out/mail
```
Supported protocols on 4.4.1 (`tshark --export-objects help`): `dicom`, `ftp-data`, `http`, `imf`, `smb`, `tftp`. `-Q` suppresses packet
output. The destination folder must already exist (tshark reports `The path to the file ... doesn't exist` otherwise). A request for
`/files/a.txt` produced `a.txt`; exporting the same capture into the same folder again produced `a(1).txt`, so duplicate names get a `(n)` suffix.

Restrict to part of the capture with a read filter:
```
tshark -r cap.pcapng -Y "ip.addr == 10.0.0.5" -Q --export-objects http,out/host5
```
(`-Y` and `-2 -R` both exported the object in a small test.)

## HTTPS
Objects from TLS traffic export only when decrypted:
```
tshark -r cap.pcapng -o tls.keylog_file:keys.log -Q --export-objects http,out/https
```
Whether HTTP/2 and HTTP/3 objects are exported depends on the version; the protocol list above shows only `http` (no separate http2 type) on 4.4.1, so test your own capture.

## Triage
```
cd out/http
sha256sum * > ../http.sha256
file * | sort -k2 | head
```
Submit hashes, not files, to reputation services first. Handle extracted content as untrusted: open
in an isolated VM, never on the analysis workstation.

## Gotchas
- Incomplete transfers (capture started mid-download, packet loss) can produce truncated files; compare
  size with `Content-Length`.
- Chunked/compressed HTTP is decoded only when the reassembly preferences are on
  (`http.desegment_body`, `http.dechunk_body`, `http.decompress_body`; all TRUE in `tshark -G defaultprefs` on 4.4.1).
- Large captures: run per stream subset to keep memory bounded.

## Verify
- [ ] Number of exported files matches the GUI's Export Objects list for the same capture.
