---
id: computing-software.cybersecurity-defensive.security-operations.dns-hunting-dga-and-tunnelling
name: dns-hunting-dga-and-tunnelling
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [dns-hunting, threat-hunting, dga, dns-tunnelling, zeek, sysmon-dns-events, c2-detection]
level: practitioner
status: docs-checked
description: "Hunt DNS telemetry for DGA domains, DNS tunnelling and C2 using MITRE ATT&CK T1568.002 and T1071.004 detection guidance and Zeek DNS log fields; set thresholds from your baseline."
sources: ["https://attack.mitre.org/techniques/T1071/004/", "https://attack.mitre.org/techniques/T1568/002/", "https://docs.zeek.org/en/master/scripts/base/protocols/dns/main.zeek.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# DNS hunting for DGA and tunnelling

## Data
Resolver query logs, Zeek DNS logging, Sysmon DNS events (named in the ATT&CK detection
text for T1568.002), EDR DNS events and protective DNS logs. Process attribution matters: ATT&CK's
T1071.004 analytics look for DNS queries from non-browser, non-system processes (for example PowerShell,
rundll32, python.exe).

Zeek's DNS script logs the `DNS::Info` record. Useful columns: `query`, `qtype_name`,
`rcode_name`, `answers`, `TTLs`, `rejected`, `rtt`, `trans_id`.

## DGA (T1568.002, Dynamic Resolution: Domain Generation Algorithms)
Adversaries use a DGA to pick a C2 destination dynamically, so there can be thousands of
candidate domains; DGAs are also used for Fallback Channels when the primary C2 is lost. ATT&CK
detection strategy DET0419 suggests:
- correlate DNS queries with high-entropy or gibberish patterns with short-lived connections
  from unusual processes, and monitor Sysmon DNS events and Windows Security logs for
  abnormal query rates and failed lookups;
- identify processes issuing repeated DNS queries to random-looking domains with abnormal
  entropy or word concatenations (some DGAs concatenate words from lists), and correlate with
  resolver logs showing high NXDOMAIN rates;
- on ESXi, high-frequency, low-TTL or unresolvable domains.
A local DNS sinkhole is listed as a mitigation. ATT&CK gives no numeric thresholds: set
NXDOMAIN-per-host and entropy cut-offs from your own baseline.

## Tunnelling (T1071.004, Application Layer Protocol: DNS)
Commands and results are embedded in DNS traffic; records named include TXT and A (and A, OPT
and TXT for FIN7, AAAA for DanBot). DNS beacons are hard to detect because they communicate infrequently.
ATT&CK analytic AN1124 detects clients issuing queries with high volume, long subdomain lengths,
encoded payload patterns, or to known malicious infrastructure; AN1122 covers daemons or
scripts generating long or frequent subdomains from tools like iodine and dnscat2; AN1123 covers
scripting environments performing queries with encoded subdomains. Cobalt Strike can encapsulate
its C2 protocol in DNS.
Hunt by grouping by client and parent domain and ranking unique subdomain count, name length,
record type mix (TXT in volume) and rate; pick thresholds from your baseline.

## Newly observed domains
Join queries to first-seen history (passive DNS or your own); review rarely contacted new domains.
This is analyst practice, not an ATT&CK statement.

## Verify
Hunt report lists hosts, process (if attributable), domains and verdicts; confirmed patterns
become detections with thresholds tuned on your baseline.

## Checked
Date: 2026-11-07. Read: ATT&CK T1071.004 (description, procedure examples scanned for the cited examples, Detection Strategy DET0400 with AN1121-AN1125), T1568.002 (description, mitigations, DET0419 with AN1178, AN1179, AN1181) and the Zeek `base/protocols/dns/main.zeek` script page (DNS::Info fields, options). Removed as not on the pages: the Splunk SPL with `ut_shannon`, the `DnsEvents` KQL and its table name, all numeric thresholds (50 NXDOMAIN, 50-character names, 500 unique, 40 average, 30-day age), the vowel-ratio and rare-TLD heuristics, resolver products (Infoblox, BIND), the `dns.log` file name, the Sysmon "EID 22" number, DNSExfiltrator, benign-lookalike examples (`*.cloudapp.net`, DNSBL) and the Splunk DGA app/freq.py. The long procedure-example tables were skimmed, not read line by line.
Method: documentation only; no commands were run.
