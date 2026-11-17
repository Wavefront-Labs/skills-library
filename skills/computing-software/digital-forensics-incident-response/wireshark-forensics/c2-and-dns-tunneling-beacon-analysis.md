---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.c2-and-dns-tunneling-beacon-analysis
name: c2-and-dns-tunneling-beacon-analysis
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [c2-beaconing, cobalt-strike, malleable-c2, jitter, dns-tunneling, icmp-tunneling, dnscat2, tshark, rita, beacon-interval-analysis, domain-fronting, exfiltration, covert-channel, dfir, network-forensics]
level: advanced
status: draft
description: "Find C2 beaconing intervals/jitter, Cobalt Strike malleable-profile traffic shaping, and DNS/ICMP tunneling in a pcap using tshark statistics and interval analysis."
sources: ["https://www.cobaltstrike.com/help-malleable-c2", "https://github.com/activecm/rita"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# C2 and DNS-tunneling beacon analysis

**Goal:** the baseline pcap-triage skill
(computing-software.digital-forensics-incident-response.wireshark-forensics.pcap-triage-and-session-reconstruction)
already flags "beaconing" as a thing to look for in conversation statistics; this
skill is the actual method for proving a beacon, and covers covert channels (DNS/
ICMP tunneling) that don't show up as a normal "connection" at all.

## 1. Proving beaconing, not just suspecting it
A beacon is periodic outbound traffic to the same destination at a roughly fixed
interval, often with deliberately randomized ("jittered") timing to defeat naive
fixed-interval detection.
```
tshark -r capture.pcapng -Y "ip.dst==<suspect_ip>" -T fields -e frame.time_epoch > times.txt
```
Diff consecutive timestamps. A tight, mostly-consistent delta (e.g. 58-62 seconds
every time) with low variance is a classic unjittered beacon. A delta that varies
within a bounded percentage of a base interval (e.g. 60s ± 20%) is jittered beaconing
— the variance *pattern itself* (bounded randomness around a fixed base, rather than
truly random intervals) is the tell, not the raw variance number alone. Tools like
**RITA** (Real Intelligence Threat Analytics, open-source) automate this beacon-score
calculation across an entire pcap/Zeek-log dataset rather than one connection at a
time — worth reaching for once manual delta-diffing on a suspect connection confirms
the technique and you need to sweep for others.

## 2. Cobalt Strike malleable C2 profiles
Cobalt Strike (and its cracked/leaked variants used by many non-authorized actors) use
**malleable C2 profiles** to shape HTTP/HTTPS/DNS traffic to look like legitimate
services (mimicking a CDN, a specific SaaS API, or jQuery CDN headers) specifically to
blend into normal traffic and defeat simple signature matching. Recognizing it in a
pcap:
- URI paths, User-Agent strings and header ordering that closely mimic a known
  legitimate service but with subtle inconsistencies (a User-Agent claiming a browser
  version inconsistent with other headers, or a URI pattern that's superficially
  plausible but doesn't match that real service's actual API structure).
- **Timing and size consistency across requests that claim to be organic browsing**
  — real browsing traffic is irregular in size and timing; beaconing traffic dressed
  up as browsing is often suspiciously regular underneath the disguise, which is
  exactly what the beacon-interval analysis above surfaces regardless of how well the
  HTTP layer is disguised.
- Published malleable-profile detection signatures (community-maintained Snort/Sigma/
  YARA rules keyed to known profile artifacts — default Cobalt Strike profile tells,
  specific cookie names, specific URI patterns from leaked profiles) are worth
  checking against, but are a moving target since profiles are fully customizable;
  don't rely on signature match alone to rule a connection in or out.

## 3. DNS tunneling
A covert channel encoded entirely in DNS queries/responses — no "connection" to spot
in conversation statistics because each query is independent and often to a
legitimate-seeming resolver chain:
- **Volume and query-name entropy** are the primary tells: an unusually high rate of
  queries to one domain/subdomain structure, with subdomain labels that look
  high-entropy/base32-like (`x7f3kq9z.tunnel.example.com`) rather than
  human-readable, especially paired with unusual record types (TXT/NULL records
  carry more payload per query than A records, and legitimate traffic rarely uses
  them at volume).
- `tshark -r capture.pcapng -Y "dns" -T fields -e dns.qry.name` then look for
  subdomain length/entropy outliers and repetition patterns (sequential-looking
  encoded chunks under the same parent domain) rather than scanning visually query by
  query — tools like `dnscat2`'s own traffic pattern is well-documented and worth
  comparing against if a specific tool is suspected.

## 4. ICMP tunneling
Similarly covert-channel-shaped: ICMP Echo Request/Reply packets carrying payload
data in the (normally fixed-pattern) data field. Legitimate ping traffic has a
predictable, often all-same-byte or incrementing payload; tunneled traffic shows
variable, high-entropy payload content of varying length across supposedly similar
Echo packets — `tshark -Y "icmp" -T fields -e data.data` and inspect payload
consistency across the capture.

## Verify
- Confirm a beacon claim with the interval-delta method above, not visual impression
  of "a lot of traffic to one place" — state the measured interval and jitter bound.
- For a suspected malleable-profile match, cite the specific inconsistency found
  (header mismatch, URI structure anomaly), not just "looks like Cobalt Strike."
- For DNS/ICMP tunneling claims, show the entropy/volume anomaly measured, not just
  "unusual-looking" query names — a borderline case needs the actual metric.

Unconfirmed: specific malleable-profile signatures and known-tool traffic patterns
change constantly as profiles/tools are updated — verify against current community
detection-rule repositories rather than a fixed signature list.
