---
id: computing-software.systems-network-administration.network-design.egress-filtering
name: egress-filtering
category: computing-software
field: systems-network-administration
product: network-design
tags: [firewall, egress-filtering, outbound-rules, proxy, dns-egress, least-privilege-rules]
level: practitioner
status: docs-checked
description: "Restrict outbound traffic: default-deny egress for servers, proxy-only web for users, DNS/NTP/SMTP pinned to internal servers, and rolling it out from logs without breaking apps."
sources:
  - https://www.cisa.gov/sites/default/files/publications/CISA_MS-ISAC_Ransomware%20Guide_S508C.pdf
  - https://www.cisecurity.org/controls/network-infrastructure-management
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Egress filtering

Most networks filter inbound tightly and allow `any` outbound. Malware C2, data exfiltration and
reverse shells all rely on that.

## Target policy
| Source | Allowed out |
|---|---|
| Servers | only to named destinations they need (update repos via proxy/mirror, partner APIs, SaaS endpoints); default deny |
| User subnets | web via proxy/SWG (or direct HTTP/HTTPS with URL filtering), no direct SMTP, no direct DNS |
| Infrastructure | NTP/DNS only from the designated internal servers |
| Mail | SMTP only from mail gateways |
| All | block outbound SMB, NetBIOS, RDP, and LDAP/RPC to the internet |

## Pin core services
- DNS: only internal resolvers may query the internet over plain DNS (and DNS over TLS). Clients use
  internal resolvers; block both from everything else. Handle DNS over HTTPS with SWG policy.
- NTP: only internal NTP servers reach public NTP.
- SMTP: only mail relays may send outbound; stops spambots on infected hosts.

## Roll out without breaking things
1. Log mode: add an explicit `allow any log` at the bottom of each server zone's outbound policy.
2. Collect a representative period of flows (firewall logs, NetFlow), including month-end jobs. Group by source app/server and destination
   FQDN/ASN.
3. Write specific allow rules (FQDN objects where supported for SaaS) with owners.
4. Change the bottom rule to deny+log for one zone at a time; watch the deny log daily and have a
   fast exception process.

## Detection value
Denied outbound attempts from servers are high-signal alerts (a compromised host calling home).
Forward them to the SIEM with a dedicated use case.

## Gotchas
- Cloud and SaaS IPs change constantly; use FQDN or vendor-published IP lists, not hand-maintained IPs.
- Certificate revocation (OCSP/CRL endpoints) must stay reachable or TLS breaks oddly.
- Windows Update, AV and EDR need their endpoints; get vendor lists before enforcing.

## Verify
- [ ] From a test server, `curl https://example.com` fails while approved destinations work; deny
  logs show the attempt.

## Checked

2026-10-28: The CISA ransomware guide returned 403 and the CIS controls page has no egress text, so nothing was confirmed from the sources. Removed all port numbers (25, 53, 80/443, 445, 853, 3389), the 2-4 week log collection period, and the Microsoft 365 endpoints feed reference. What remains is design process (default deny for servers, pin DNS/NTP/SMTP to internal hosts, log-then-enforce rollout).
Method: documentation only; no commands were run.
