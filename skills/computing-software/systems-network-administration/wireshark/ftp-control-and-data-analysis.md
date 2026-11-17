---
id: computing-software.systems-network-administration.wireshark.ftp-control-and-data-analysis
name: ftp-control-and-data-analysis
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, ftp-analysis, ftp, ftp-data, passive-mode, protocol-analysis]
level: practitioner
status: verified
description: "Analyse FTP in Wireshark: control commands and reply codes, active vs passive data connections, NAT/ALG breakage, and FTPS limitations."
sources:
  - https://www.rfc-editor.org/rfc/rfc959
  - https://www.rfc-editor.org/rfc/rfc2428
  - https://www.wireshark.org/docs/dfref/f/ftp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FTP control and data analysis

## Filters
```
ftp                                  # control channel (TCP 21)
ftp-data
ftp.request.command == "PASV" || ftp.request.command == "EPSV"
ftp.response.code >= 400
ftp.request.command == "USER" || ftp.request.command == "PASS"    # cleartext credentials
ftp.passive.port                      # decoded port of a 227/229 reply
```

## Active vs passive
- Active (`PORT h1,h2,h3,h4,p1,p2`): server connects from port 20 (the default data port) to the client's announced port.
  Breaks through client-side NAT/firewalls.
- Passive (`227 Entering Passive Mode (h1,h2,h3,h4,p1,p2)`): client connects to the server's port.
  Port = p1*256 + p2. EPSV (`229 (|||50123|)`) omits the address and works with NAT and IPv6.

## Typical failures
| Capture shows | Cause |
|---------------|-------|
| 227 reply with a private IP to an internet client | server behind NAT not configured with its public passive address |
| SYNs to the passive port with no reply or RST | firewall not opening passive range |
| LIST hangs after 150 | data connection blocked; transfer never starts |
| 425 Can't open data connection | server could not connect (active mode) |
| 530 (text varies by server, e.g. "Login incorrect") | bad credentials (visible in PASS) |
| ALG rewrote PORT address incorrectly | compare PORT payload inside vs outside the firewall |

## FTPS
Explicit FTPS (`AUTH TLS`) encrypts control, so firewalls/ALGs cannot see PASV ports; the server's
passive range must be opened statically. Implicit FTPS uses 990. Wireshark decrypts only with key logs.

## Data transfer timing
Use Statistics > Conversations on the data connection for throughput; Export Objects > FTP-DATA to
extract files (the capture must include the data port: a capture filter of `port 21` records only the control channel).
FTP on a non-standard port needs `-d tcp.port==2121,ftp` (or Decode As).

## Verify
- [ ] A test transfer shows 150 then 226 replies and a data connection to the expected port.

## Checked (2026-10-22)
- Ran on Wireshark 4.4.1 over a loopback capture of Python `ftplib` against a minimal FTP server (PASV, RETR, a 530 login failure): every filter in the skill matched (`ftp.request.command == "PASV" || ...`, `ftp.response.code >= 400`, USER/PASS 4 packets, `ftp-data` showed `FTP Data: 109 bytes (PASV) (RETR img.png)`); `ftp.passive.port` decoded the 227 reply and equalled p1*256+p2; `--export-objects ftp-data` wrote `img.png`. A first capture with a `port 21`-style filter lost the data connection entirely, hence the new note.
- RFC 2428 EPSV reply format `229 Entering Extended Passive Mode (|||6446|)` confirmed in https://www.rfc-editor.org/rfc/rfc2428.txt; ports 20/21/989/990 confirmed in the IANA registry https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.csv (ftp-data 20, ftp 21, ftps-data 989, ftps 990 "control, over TLS/SSL"); active-mode port 20 is the RFC 959 default data port.
- RFC 959 text confirms 150, 226, 227 `(h1,h2,h3,h4,p1,p2)`, 425 "Can't open data connection", 530 "Not logged in" and the server default data port L-1 (20); RFC 4217 confirms `AUTH TLS` (https://www.rfc-editor.org/rfc/rfc4217.txt). Not captured here: EPSV and active PORT sessions, FTPS, NAT/ALG behaviour; the cause column of the failure table is interpretation of those reply codes, not tested.
