---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.networkminer-artefact-extraction
name: networkminer-artefact-extraction
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [networkminer, pcap-analysis, file-extraction, credentials, host-profiling, passive-os-fingerprinting, dfir]
level: practitioner
status: draft
description: "Use NetworkMiner to profile hosts and extract files, images, credentials, DNS, sessions and certificates from pcaps for fast passive network triage."
sources: ["https://www.netresec.com/?page=NetworkMiner", "https://www.netresec.com/?page=Blog"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NetworkMiner artefact extraction

**Goal:** a fast, host-centric view of a capture: what each host is, what files and
credentials crossed the wire, without building filters.

## Load
NetworkMiner (Windows, or Linux via Mono): File > Open (pcap/pcapng), or drag files in.
Free edition handles pcap/pcapng; Professional adds PcapNG comments, GeoIP, port-independent
protocol identification, OSINT lookups and command-line batch processing (NetworkMinerCLI).
It never transmits; it is fully passive and safe offline.

## Tabs
| Tab | What you get |
|---|---|
| Hosts | each IP: MAC/vendor, hostname, OS guess (p0f/Satori fingerprints), open ports, sessions, user-agents |
| Files | reassembled files from HTTP, SMB, FTP, TFTP, SMTP/POP3/IMAP, TLS certificates; with MD5/SHA1/SHA256 |
| Images | thumbnails of extracted images |
| Messages | email and chat messages reconstructed |
| Credentials | cleartext logins and hashes (HTTP basic/forms, FTP, SMTP AUTH, NTLM challenge-response, Kerberos) |
| Sessions | TCP sessions with start time and client/server |
| DNS | queries and answers with timestamps |
| Parameters | HTTP GET/POST parameters, cookies, form fields |
| Keywords / Anomalies | keyword search across frames; parsing anomalies |
Extracted files go to `AssembledFiles/<ip>/<protocol - port>/` under the install directory.

## Workflow
1. Hosts tab: identify internal victims and external peers; sort by bytes or sessions.
2. Files tab: sort by extension; hash executables, archives and documents; check against threat
   intel; open carved TLS certificates (subject/issuer of C2).
3. Credentials tab: compromised accounts in cleartext protocols; NTLM hashes show which user
   authenticated where.
4. Export (File > Export to CSV/JSON) for the case record.

## Gotchas
- Extracted malware lands on your disk: run in an isolated analysis VM with AV exclusions and
  never double-click extracted files.
- Encrypted traffic yields only metadata and certificates; decrypt first (key log) and feed the
  decrypted pcap if possible.
- Large captures (> a few GB) are slow in the free edition; split with `editcap -c`.

## Self-check
Every artefact you cite (file, credential, host fingerprint) has its source frame/session and
hash recorded, and was cross-checked in Wireshark.
