---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.http-forensic-analysis
name: http-forensic-analysis
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [http-forensics, http, protocol-forensics, pcap, user-agent, export-objects, dfir]
level: practitioner
status: draft
description: "Analyse HTTP traffic in captures: request methods, hosts, URIs, user agents, status codes, content types, reassembly, spotting C2, exploit and exfiltration patterns."
sources: ["https://www.wireshark.org/docs/dfref/h/http.html", "https://datatracker.ietf.org/doc/html/rfc9110", "https://docs.zeek.org/en/master/logs/http.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# HTTP forensic analysis

**Goal:** understand what clients requested and received over cleartext HTTP (or decrypted
HTTPS), and spot malicious patterns.

## Wireshark filters
```text
http.request                                   all requests
http.request.method == "POST"                  uploads, C2 check-ins, exfil
http.response.code >= 400                      errors (scanning, failed exploits)
http.host contains "example"
http.user_agent contains "python" or http.user_agent contains "curl"
http.content_type contains "application/x-msdownload"   executables delivered
http.request.uri matches "\\.(exe|dll|ps1|hta|zip)$"
http.request.full_uri contains "/wp-admin"
```
Statistics -> HTTP -> Requests / Packet Counter / Load Distribution summarise hosts and codes.
Follow -> HTTP Stream shows full request/response; File -> Export Objects -> HTTP extracts
bodies.

## Patterns
- **Malware download**: GET for executable/script/archive from rare domain or raw IP, often
  with mismatched `Content-Type` or extension; check `Content-Length` vs saved file.
- **C2 over HTTP**: regular intervals, same URI with varying parameters, small POST bodies,
  base64/encrypted blobs, unusual headers (`X-` custom, cookie used as data channel), default
  framework URIs (Cobalt Strike malleable profiles change these).
- **Exploitation**: payloads in URIs or headers (`${jndi:ldap://`, `../../`, `<?php`,
  OGNL `%{`), followed by 200 and a second-stage download.
- **Exfiltration**: large POST/PUT to storage or paste sites, multipart uploads.
- **Proxy logs** show the same with less detail when no PCAP exists.

## Reassembly
Enable "Reassemble HTTP bodies spanning multiple TCP segments" and decompress gzip/chunked
(defaults); for missing packets, partial objects may be truncated.

## Verify
Hash exported objects and compare with files found on endpoints (Zone.Identifier HostUrl
matching the request URL), and confirm request timing against host process network events.
