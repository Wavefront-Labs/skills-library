---
id: computing-software.cybersecurity-defensive.zeek.dns-log-analysis
name: dns-log-analysis
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, dns-log, dns-queries, auth-addl, dns-tunnelling]
level: practitioner
status: docs-checked
description: "Interpret Zeek dns.log entries: query, qtype_name, rcode_name, answers and TTLs, unanswered queries, DoH and DoT blind spots, and the policy/protocols/dns/auth-addl.zeek script."
sources: ["https://docs.zeek.org/en/current/reference/logs/dns.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# dns.log analysis

`dns.log` captures application-level name resolution, assuming traffic is not encrypted as with DNS over HTTPS or TLS. Field details are in `DNS::Info`.

Analysts mainly ask: who is asking, what is the question, who answered, and how. Fields include `trans_id`, `rtt`, `query`, `qclass_name`, `qtype_name`, `rcode_name` (for example `NOERROR`), and the flags `AA` and `TC`, plus the answers and their TTLs.

A response entry for an A record of `zeek.org` lists the answer addresses; a query entry for AAAA with no answer shows no answers. Query and response records share the same `uid`.

Security context: intruders use DNS to resolve names like everyone else, but may subvert it for command-and-control, obfuscated or encrypted payloads, or other unwanted functions, because administrators tend to allow DNS everywhere.

To add authority and additional records to entries, load the policy script:

```
zeek -C LogAscii::use_json=T protocols/dns/auth-addl.zeek -r capture.pcap
```

Before this, an unanswered query shows little; with it, the log carries more detail on the first entry.

Pivot from a `uid` into `conn.log` to see volume and timing for the same flow.

## Checked

2026-11-04: read against the official Zeek documentation page(s) listed in sources; the claims, names, values and examples in this skill match the page text. Nothing else was added.

Method: documentation only; no commands were run.
