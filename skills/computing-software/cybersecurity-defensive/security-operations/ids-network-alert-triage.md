---
id: computing-software.cybersecurity-defensive.security-operations.ids-network-alert-triage
name: ids-network-alert-triage
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [network-alert-triage, alert-triage, suricata, snort, zeek, ids, ndr, pcap-analysis, soc]
level: practitioner
status: docs-checked
description: "Triage IDS/IPS and NDR network alerts (Suricata, Snort, Zeek): read the signature, inspect the packet/PCAP, check direction and response, and correlate with host data."
sources: ["https://docs.suricata.io/en/latest/rules/intro.html", "https://docs.suricata.io/en/latest/output/eve/eve-json-format.html", "https://docs.zeek.org/en/master/logs/index.html", "https://docs.zeek.org/en/master/logs/conn.html", "https://docs.zeek.org/en/master/logs/files.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# IDS and network alert triage

## Read the signature
- Open the rule (`sid`): what content matches, direction (for example `$HOME_NET -> $EXTERNAL_NET`), flow
  (for example `flow:established,to_server`), `classtype`, and references. Rule metadata can carry fields such as
  `signature_severity`, which Suricata includes under `alert.metadata` in EVE output.
- Policy-style rules indicate behaviour (remote admin tools, anonymisers), not necessarily attacks.

## Direction and outcome
- Inbound exploit attempt (scanner hitting a CVE signature): did the target run the vulnerable
  software? Did it respond (HTTP 200 vs 404, payload size)? Most are noise from internet scanning.
- Outbound C2/malware signatures from an internal host: high priority; the host initiated traffic.
- Check `app_proto` and the protocol fields in the alert record (HTTP host, URI, user agent; TLS details).

## Inspect the evidence
- Suricata EVE JSON: the alert record carries `app_proto` and a `flow` object (including `bytes_toserver`); the
  `flow_id` joins an alert to the flow and protocol records (HTTP, DNS, TLS) of the same flow.
- Pull the PCAP for the flow from your full-packet capture and follow the stream; confirm the match is not a
  coincidence in benign content.
- Zeek: `conn.log` (duration, bytes, `conn_state`), `http.log`, `dns.log`, `ssl.log`, `files.log` (file hashes).

## Correlate
- Host: EDR or Sysmon network-connection telemetry (Sysmon event ID 3) for the process making the connection, and its parent.
- Reputation of destination (passive DNS, age of domain, hosting ASN).
- Other hosts talking to the same destination.

## Verdicts
- True positive needing response: outbound C2 confirmed by process; successful exploit (response
  shows execution, follow-on connections).
- Benign true positive: policy rule matched sanctioned tool; tune with suppression by host.
- False positive: content match in benign traffic; threshold or modify rule locally (keep sid notes).

## Gotchas
- Encrypted traffic hides payload; rely on TLS metadata, certificates and host telemetry.

## Verify
Case records signature logic, direction, evidence (PCAP excerpt or EVE record), host correlation and verdict.

## Checked
Checked 2026-11-08 against the Suricata rules introduction (rule header, `flow:established,to_server`, `classtype`,
`sid`), the Suricata EVE JSON format page (`flow_id`, `app_proto`, `flow` bytes, alert metadata such as
`signature_severity`) and the Zeek conn.log, files.log and common-logs pages. Removed as not confirmed: ET
confidence and deployment metadata, `payload_printable`, JA3/JA4 and SNI field names, ET POLICY and TOR
examples, Arkime, Security Onion, tcpflow, `DeviceNetworkEvents`, and the SANS white papers source (index page only).
Method: documentation only; no commands were run.
