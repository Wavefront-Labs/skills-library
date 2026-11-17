---
id: computing-software.systems-network-administration.wireshark.ioc-and-credential-extraction
name: ioc-and-credential-extraction
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, ioc-extraction, cleartext-credentials, credentials, network-forensics, threat-hunting, tshark]
level: practitioner
status: verified
description: "Pull indicators of compromise and exposed credentials from a pcap: domains, IPs, URLs, user agents, JA3/JA4, file hashes, and Wireshark's Tools > Credentials."
sources:
  - https://www.wireshark.org/docs/man-pages/tshark.html
  - https://github.com/FoxIO-LLC/ja4
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# IOC and credential extraction

## Credentials in cleartext
Tools > **Credentials** lists usernames/passwords Wireshark found. The User's Guide says the ftp, http, imap, pop and
smtp dissectors feed it (`tshark -q -z credentials` prints the same table; it listed an HTTP basic-auth user and an FTP
user in a synthetic capture). Telnet and Kerberos/NTLM are not in that list.
Filters:
```
http.authorization || ftp.request.command == "PASS" || pop.request.command == "PASS"
imap.request contains "LOGIN" || smtp.auth.password || ntlmssp.auth.username
```
Report found cleartext credentials as a finding and treat them as compromised.

## Indicators
```bash
# Domains queried
tshark -r cap.pcapng -Y "dns.flags.response==0" -T fields -e dns.qry.name | sort | uniq -c | sort -rn
# External IPs contacted
tshark -r cap.pcapng -q -z endpoints,ip
# URLs and user agents
tshark -r cap.pcapng -Y http.request -T fields -e http.host -e http.request.uri -e http.user_agent
# TLS SNI and client fingerprints (JA3/JA4 fields exist in recent Wireshark)
tshark -r cap.pcapng -Y "tls.handshake.type==1" -T fields -e ip.src -e tls.handshake.extensions_server_name -e tls.handshake.ja4
# Files transferred: export and hash
tshark -r cap.pcapng --export-objects http,objs/ -q && sha256sum objs/*
```
Check the results against your threat-intelligence sources and the org's allowlist.
Self-signed or odd certificates: see suspicious-certificate-detection for the subject/issuer fields.

## Handling
- Work on a copy; record the original file's hash for chain of custody.
- Do not open extracted objects on your workstation; use a sandbox.

## Verify
- [ ] IOC list (domains, IPs, URLs, hashes, fingerprints) produced with source packet references; credential findings reported.

## Checked
Run with TShark 4.4.1 on synthetic captures: the credential filters compile and matched (HTTP `Authorization`, FTP
PASS), `imap.request.password`/`smtp.auth.password` fields exist, `-z credentials` listed `HTTP basic auth` and `FTP` rows,
`--export-objects http,objs/ -q` wrote the two HTTP bodies (`a`, `a(1)`), `-z endpoints,ip` and the DNS/URL/SNI field
pipelines ran, `tls.handshake.ja4` printed (`t12d010100_...`). The credential-source list was corrected from the
Tools-menu text of the 4.4.1 User's Guide. References to Zeek and named intel services were removed.
