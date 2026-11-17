---
id: business-finance.risk-management.business-continuity-planning.business-impact-analysis-and-recovery-objectives
name: business-impact-analysis-and-recovery-objectives
category: business-finance
field: risk-management
product: business-continuity-planning
tags: [business-continuity-planning, risk-management, bcp, bcm, business-impact-analysis, bia, rto, recovery-time-objective, rpo, recovery-point-objective, mtpd, maximum-tolerable-period-of-disruption, mbco, critical-processes, dependencies, single-points-of-failure, continuity-strategies, disaster-recovery, tabletop-exercise, crisis-management, iso-22301, operational-resilience, impact-tolerance, call-tree]
level: practitioner
status: draft
description: "Run a business impact analysis that sets MTPD, RTO and RPO per process, maps people, system, site and supplier dependencies, and turns the gaps into tested continuity strategies."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Business impact analysis and recovery objectives

**Goal:** decide which activities must come back first and how fast, based on what the
disruption actually costs — then check that recovery capabilities can really meet those
times. A continuity plan not built on a BIA is a phone list. Reference standard: ISO 22301
(business continuity management systems); ISO/TS 22317 covers BIA guidance.

## 1. Scope and the impact scale
List the organisation's products/services and the processes delivering them. Agree impact
categories and bands before interviews: financial (revenue lost, penalties), customer harm,
regulatory/legal, reputation, safety, contractual SLAs. Use the same bands as the ERM
impact scale where possible.

## 2. Interview process owners
For each process, ask how impact grows over time if it stops: at 1 hour, 4 hours, 1 day,
3 days, 1 week, 1 month. Record the time at which impact becomes unacceptable. From this:
- **MTPD** (maximum tolerable period of disruption) — after this the organisation's
  viability or obligations are seriously threatened.
- **RTO** (recovery time objective) — target time to resume, set **shorter than MTPD** to
  leave margin.
- **MBCO** (minimum business continuity objective) — the reduced level of service that's
  acceptable during disruption (e.g. 60% of payments, priority clients only).
- **RPO** (recovery point objective) — how much data loss is tolerable, measured as time
  since last good copy (e.g. 15 minutes for trading, 24 hours for HR records).
Ask also about peak periods (month-end, seasonal) — the BIA should reflect the worst
plausible timing, not an average Tuesday.

## 3. Map dependencies
For each prioritised process: people (minimum staff, key skills, single experts), premises,
IT applications and data, equipment, **third parties and suppliers** (and their own
continuity arrangements), upstream internal processes, and vital records. Then:
- Check each **IT system's RTO/RPO capability** (from DR testing) against the process RTO/RPO.
  A process with a 4-hour RTO depending on a system with 48-hour recovery is the classic gap.
- Flag **single points of failure** — one person, one site, one supplier, one network link.

## 4. Choose continuity strategies
Per gap: alternate site or work-from-home capability, cross-training and documented
procedures, manual workarounds, DR architecture changes (replication, backups with
tested restores), second suppliers or contractual SLAs, stock buffers. Cost the options
against the impact avoided; sign off accepted residual gaps at the right level.

## 5. Plans and exercises
- Plans are short and action-oriented: activation criteria, who decides, call tree,
  first-hour checklist, recovery steps per process in priority order, contacts.
- **Exercise** at least annually: tabletop walk-throughs for decision-making, technical DR
  failover tests for systems, call-tree tests. Record what failed and fix it.
- Financial-services regulators in several jurisdictions (e.g. UK operational-resilience
  rules) require **important business services** with **impact tolerances** and scenario
  testing — *check whether such a regime applies to you*.

## Gotchas
- Every process owner says their process is critical with a 1-hour RTO. Challenge with the
  impact curve and costs; prioritisation is the point.
- RTOs set without checking IT and supplier recovery capability.
- Ignoring people: a pandemic or key-person loss with all systems running.
- Backups that have never been restored are not backups.
- Plans held only on the systems that are down; keep offline/printed copies.
- BIA done once and never refreshed after reorganisations or system changes (review annually).

## Verify
- [ ] Each process has an impact-over-time curve, MTPD, RTO (< MTPD), MBCO and RPO.
- [ ] Dependencies mapped, including suppliers and key people.
- [ ] IT recovery capability compared with process RTO/RPO; gaps listed.
- [ ] Strategy or signed risk acceptance for every gap.
- [ ] Plans exercised in the last 12 months, with lessons tracked to closure.

Related: business-finance.risk-management.enterprise-risk-management.risk-register-and-appetite-statement.
