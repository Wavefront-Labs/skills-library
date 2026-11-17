---
id: computing-software.networking-hardware-and-wireless.powerdns.pipe-backend-protocol
name: pipe-backend-protocol
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, pipe-backend, pipe-command, pipe-abi-version, co-process, helo]
level: advanced
status: docs-checked
description: "Implement a PowerDNS pipe backend co-process: pipe settings, HELO handshake, Q and AXFR questions, DATA, END, FAIL and LOG answers."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/backends/pipe.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pipe backend protocol

Settings: `pipe-command` (mandatory; a command, or a Unix socket that is already listening), `pipe-abi-version` (default 1, values 1 to 5), `pipe-timeout` (default 2000 ms; on expiry the process is declared dead and respawned), `pipe-regex` (only matching questions are sent; root is `^\.$`). Launch name `pipe`. No DNSSEC, DNS update, zone caching or views.

Handshake: PowerDNS sends `HELO<TAB>N`; reply `OK<TAB>banner`, or `FAIL` (and keep running) if N is unsupported.

Questions, tab separated, newline terminated:
- ABI 1: `Q qname qclass qtype id remote-ip`
- ABI 2 adds `local-ip`; ABI 3+ adds `edns-subnet-address`.
- `AXFR id` (ABI 4+ adds `zone-name`).
- ABI 5 allows `CMD ...` direct commands, answered with lines then `END`.

Answers:
- `DATA qname qclass qtype ttl id content` (ABI 1, 2)
- `DATA scopebits auth qname qclass qtype ttl id content` (ABI 3+)
- `END` (also means no data), `FAIL`, and `LOG message` (only between a question and `END`).

Rules:
- Answer literally; the question may differ from the client's (an AAAA can arrive as ANY). A wildcard name returns data only if that exact name exists.
- For ABI 1 and 2, scopebits is 0 and auth 1. For ABI 3+, auth is 0 for delegation NS and glue, 1 for the zone's own SOA and NS.
- Enable `edns-subnet-processing` for ABI 3+ to get real subnets.
- Raise `distributor-threads` for latency-bound pipes.
- IPv6 addresses may carry a `%interface` suffix.

## Checked

2026-11-08. Read docs/backends/pipe.rst in full. Confirmed the feature table (no DNSSEC, DNS update, zone caching or views), pipe-command, pipe-abi-version default 1, pipe-timeout default 2000, pipe-regex and the root pattern, the HELO and OK handshake, question formats per ABI version, answer formats, auth and scopebits defaults, CMD in ABI 5, distributor-threads, wildcard and IPv6 notes. Description shortened. Nothing removed.

Method: documentation only; no commands were run.
