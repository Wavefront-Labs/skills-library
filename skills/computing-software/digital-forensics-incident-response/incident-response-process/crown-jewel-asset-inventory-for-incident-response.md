---
id: computing-software.digital-forensics-incident-response.incident-response-process.crown-jewel-asset-inventory-for-incident-response
name: crown-jewel-asset-inventory-for-incident-response
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [crown-jewels, asset-inventory, ir-preparation, business-impact, dfir]
level: practitioner
status: draft
description: "Build an IR-ready crown-jewel inventory: critical business services, their systems, identities, data stores, owners, log sources and dependencies, kept current for triage."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://www.mitre.org/sites/default/files/publications/pr-13-1028-mission-assurance-cjafor.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Crown-jewel asset inventory for incident response

During an incident the questions are "does this host matter, who owns it, and what depends on it". An asset CMDB rarely answers them; a crown-jewel register built for IR does. It maps to CSF ID.AM and supports severity scoring in 800-61r3.

## What to record per crown jewel
| Field | Example |
|---|---|
| Business service | Payments clearing |
| Impact if down / leaked | Revenue per hour, regulatory, safety |
| Systems | App servers, DB cluster, message queue (hostnames, cloud resource IDs) |
| Identities | Service accounts, admin groups, CI/CD deploy keys |
| Data stores | DB names, buckets, file shares, data classification |
| Upstream dependencies | AD, DNS, PKI, IdP, hypervisor cluster |
| Log sources and retention | DB audit 90 d, app logs in SIEM 1 y |
| Business and technical owners | Role + 24x7 contact |
| Recovery | RTO/RPO, backup location, rebuild runbook link |

## Building it
1. Start from the business: run a short workshop (MITRE Crown Jewels Analysis style) asking which 10 to 20 services would make the news if lost.
2. Trace each service down to systems and identities using architecture diagrams, cloud tags and network flows.
3. Include tier-0 dependencies (domain controllers, IdP, PKI, backup servers, hypervisors) as crown jewels in their own right; attackers target them to reach everything else.
4. Tag the assets in the SIEM/EDR (e.g. an asset criticality field or watchlist) so alerts on them auto-raise severity.
5. Review quarterly and after each major change; store it where the war room can reach it if AD is down.

## Gotchas
- A crown jewel without a logging row is a blind spot; flag it to the logging baseline owner.
- Keep the list short. If everything is critical, triage gains nothing.
- The register itself is sensitive (it is an attacker's target list); restrict access.

## Verify
Pick a random crown jewel and, within 10 minutes, name its owner, its admin identities and where its last 30 days of logs live.
