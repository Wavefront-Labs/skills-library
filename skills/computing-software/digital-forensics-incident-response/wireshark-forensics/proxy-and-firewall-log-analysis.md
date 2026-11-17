---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.proxy-and-firewall-log-analysis
name: proxy-and-firewall-log-analysis
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [proxy-logs, firewall-logs, web-proxy, squid, palo-alto, egress-analysis, beaconing, dfir]
level: practitioner
status: draft
description: "Investigate egress with proxy and firewall logs when no pcap exists: fields that matter, beacon and exfil detection, user attribution and log pitfalls."
sources: ["https://wiki.squid-cache.org/Features/LogFormat", "https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/monitoring/use-syslog-for-monitoring/syslog-field-descriptions", "https://www.sans.org/white-papers/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Proxy and firewall log analysis

**Goal:** reconstruct network activity of compromised hosts from logs, which cover far more
time than any packet capture.

## What each source gives you
| Source | Key fields |
|---|---|
| Web proxy (Squid, Zscaler, Bluecoat/Symantec, Netskope) | time, client IP, **authenticated user**, method, full URL, status, bytes in/out, user-agent, category, action |
| Next-gen firewall traffic (Palo Alto, Fortinet, Check Point) | 5-tuple, NAT translations, application ID, bytes, session duration, rule, action |
| NGFW threat/URL logs | URL/SNI, threat signatures, file names and hashes |
| Host firewall (Windows 5156/5157, `pfirewall.log`) | per-host connections, process (5156 includes application path) |
Squid native format: `time elapsed client action/code bytes method URL user hierarchy/peer type`.

## Analyses
- **Beaconing:** same client -> same destination at regular intervals. Group by client+domain,
  compute inter-arrival times, flag low standard deviation and long duration; tolerate jitter
  (C2 frameworks add 10-50%).
- **Exfiltration:** sum bytes out per client/destination per hour; big POST/PUT or upload to
  file-sharing categories (mega.nz, transfer.sh, temp.sh, file.io, rclone to cloud storage);
  large outbound on non-web ports in firewall logs.
- **Rare destinations:** domains contacted by one or two hosts only (long tail), newly
  registered domains, direct-to-IP HTTP requests, odd user-agents (`curl`, `python-requests`,
  `Go-http-client`, empty, spoofed old browsers).
- **Blocked attempts:** denied requests reveal malware trying C2 even when egress worked
  elsewhere.
- **User attribution:** proxy auth user, or firewall User-ID; otherwise map IP via DHCP.

## Pitfalls
- HTTPS without TLS inspection: proxy logs only `CONNECT host:443` with total bytes, no path.
- NAT: firewall external IP maps to many internal hosts; use pre-NAT source fields.
- Time zones and clock drift: proxies often log local time; normalise to UTC.
- Sampling/summarisation in cloud proxies and flow logs; retention may be short.
- Bytes are often from the proxy's perspective (client->proxy vs proxy->server); know which.

## Example (Squid access.log)
```bash
awk '{print $3, $7}' access.log | sort | uniq -c | sort -rn | head        # client/URL pairs
awk '$6=="POST"{s[$3" "$7]+=$5} END{for(k in s) print s[k],k}' access.log | sort -rn | head
```

## Self-check
For each suspicious flow you report the client (and user), destination, first/last seen,
total bytes each way, and whether content visibility existed.
