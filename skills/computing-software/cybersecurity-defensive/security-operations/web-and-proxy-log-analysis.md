---
id: computing-software.cybersecurity-defensive.security-operations.web-and-proxy-log-analysis
name: web-and-proxy-log-analysis
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [log-analysis, web-log-analysis, proxy-log-analysis, access-log, web-shell-detection, combined-log-format, user-agent-analysis, http-status-codes]
level: practitioner
status: draft
description: "Analyse web server and proxy logs to find web shells, scanning, exploitation attempts and suspicious outbound browsing, with field meanings and queries."
sources: ["NIST SP 800-92", "Apache httpd Log Files documentation", "NSA/ASD Detect and Prevent Web Shell Malware (CSI)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Web server and proxy log analysis

**Goal:** turn access logs into answers: was the site exploited, is there a web shell, and
which internal users or hosts reached something malicious.

## Web server access logs
Combined log format: `client ident user [time] "METHOD path HTTP/x" status bytes "referer" "user-agent"`.
IIS W3C logs list fields in the `#Fields:` header (`cs-uri-stem`, `cs-uri-query`, `sc-status`, `time-taken`).

### Web shell indicators (NSA/ASD guidance)
- Requests to files that are rarely requested and only by one or two client IPs:
```
awk '{print $7}' access.log | cut -d'?' -f1 | sort | uniq -c | sort -n | head -50
```
- POST requests to static-looking or upload-directory paths (`/uploads/x.php`, `.aspx` in image dirs).
- Successful (200) responses to new file names right after an upload or exploit attempt.
- Unusual user agents or none at all, and request sizes that vary widely on one URL.

### Exploitation and scanning
- Bursts of 404s from one IP: content discovery scanning.
- Encoded traversal and injection strings in URIs/queries (`../`, `%2e%2e`, `UNION SELECT`, `${jndi:`).
- Match the exploit window: first successful request to the vulnerable endpoint, then follow that client IP.

## Proxy / secure web gateway logs
Key fields: user, source IP, destination host, category, action, bytes out, user agent.
- Large `bytes_out` to file-sharing or uncategorised domains: possible exfiltration.
- Rare destination per user (`stats dc(user) by dest | where dc_user=1`), newly registered domains.
- Non-browser user agents (PowerShell, curl, Python) from user workstations.
- Beacon-like regular intervals to one host (see beaconing detection).

## Gotchas
- Behind a load balancer or CDN, the client IP is in `X-Forwarded-For`; log it or you only see the LB.
- POST bodies are not logged; a web shell's commands are invisible in access logs (use EDR on the server).
- Times: Apache logs local time with offset, IIS logs UTC by default.
- TLS-inspected vs not: proxies without inspection log only the CONNECT host, not full URLs.

## Verify
- [ ] Every suspicious file path found in logs is checked on disk (hash, creation time) on all web nodes.
- [ ] Client IP field confirmed to be the real client, not the load balancer.
