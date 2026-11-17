---
id: computing-software.cybersecurity-defensive.zeek.analyzer-log-dpd
name: analyzer-log-dpd
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, analyzer-log, dynamic-protocol-detection, dpd, protocol-violation]
level: advanced
status: docs-checked
description: "Dynamic protocol detection in Zeek: signature-driven analyzer activation, analyzer.log mismatch reports, and a TLS-looking HTTP example."
sources: ["https://docs.zeek.org/en/current/reference/logs/analyzer.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# analyzer.log and dynamic protocol detection

Zeek uses signatures matching typical protocol dialogues to find the right analyzer from the payload. When one matches, it turns on the analyzer to confirm. Zeek can turn analyzers off when it becomes obvious they are parsing the wrong protocol. This allows loose signatures and trying several analyzers in parallel.

`analyzer.log` reports problems with this mechanism. Fields are in `Analyzer::Logging::Info`. The page says the log was revamped in Zeek 8.0 and resembles what `dpd.log` provided in older versions, and points to the 8.0 release notes.

The worked example: tcpdump shows a short session to TCP port 443 with a normal handshake, a 517-byte client payload and a 467-byte server reply, then FINs. It looks unremarkable. tshark decodes the client payload as a TLSv1 Client Hello, but the server reply as `HTTP/1.1 400 Bad Request (text/html)`. A TLS analyzer expecting a TLS server response sees HTTP instead, so a protocol violation is logged in `analyzer.log`.

Practice: when a service on a standard port behaves oddly, correlate `analyzer.log` with `conn.log` through the `uid`, and compare against a packet decode.

## Checked

2026-11-08. Read the DPD and analyzer.log page in full; every claim confirmed.

Method: documentation only; no commands were run.
