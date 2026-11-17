---
id: computing-software.cybersecurity-defensive.security-operations.firewall-log-analysis
name: firewall-log-analysis
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [log-analysis, firewall-log-analysis, palo-alto-traffic-logs, port-scan-detection, denied-traffic, session-end-reason, egress, nat-attribution]
level: practitioner
status: docs-checked
description: "Analyse firewall logs using Palo Alto traffic log fields: action and session end reason, rule, NAT translation for attribution, bytes, and scan or egress patterns."
sources: ["https://docs.paloaltonetworks.com/ngfw/administration/monitoring/use-syslog-for-monitoring/syslog-field-descriptions/traffic-log-fields", "https://csrc.nist.gov/pubs/sp/800/92/final"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Firewall log analysis

Field names below are from the Palo Alto Networks (PAN-OS) traffic log field reference. Other
vendors use different names and values; read your vendor's log reference before translating.

## Know your fields (PAN-OS traffic log)
- `src`, `dst` (original session addresses), `sport`, `dport`, `proto`, `app` (application), `category` (URL category).
- `subtype`: `start`, `end`, `drop` (dropped before the application is identified and no rule allows it) or `deny` (dropped after the application is identified, by a block rule or no allowing rule).
- `action`: allow, deny, drop, drop ICMP, reset both, reset client, reset server. `action_source` says whether the action came from the application or from policy.
- `rule` (rule the session matched), `rule_uuid` (permanently identifies the rule), `from` / `to` (zones), `srcuser` / `dstuser`.
- `bytes` (total), `bytes_sent` (client to server), `bytes_received` (server to client), `packets`, `pkts_sent`, `pkts_received`, `start`, `elapsed`.
- NAT: `natsrc`, `natdst`, `natsport`, `natdport` (post-NAT values); `repeatcnt` counts sessions with the same source, destination, application and subtype within 5 seconds.
- `session_end_reason`, reported by priority when several apply: threat, policy-deny, decrypt-cert-validation, decrypt-unsupport-param, decrypt-error, tcp-rst-from-client, tcp-rst-from-server, resources-unavailable, tcp-fin, tcp-reuse, decoder, aged-out, unknown, n/a (n/a when the log type is not end).
- `flags` is a 32-bit field decoded by AND-ing bit values (for example 0x00400000 means a NAT translation was performed).

## Attribution through NAT
Outbound traffic to an attacker shows your public IP. Traffic logs record `natsrc` and `natsport`, so
given an external report with public IP, port and time, search for matching `natsrc` and `natsport`
within a tight time window to find the internal `src`.

## Patterns (analyst heuristics, not vendor statements)
- Inbound scans: one source, many ports or destinations denied; matters when followed by an allow to the same target.
- Internal scanning or lateral movement: an internal host contacting many internal hosts on admin ports.
- Egress anomalies: long `elapsed` with steady small `bytes_sent` (beacon-like), large `bytes_sent` to rare destinations, unexpected `app` on a common port.
- Denied egress from servers: servers rarely need new outbound destinations.
Set numeric thresholds from your own baseline.

## Gotchas
- `session_end_reason` is only meaningful on end logs; a long session shows its end reason only when the end log is written.
- Log volume drives retention; NIST SP 800-92 covers log management planning (infrastructure and processes) at a high level and is not a step-by-step guide.
- Keep clocks and time zones consistent when correlating firewall logs with a SIEM.

## Verify
Pick a known connection (for example your own test from a host) and find it end to end: source host,
rule, NAT, bytes, end reason.

## Checked
Date: 2026-11-07. Read: the Palo Alto "Traffic Log Fields" page (format list, subtype, action, session end reason list and priority text, flags, NAT, bytes, rule and zone fields; later sections on tunnel/SD-WAN/device fields only scanned) and the NIST SP 800-92 abstract page. Removed as unconfirmed: all FortiGate field names and claims (the Fortinet log reference page fetched is only an introduction), the generic cross-vendor field mapping (`policyid`, `sentbyte`, `utmaction`, `transip`), `src_user` as a field name (the page names it `srcuser`), the Splunk CIM `tstats` example, "logs at session end by default" and "log at session start" advice, the cleanup-rule claim, the `incomplete`/`insufficient-data` App-ID values, `action=close/accept/timeout` meanings, and the 445/3389/5985/22 port list. The old URL with `pan-os/11-1` redirects to the current page; the source link now uses the current address.
Method: documentation only; no commands were run.
