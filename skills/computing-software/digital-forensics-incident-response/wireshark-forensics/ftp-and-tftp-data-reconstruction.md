---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.ftp-and-tftp-data-reconstruction
name: ftp-and-tftp-data-reconstruction
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [ftp-forensics, tftp, file-extraction, wireshark, exfiltration, dfir]
level: practitioner
status: verified
description: "Reconstruct FTP and TFTP transfers from packet captures: control-channel commands and credentials, active/passive data channels, Export Objects FTP-DATA and TFTP, and verifying files."
sources: ["https://www.wireshark.org/docs/wsug_html_chunked/ChIOExportSection.html", "https://wiki.wireshark.org/FTP", "https://wiki.wireshark.org/TFTP", "https://www.rfc-editor.org/rfc/rfc959", "https://www.rfc-editor.org/rfc/rfc1350"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FTP and TFTP data reconstruction

FTP is still used for exfiltration (clear-text, scriptable from `ftp.exe`, malware with hardcoded FTP drop servers) and TFTP for network-device config theft and PXE abuse. Both are fully recoverable from captures when unencrypted.

## FTP control channel (TCP 21)
```text
ftp.request.command == "USER" || ftp.request.command == "PASS"   # credentials in clear
ftp.request.command in {"STOR", "RETR", "LIST", "CWD", "DELE"}
ftp.response.code == 227 || ftp.response.code == 229             # passive mode replies
```
`tshark -r cap.pcapng -Y ftp -T fields -e frame.time_utc -e ip.src -e ftp.request.command -e ftp.request.arg -e ftp.response.code` gives a session transcript. `STOR` = upload to server (exfiltration from the client's view), `RETR` = download.

## Data channel
- Passive: `227 Entering Passive Mode (a,b,c,d,p1,p2)` -> port = p1*256+p2; `229` EPSV gives the port directly. Active: client sends `PORT`.
- Wireshark links the data connection to the command when it sees both; filter `ftp-data` and use `ftp-data.command` / `ftp-data.current-working-directory` to see which file a stream belongs to.
- **File > Export Objects > FTP-DATA** exports each transferred file. If export fails (missing packets, unusual ports), follow the TCP stream of the data connection, show as Raw, and save.
- `TYPE A` (ASCII) transfers may have converted line endings; hash comparisons with the original can differ for text files.

## TFTP (UDP 69, then ephemeral ports)
Read (`RRQ`) and write (`WRQ`) requests carry the file name and mode; data travels in 512-byte blocks (or a negotiated `blksize`, RFC 2348) acknowledged one by one. Filter `tftp`, then **File > Export Objects > TFTP**. In a test with block 2 of 3 missing, the TFTP export wrote no file at all, so carve incomplete transfers from the packets (or Follow the UDP stream).
Use cases: `WRQ` from a router to an unknown server (config exfiltration), unexpected `RRQ` for boot images.

## FTPS / SFTP
FTPS (explicit `AUTH TLS` or implicit 990) needs TLS keys to decrypt; SFTP is SSH and not recoverable without session keys. Metadata (sizes, timing, server) still supports exfiltration volume estimates.

## Gotchas
- Some exfil tools use FTP over non-standard ports; use "Decode As" FTP on that port so Wireshark parses it.
- Large captures with packet loss produce truncated exports; check file size against the server's `150 Opening ... (N bytes)` response.

## Verify
Each extracted file's size matches the protocol-reported size, its hash is recorded, and the transfer direction and account are documented from the control channel.

## Checked
Run on Wireshark 4.4.1 against a synthetic capture (EPSV and PASV sessions with STOR and RETR, a TFTP WRQ, an FTP
server on port 2121): every filter matched the intended frames (the set filter only parses with commas),
`--export-objects ftp-data` wrote `secret.txt` (1200 bytes) and `a.bin` (300 bytes) with the right sizes, the PASV port
195*256+200 = 50120 matched the data connection, `ftp-data.command` and `ftp-data.current-working-directory` were
populated, `--export-objects tftp` wrote `running-config`, the transcript `-T fields` command ran, and
`-d tcp.port==2121,ftp` made the non-standard port decode as FTP. Implicit FTPS on TCP 990 is in the IANA registry, EPSV 229 in RFC 2428, the 227 reply in RFC 959 and `blksize` in RFC 2348.
