---
id: computing-software.digital-forensics-incident-response.incident-response-process.sequencing-recovery-by-dependency
name: sequencing-recovery-by-dependency
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [recovery-sequencing, incident-recovery, recovery-planning, dfir, business-continuity]
level: advanced
status: draft
description: "Order restoration after a destructive incident by dependency: clean identity and network services first, then core platforms and business apps."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://www.cisa.gov/stopransomware/ransomware-guide", "https://csrc.nist.gov/pubs/sp/800/184/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sequencing recovery by dependency

**Goal:** restore services in an order that works technically and does not reintroduce the
attacker. SP 800-184 (Guide for Cybersecurity Event Recovery) and SP 800-61r3 RC.RP emphasise
prioritising by business impact and dependency.

## Typical order after enterprise-wide ransomware
1. **Isolated recovery network** (clean VLAN, no trust to compromised segments).
2. **Identity:** AD forest recovery from a pre-compromise DC backup, or a validated clean DC;
   krbtgt reset twice; Tier 0 credentials rotated. Entra Connect rebuilt if on-prem identity was compromised.
3. **Core network services:** DNS, DHCP, NTP, PKI (if CA not compromised; if it was, new CA).
4. **Security tooling:** EDR console, SIEM ingest, Velociraptor - every restored host gets EDR before it is reachable.
5. **Management plane:** hypervisors (rebuilt), backup server (from clean media), jump hosts.
6. **Business-critical apps** in the order agreed with the business (BIA): typically payments,
   ERP, customer-facing, then internal.
7. **Endpoints:** reimage at scale from golden image.

## Each restored system passes a gate
- Restored from a backup older than the earliest known compromise (or rebuilt from source).
- Patched, hardened, EDR installed and reporting, IOC sweep clean, local admin password rotated.
- Moved from the recovery network into production only after the gate.

## Planning artefacts
- Dependency map (which apps need AD, SQL, file shares, DNS); recovery time objective per app.
- A recovery tracker visible to leadership: system, owner, status, gate passed, ETA.

## Gotchas
- Restoring apps before identity: they cannot authenticate, and teams start creating local accounts.
- Restoring the domain from a backup taken after the attacker created persistence.
- Business pressure to skip gates for one "urgent" system; record it in the decision log.

## Verify
Every production-reconnected system has a completed gate record.
