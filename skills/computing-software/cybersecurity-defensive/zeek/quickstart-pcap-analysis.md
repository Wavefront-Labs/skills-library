---
id: computing-software.cybersecurity-defensive.zeek.quickstart-pcap-analysis
name: quickstart-pcap-analysis
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, pcap-analysis, read-pcap, uid-pivot, json-logs]
level: intro
status: docs-checked
description: "Run zeek -r on a pcap, switch logs to JSON with LogAscii::use_json=T, and pivot between conn.log, http.log and weird.log using the uid field."
sources: ["https://docs.zeek.org/en/current/quickstart.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# quickstart pcap analysis

Run Zeek on a capture in a clean directory:

```
zeek -r quickstart.pcap LogAscii::use_json=T
```

Zeek prints nothing but writes logs to the current directory: `conn.log` (one record per connection), `http.log`, and `weird.log` for unusual behaviour such as an invalid HTTP method.

Pivot between logs with the `uid` field, the unique connection identifier. A uid found in `conn.log` appears in `http.log`, and a weird such as `unknown_HTTP_method` carries the same uid in `weird.log`.

Without `LogAscii::use_json=T` the logs are tab-separated (TSV). The option can be appended to any zeek invocation.

To extend behaviour, run a script alongside the pcap:

```
zeek example.zeek -r quickstart.pcap
```

where the script defines event handlers such as `event http_request(...)`. Custom scripts can also run on live traffic.

## Checked

2026-11-08. Read the Quick Start Guide in full; every claim confirmed.

Method: documentation only; no commands were run.
