---
id: law-government.platform-and-community-governance.content-moderation-operations.running-moderation-queues-with-quality-and-wellbeing
name: running-moderation-queues-with-quality-and-wellbeing
category: law-government
field: platform-and-community-governance
product: content-moderation-operations
tags: [content-moderation-operations, platform-and-community-governance, content-moderation, moderation-ops, review-queue, queue-design, prioritisation, severity-tiers, sla, turnaround-time, routing, language-routing, escalation-path, escalation-matrix, quality-assurance, qa-sampling, inter-rater-reliability, decision-consistency, calibration-sessions, accuracy-rate, false-positives, false-negatives, moderator-wellbeing, resilience-programme, exposure-limits, bpo, outsourcing, workforce-management, csam-reporting, ncmec, imminent-harm, trust-and-safety]
level: practitioner
status: draft
description: "Run content review at scale: severity-tiered queues and SLAs, routing, escalation paths, QA sampling and calibration for consistency, staffing models and moderator wellbeing safeguards."
sources: ["Trust & Safety Professional Association, operations curriculum (public)", "Santa Clara Principles (2021)", "Published research on moderator wellbeing and exposure to traumatic content"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running moderation queues with quality and wellbeing

**Goal:** get the right decision on reported or flagged content, fast enough for its
severity, consistently across thousands of decisions and reviewers, without harming the
people doing the work. Applies to in-house and outsourced (BPO) operations.
Legally mandated timelines and reporting duties differ by jurisdiction (e.g. US
providers' duty to report apparent child sexual abuse material to NCMEC; EU DSA notice-
and-action and statement-of-reasons rules; UK Online Safety Act duties; Germany's
NetzDG legacy timelines) — map these into the queue design.

## 1. Design the queues
- **Intake sources:** user reports, automated classifiers, trusted flaggers, legal
  requests, proactive sweeps. Tag every item with its source.
- **Severity tiers** with target turnaround, for example:
| Tier | Examples | Target |
|---|---|---|
| P0 | imminent threat to life, live self-harm, child exploitation | minutes; 24/7 specialist team; law-enforcement escalation |
| P1 | credible threats, doxxing, non-consensual intimate imagery, terror content | hours |
| P2 | harassment, hate, scams | within a day |
| P3 | spam, low-harm policy violations | days / automated |
Targets are illustrative — set them from harm, volume and legal duties.
- **Routing:** by policy area (specialist queues for child safety, violent extremism),
  language and market, and reviewer clearance level.
- Prioritise within a queue by severity score and virality (views per hour), not first-in-first-out.

## 2. Escalation paths
Write an escalation matrix: what goes to policy specialists (novel edge cases), legal
(court orders, lawful-access requests, defamation), communications (high-profile accounts,
press attention), law enforcement liaison (imminent harm), and executive on-call
(crises). Every escalation has a named owner per shift and a response time.

## 3. Consistency and quality
- **QA sampling:** independently re-review a random sample of each reviewer's decisions
  (commonly 2-5%, more for new reviewers), plus targeted sampling of appeals overturned.
- Track accuracy by policy, reviewer and vendor; separate false positives (wrongful
  removals) from false negatives (missed violations).
- **Calibration sessions** weekly: reviewers and QA decide the same tricky items and
  discuss disagreements; feed unclear cases back to policy writers.
- Measure inter-rater agreement on a golden set; falling agreement signals unclear policy
  or training drift.
- Decision tooling should show the relevant policy snippet and require a reason code —
  this also produces the statement of reasons users and regulators may require.

## 4. Staffing and workforce management
Forecast volume by queue, hour and language; account for seasonal spikes, elections and
crises. Use average handling time per item type to set headcount; build surge capacity
(cross-trained reviewers, vendor surge clauses). Track backlog age, not just size.

## 5. Moderator wellbeing (non-negotiable)
- Limit continuous exposure to graphic queues; rotate reviewers between high- and
  low-severity work; schedule breaks.
- Tooling: default greyscale, blurring, muting, thumbnail-first viewing for graphic media.
- Access to qualified psychological support during and after employment; no penalty for
  stepping away from a distressing item.
- Informed consent and screening before assigning someone to the most severe queues.
- Hold vendors to the same standards contractually and audit them.

## 6. Metrics to report weekly
Volume in and out per queue; turnaround vs target; backlog age; accuracy (QA) and appeal
overturn rate; escalations; wellbeing indicators (sick leave, attrition, support usage).

## Gotchas
- Speed targets that push reviewers to guess — accuracy and wellbeing collapse together.
- One global queue: missing language expertise produces systematic errors in some markets.
- QA that only measures agreement with QA, never checking whether the policy itself is clear.
- Mandatory reporting items (e.g. CSAM) handled in a general queue without the legal workflow.

## Verify
- [ ] Severity tiers with targets mapped to legal deadlines; routing by policy and language.
- [ ] Written escalation matrix with named owners per shift.
- [ ] QA sampling, golden set and weekly calibration in place; accuracy tracked by policy.
- [ ] Volume forecast and surge plan documented.
- [ ] Wellbeing safeguards in place for staff and vendors; metrics reported weekly.
