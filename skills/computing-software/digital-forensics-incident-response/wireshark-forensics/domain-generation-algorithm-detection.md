---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.domain-generation-algorithm-detection
name: domain-generation-algorithm-detection
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [dga, dns-forensics, c2-beaconing, malware-network-behaviour, dfir]
level: advanced
status: draft
description: "Detect DGA-driven malware in DNS data: NXDOMAIN bursts, entropy and n-gram scoring, query timing, known-family seeds, and confirming the infected host."
sources: ["https://attack.mitre.org/techniques/T1568/002/", "https://github.com/baderj/domain_generation_algorithms", "https://dgarchive.caad.fkie.fraunhofer.de/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Domain generation algorithm detection

**Goal:** DGA malware (ATT&CK T1568.002) generates hundreds of pseudo-random domains per day and
tries them until one resolves. The failures are loud in DNS logs.

## Signals
- **NXDOMAIN bursts** from one client: dozens to thousands of non-existent domains in minutes.
- **Lexical features**: high character entropy, low proportion of dictionary words, unusual consonant runs,
  long labels, numeric mixes; uncommon TLDs per family. Wordlist DGAs (Suppobox, Matsnu) evade entropy - use n-gram/word models.
- **Timing**: queries batched at fixed intervals or at the start of each period (daily seeds).
- **Successful resolutions** among the noise: the few domains that resolve are the C2 - highest priority.

## Hunting queries
```text
Zeek dns.log: rcode_name == "NXDOMAIN" grouped by id.orig_h, count per 10 min, distinct query count
Splunk: index=dns rcode=NXDOMAIN | bucket _time span=10m | stats dc(query) as uniq by src, _time | where uniq > 50
```
- Score domains with an entropy/n-gram function or a trained model (e.g. `dga_detection` libraries) and review the top.
- Exclude known noisy sources: Chrome's random intranet redirect probes (10-char random single-label lookups at startup), antivirus/CDN random subdomains, DNS-based telemetry (`*.mcafee.com`-style).

## Confirm
- Map the client IP to a host (DHCP logs), then find the process (EDR DNS events, Sysmon 22).
- Match domains to known families: DGArchive (registration needed) or reimplemented DGAs (baderj repository) to identify the family and predict future domains for blocking/sinkholing.

## Gotchas
- DNS forwarders hide original clients; collect logs at the first-hop resolver or use Sysmon 22 on hosts.
- Encrypted DNS bypasses these logs entirely.

## Verify
The infected host and process are identified, and the resolving DGA domains are blocked and fed to scoping.
