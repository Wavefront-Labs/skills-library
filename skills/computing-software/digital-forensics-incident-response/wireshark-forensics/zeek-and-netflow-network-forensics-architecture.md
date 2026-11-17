---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.zeek-and-netflow-network-forensics-architecture
name: zeek-and-netflow-network-forensics-architecture
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [zeek, bro, netflow, sflow, arkime, moloch, full-packet-capture, conn-log, pcap-retention, network-forensics-architecture, retrospective-analysis, security-onion, span-port, tap, dfir]
level: advanced
status: docs-checked
description: "Design a network-forensics architecture (Zeek logs, NetFlow, full packet capture) that makes retrospective analysis possible when no pcap was captured at the time of the incident."
sources: ["https://zeek.org/", "https://arkime.com/", "https://github.com/arkime/arkime", "https://docs.securityonion.net/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Zeek and NetFlow network forensics architecture

**Goal:** the baseline pcap-triage skill
(computing-software.digital-forensics-incident-response.wireshark-forensics.pcap-triage-and-session-reconstruction)
assumes you already have a capture. Most incidents don't — nobody was capturing full
packets at the border six weeks ago when the intrusion actually started. This skill
is about what to build *before* the next incident so that assumption holds, and what
you can still get when it doesn't.

## 1. The retention economics problem — why this isn't "just capture everything"
Full packet capture at any meaningful network speed generates enormous storage volume
very fast; retaining weeks of full PCAP at a typical enterprise egress point is often
impractical on storage cost alone. The practical architecture layers three different
levels of detail against three different retention horizons:
- **NetFlow/sFlow/IPFIX** — connection metadata (five-tuple, byte/packet counts,
  duration) with minimal storage footprint, retained for months, answers "did host A
  talk to host B, how much, when" even with zero payload visibility. Cheapest, holds
  longest, least detail.
- **Zeek logs** (`conn.log`, `dns.log`, `http.log`, `ssl.log`, `files.log`, etc.) —
  protocol-aware metadata extraction without storing the payload itself: full HTTP
  request/response headers, TLS server names and certificate details (JA3 needs an extra package), DNS query/response
  pairs, extracted-file hashes — carries far more protocol detail than NetFlow because it is already parsed to the
  protocol level. This is the sweet spot most organizations should retain for 30-90+ days at
  minimum.
- **Full packet capture** — retained for a short rolling window (hours to a few days,
  storage-permitting) at high-value chokepoints, because this is the only tier that
  lets you actually extract file content, decrypt (if keys are available, see
  computing-software.digital-forensics-incident-response.wireshark-forensics.tls-decryption-and-certificate-forensics),
  or re-derive anything Zeek's protocol parsers didn't specifically extract.

## 2. Working from Zeek logs when there's no pcap
When an incident is discovered after the full-PCAP retention window has rolled over
but Zeek logs survive, the investigation runs **log-first**: `conn.log` for
who-talked-to-whom-when (feeds the same beacon-interval analysis as
computing-software.digital-forensics-incident-response.wireshark-forensics.c2-and-dns-tunneling-beacon-analysis,
just from structured logs instead of raw packets), `dns.log` for every resolution
(including to domains later found malicious — a DNS log entry weeks old can be the
only surviving proof a host ever resolved a C2 domain), `ssl.log`/`x509.log` for server names and
certificate details without needing the packets at all, `files.log` for file hashes
(when a hash analyzer such as `frameworks/files/hash-all-files` was loaded) computed from HTTP/SMB/FTP transfers in-stream at capture time — meaning file-level
IOC matching against a hash list is possible retroactively even without the original
payload bytes surviving.

## 3. Arkime/Moloch as the middle ground
Arkime stores network traffic in standard PCAP format and indexes session metadata in
OpenSearch or Elasticsearch, with a web interface to browse, search and export PCAP. Per
its documentation, PCAP retention depends on the sensor disk space and metadata retention
on the search cluster scale, so both can be sized independently, at the cost of running
and maintaining the stack. Worth considering specifically where retrospective full-payload access (not
just metadata) needs to survive longer than storage economics otherwise allow.

## 4. Deployment architecture basics
A SPAN port or network TAP feeding a dedicated sensor (Zeek, Arkime, or an all-in-one
distribution such as Security Onion, whose documentation covers Zeek, Suricata and Stenographer packet capture) at each network chokepoint
that matters — internet egress at minimum, internal segmentation boundaries where
lateral movement would need to be visible. A sensor seeing only a subset of traffic
(e.g. only north-south, missing east-west internal traffic) creates a blind spot that
won't be obvious until an investigation specifically needs the traffic that wasn't
visible — document sensor placement and coverage explicitly as part of the
architecture, not just "we have a sensor."

## Verify
- Confirm actual retention windows (not just configured intent) for each tier by
  checking the oldest available log/pcap timestamp on the live system, not the
  configuration file's stated retention value — storage pressure silently shortens
  retention in practice more often than configuration is actually changed.
- Confirm sensor placement covers the segments relevant to the current incident
  before concluding "no network evidence exists" — it may exist, just not at the
  monitored chokepoint.
- When working from Zeek logs without pcap, explicitly note in the report that
  conclusions are drawn from parsed metadata, not raw payload, where that distinction
  matters (e.g. a file hash from `files.log` vs an examined file from a surviving
  pcap).

Unconfirmed: specific storage sizing figures for full-PCAP vs Zeek vs NetFlow depend
heavily on actual traffic mix and link speed at a given site — size any real
deployment against measured traffic volume, not a generic industry rule of thumb.

## Checked

Checked 2026-10-25 against the Arkime README (arkime/arkime, last pushed 2026-10-24: PCAP in standard format, metadata in OpenSearch/Elasticsearch, retention depends on disk and cluster scale), the Security Onion 2.4 documentation tree (pages for Zeek, Suricata and Stenographer) and the Zeek scripts (Zeek sources (zeek/zeek master, last pushed 2026-10-23: doc/frameworks, tools/zeek-cut, base and policy scripts, event definitions)) for the log contents. Corrected: JA3 is not in the base ssl.log and hashes in files.log require a hash analyzer; Arkime is described from its README instead of the unconfirmed "Zeek-log speed" and former-name remarks; Security Onion is no longer said to bundle Arkime. The storage sizing remark was already marked unconfirmed and stays that way; no figures are stated as fact.

Method: documentation only; no commands were run.
