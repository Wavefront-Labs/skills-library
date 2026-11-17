---
id: computing-software.it-governance-risk-compliance.risk-assessment-methods.bia-rto-rpo
name: bia-rto-rpo
category: computing-software
field: it-governance-risk-compliance
product: risk-assessment-methods
tags:
- risk-assessment-methods
- bia-rto-rpo
- risk-bia-continuity
level: practitioner
status: draft
description: Run a BIA to identify critical processes, impact over time, dependencies, and set RTO, RPO, MTPD and minimum service levels.
sources:
- https://csrc.nist.gov/pubs/sp/800/30/r1/final
- https://www.fairinstitute.org/
- https://www.isaca.org/credentialing/crisc
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Business impact analysis, RTO, RPO
**Goal:** recovery objectives grounded in impact.
- Steps: list processes; assess impact over time (financial, legal, customer, safety); identify dependencies (systems, people, suppliers); set MTPD (maximum tolerable period of disruption), RTO (restore time) and RPO (maximum data loss); prioritise.
- RTO must be less than MTPD; RPO drives backup or replication design.
- Validate with process owners; revisit annually or on change.

## Self-check
Check every critical system's backup and DR design can actually meet its stated RTO and RPO.
