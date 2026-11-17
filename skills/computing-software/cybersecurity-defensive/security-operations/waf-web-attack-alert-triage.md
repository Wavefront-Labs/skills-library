---
id: computing-software.cybersecurity-defensive.security-operations.waf-web-attack-alert-triage
name: waf-web-attack-alert-triage
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [waf-alert-triage, alert-triage, waf, web-attacks, owasp-crs, sql-injection, xss, soc]
level: practitioner
status: draft
description: "Triage WAF and web attack alerts (SQLi, XSS, path traversal, RCE probes): read the request, check the response and backend logs, separate scanning from targeted exploitation."
sources: ["https://coreruleset.org/docs/", "https://docs.aws.amazon.com/waf/latest/developerguide/logging.html", "https://owasp.org/www-project-top-ten/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# WAF and web attack alert triage

## Read the request
- Full URI, query, body (if logged), headers, method, source IP, user agent; WAF rule IDs matched
  (OWASP CRS 942xxx SQLi, 941xxx XSS, 930xxx LFI, 932xxx RCE, 913xxx scanner detection) and
  anomaly score.
- Decode payloads (URL, double URL, base64, unicode) before judging.

## Blocked vs allowed
- Blocked and from a mass scanner (Nuclei/zgrab user agents, many targets, known scanner ASN): log,
  no action beyond trend tracking.
- **Allowed** (detection mode, or rule excluded) or **blocked but payload variants continue from the
  same source**: investigate.

## Did it work?
- Response code and size from WAF/load balancer/app logs: 500s on SQLi probes suggest injection
  reaching the database; unusual large 200 responses on traversal (`/etc/passwd` contents size).
- Application logs/APM traces for the request ID; database error logs at that time.
- Follow-on behaviour: new outbound connections from the web server, new files in web roots
  (web shell), new processes spawned by the web server user (EDR).
- Is the targeted CVE relevant? (Log4Shell probes against a non-Java stack are noise.)

## Targeted vs opportunistic
Targeted: payloads tailored to your parameters, authenticated sessions, slow rate, from residential
IPs or your customers' accounts; recon of your specific paths. Escalate.

## Responses
- Block source/ASN temporarily (rate-limit rules), virtual patch rule for the endpoint, notify app
  owner, open vulnerability ticket if exploitation evidence or a scanner confirms the flaw.

## Gotchas
- False positives from legitimate content (rich text, JSON with SQL keywords): tune CRS with rule
  exclusions per parameter, never by disabling the whole rule group.
- WAF logs often omit bodies; enable sampled full logging for investigations.

## Verify
Case records decoded payload, block/allow, evidence of success or not, and follow-up (tuning,
virtual patch, vuln ticket).
