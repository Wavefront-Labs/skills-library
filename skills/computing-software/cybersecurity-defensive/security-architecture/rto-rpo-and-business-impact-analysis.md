---
id: computing-software.cybersecurity-defensive.security-architecture.rto-rpo-and-business-impact-analysis
name: rto-rpo-and-business-impact-analysis
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [resilience, rto-rpo, business-impact-analysis, bia, mtd, recovery-time-objective, recovery-point-objective, service-tiering, mtbf, mttr]
level: practitioner
status: draft
description: "Run a business impact analysis to set RTO, RPO and maximum tolerable downtime per service, tier services, and turn those numbers into backup and DR requirements."
sources: ["NIST SP 800-34 Rev. 1 (business impact analysis)", "ISO 22301 Business continuity management", "CompTIA Security+ SY0-701 objective 5.2 (RTO, RPO, MTTR, MTBF)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# RTO, RPO and business impact analysis

**Goal:** recovery targets come from what the business can tolerate, so backup frequency, DR
spend and restore order are justified rather than guessed.

## Definitions
- **MTD** (maximum tolerable downtime): beyond this the business suffers unacceptable harm.
- **RTO** (recovery time objective): target time to restore the service; must be below MTD
  with margin for detection and decision time.
- **RPO** (recovery point objective): maximum acceptable data loss measured in time.
- **MTTR / MTBF**: reliability metrics for components (repair time, time between failures).

## BIA process
1. List business processes (not systems) with their owners.
2. For each, interview the owner: impact over time if unavailable (1 h, 4 h, 1 day, 1 week)
   in financial, regulatory, safety, customer and reputational terms.
3. Set MTD where impact becomes unacceptable; set RTO and RPO accordingly.
4. Map processes to supporting systems and their dependencies (identity, network, third parties).
   A system inherits the strictest RTO of the processes it supports.
5. Tier services:

| Tier | RTO | RPO | Example |
|---|---|---|---|
| 0 | Hours | Minutes | Identity, DNS, core network (everything depends on them) |
| 1 | < 4 h | < 15 min | Payments, order processing |
| 2 | < 24 h | < 4 h | Internal business apps |
| 3 | < 1 week | < 24 h | Reporting, archives |

6. Translate: RPO 15 minutes means log shipping or replication, not nightly backups. RTO 4 hours
   for 20 TB means warm standby, not restore from tape.
7. Get sign-off from business owners on targets and the cost to achieve them.

## Gotchas
- Owners say everything is critical: ask what they would actually do (manual workaround?) after 1 hour, 1 day.
- Forgetting tier 0 dependencies makes tier 1 RTOs impossible.
- Ransomware recovery times are longer than infrastructure failure times (investigation, cleaning); set cyber-specific objectives.
- BIA goes stale; revisit annually and after major changes.

## Verify
- [ ] Each tier-1 service has documented RTO/RPO, dependencies and owner sign-off.
- [ ] Backup and DR configurations demonstrably meet the RPO/RTO (restore test results).
