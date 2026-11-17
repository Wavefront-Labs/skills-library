---
id: computing-software.systems-network-administration.network-design.firewall-logging-design
name: firewall-logging-design
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, firewall-design, firewall-logging, syslog, siem, log-retention]
level: practitioner
status: docs-checked
description: "Design firewall logging: which rules log at session end vs start, deny logging, syslog/CEF to a SIEM, volume and retention, and fields needed for investigations."
sources:
  - https://csrc.nist.gov/pubs/sp/800/92/final
  - https://csrc.nist.gov/pubs/sp/800/41/r1/final
  - https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/monitoring/use-syslog-for-monitoring
  - https://www.ncsc.gov.uk/collection/device-security-guidance/managing-deployed-devices/logging-and-protective-monitoring
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Firewall logging

## What to log
| Traffic | Log? |
|---|---|
| Allowed internet egress / ingress | yes, session end (bytes, duration, app, user) |
| Denies from internal sources | yes, always (malware beacons, misconfig) |
| Denies of internet background noise to the edge | summarise or sample; high volume, low value |
| Internal allowed east-west | yes for sensitive zones; volume heavy, consider flow export instead |
| Admin access, config changes, HA events, VPN logins | yes, to a separate audit stream |
| Threat/IPS/URL/file events | yes |

Log at **session end** for allowed traffic (includes bytes and duration); log at start only when you
need real-time visibility of long sessions.

## Transport and format
- Forward logs to a central collector by syslog or vendor log forwarding; prefer a reliable, encrypted
  transport where the device supports it (UDP can drop messages under load) and a structured format
  the SIEM can parse.
- NTP-synchronised timestamps, UTC preferred.
- Include NAT translations, user identity, application, and rule name or ID.
- Rule names must be meaningful so log searches map to policy.

## Volume and retention
Estimate events per second x average event size x seconds per day for storage; measure the average
size from a sample of your own logs. Set retention from your policy and any compliance requirement;
use hot/warm/cold tiers.

## Hygiene
- Alert on log source going silent.
- Do not log on "any any deny" cleanup rules facing the internet at full detail if it floods the SIEM;
  use counters + sampling.
- Protect logs from tampering (separate admin domain, WORM storage).

## Verify
- [ ] Test connection from a known host appears in the SIEM within a minute with user, app, NAT and rule fields parsed.

## Checked

2026-10-28: The NCSC device logging page confirms that rsyslog/syslog can forward logs to a remote log server. NIST SP 800-92 and 800-41 and the Palo Alto syslog page returned only abstracts, so no figures could be confirmed. Removed: event size and 5000 EPS volume estimate, the PCI DSS retention figures, CEF/LEEF/JSON format names and the vendor field names (User-ID, FSSO, app-ID). The logging table is design guidance, not a checkable figure.
Method: documentation only; no commands were run.
