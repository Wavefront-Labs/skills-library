---
id: computing-software.cybersecurity-defensive.zeek.weird-and-notice-logs
name: weird-and-notice-logs
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, weird-log, notice-log, protocol-anomalies, alerts]
level: practitioner
status: docs-checked
description: "Distinguish weird.log protocol anomalies from notice.log script-raised alerts, count weird names, and treat notices as the closest thing to IDS alerts in Zeek."
sources: ["https://docs.zeek.org/en/current/reference/logs/weird-and-notice.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# weird and notice logs

**weird.log** holds unusual or unexpected activity flagged by protocol analyzers, mostly hard-coded by whoever wrote the analyzer, occasionally by scripts. Fields: `Weird::Info`. Weirds can often be ignored because of volume.

A 24-hour count on a home network (name and flag) looked like:

```
553 ["window_recision",false]
129 ["unknown_protocol",false]
128 ["non_ip_packet_in_ethernet",false]
 21 ["bad_HTTP_request",false]
```

Other names seen include `truncated_IP`, `SYN_after_close`, `data_after_reset`, `bad_TCP_header_len` and `DNS_RR_unknown_type`. The page points to Fatema Bannat Wala's writing, such as What Is Weird in Zeek, as the best reference.

**notice.log** records situations explicitly detected and reported by Zeek scripts (or packages) as worth inspecting. They are usually semantic, such as a self-signed certificate, rather than protocol errors. Fields: `Notice::Info`. Notices are much more interesting than weirds: they are the closest Zeek comes to IDS alerts. Document coverage of notice.log is thinner than for other logs.

Triage: count weird names first to find noisy analyzers, then review notices; use `uid` to pivot into `conn.log`.

## Checked

2026-11-04: read against the official Zeek documentation page(s) listed in sources; the claims, names, values and examples in this skill match the page text. Nothing else was added.

Method: documentation only; no commands were run.
