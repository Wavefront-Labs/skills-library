---
id: computing-software.systems-network-administration.wireshark.dns-response-time-and-error-analysis
name: dns-response-time-and-error-analysis
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, dns-analysis, dns-time, dns, nxdomain, servfail, dns-retransmission, dns-response-time, dns-statistics]
level: practitioner
status: verified
description: "Measure DNS performance and failures from a capture: dns.time, unanswered queries, rcode breakdown, retries, truncation to TCP, and slow upstream resolvers."
sources:
  - https://www.wireshark.org/docs/dfref/d/dns.html
  - https://www.rfc-editor.org/rfc/rfc1035
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# DNS response time and errors

## Filters
```
dns.flags.response == 1 && dns.time > 0.2      # slow answers (dns.time = query->response)
dns.flags.response == 0 && !dns.response_in    # unanswered queries (tshark needs `-2 -Y`; `-2 -R` and one pass match every query)
dns.flags.rcode == 3                           # NXDOMAIN
dns.flags.rcode == 2                           # SERVFAIL (upstream/DNSSEC failure)
dns.flags.rcode == 5                           # REFUSED (ACL, recursion off)
dns.retransmission                             # same query id re-sent
dns.flags.truncated == 1                       # TC bit: client should retry over TCP 53
```

Run on a synthetic capture (fast, slow 0.35 s, NXDOMAIN, SERVFAIL, REFUSED, a retried query, a TC=1 answer and an
unanswered query): each filter matched exactly the intended frames; with `-2 -Y` the unanswered filter listed the
unanswered query and the retransmitted duplicate of the retried query (so subtract retransmissions).

## Measure
- Add `dns.time` as a column; sort descending.
- Statistics > DNS (or `tshark -q -z dns,tree`) gives rcode counts (No error / Server failure / Refused / No such name in the test), query
  types and payload-size stats.
- I/O graph with `AVG(dns.time)dns.time` over time shows when resolution degraded.
- `tshark -r cap.pcapng -Y "dns.flags.response==1" -T fields -e ip.src -e dns.time | sort -k2 -rn | head` ranks resolvers.

## Read the patterns
- Client waits one resolver timeout (OS and configuration specific) then re-asks, possibly another server =
  primary resolver timing out; `dns.time` on the late answer in the test showed 1.03 s.
- Many NXDOMAIN for `name.corp.local.corp.local` = search suffix expansion (ndots); fine
  unless it is slow.
- AAAA queries slow/unanswered while A is fine = broken IPv6 handling in a middlebox/resolver.
- SERVFAIL only for signed zones = DNSSEC validation failure upstream.
- TC=1 followed by no TCP 53 = firewall blocking DNS over TCP.

## Capture point
On a resolver capture both sides: client query arrival and upstream query/answer split
"resolver slow" from "upstream slow".

## Verify
- [ ] Slow or failing names, the responding server and the rcode identified with timings.
