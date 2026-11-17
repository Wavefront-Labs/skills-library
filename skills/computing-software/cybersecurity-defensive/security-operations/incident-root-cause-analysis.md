---
id: computing-software.cybersecurity-defensive.security-operations.incident-root-cause-analysis
name: incident-root-cause-analysis
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [incident-reporting, root-cause-analysis, five-whys, contributing-factors, blameless-postmortem, lessons-learned, corrective-actions, causal-analysis]
level: practitioner
status: draft
description: "Find the root cause and contributing factors of a security incident with timeline-driven 5 Whys and control-failure analysis, producing tracked corrective actions."
sources: ["NIST SP 800-61r3 (lessons learned and improvement)", "CSF 2.0 ID.IM (improvement)", "CySA+ CS0-003 objective 3.3 (root cause analysis, lessons learned)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Incident root cause analysis

**Goal:** understand why the incident was possible and why it was not stopped sooner, and fix
those conditions so the same class of incident does not recur.

## Inputs
Final technical timeline, detection timeline (what fired, when, who saw it), decision log,
and interviews with responders and system owners. Hold the review within two weeks while
memory is fresh. Blameless: focus on conditions and controls, not individuals.

## Method
1. **Map the kill chain** of the incident: initial access, execution, persistence, privilege,
   lateral movement, objective. For each step ask:
   - Which preventive control should have stopped it? Why did it not (absent, misconfigured, bypassed, exception)?
   - Which detective control should have seen it? Did it fire? Was the alert actioned?
2. **5 Whys** on the main failures, branching where there are several causes:
   - VPN was exploited -> patch not applied -> appliance not in patch inventory ->
     network devices owned by a team outside the vulnerability programme -> no asset ownership process for network appliances.
   The root cause is the last actionable condition, usually a process or ownership gap.
3. **Contributing factors:** staffing, alert fatigue, missing logs, slow approvals, unclear authority.
4. **What went well:** keep it; it is evidence for what to protect in budgets.

## Corrective actions
| Action | Addresses | Owner | Due | Verification |
|---|---|---|---|---|
| Add network appliances to scanner scope and patch SLA | Root cause | VM lead | 30 days | Scan coverage report |
| Alert on VPN logins from new countries for admins | Detection gap | DE lead | 14 days | Replay test |
Prefer a few systemic actions over many local fixes. Track to closure in the risk or ticket system and report status monthly.

## Gotchas
- Stopping at "human error" (user clicked) is not a root cause: why did one click lead to compromise?
- Too many actions dilutes effort; prioritise those that break the most attack paths.
- Actions without verification are wishes; define how you will test each fix.

## Verify
- [ ] Root cause stated as a correctable condition, with evidence.
- [ ] Each corrective action has an owner, date and verification test, and is tracked to completion.
