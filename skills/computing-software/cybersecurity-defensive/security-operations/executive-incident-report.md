---
id: computing-software.cybersecurity-defensive.security-operations.executive-incident-report
name: executive-incident-report
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [incident-reporting, executive-incident-report, incident-summary, business-impact, board-reporting, after-action-report, plain-language]
level: practitioner
status: draft
description: "Write an executive incident report: what happened, business impact, what was done, residual risk and decisions needed, in plain language on two pages."
sources: ["NIST SP 800-61r3 (post-incident activity, reporting)", "CySA+ CS0-003 objective 4.2 (incident response reporting)", "CSF 2.0 RS.CO and RC.CO"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Executive incident report

**Goal:** leaders understand in five minutes what happened, what it cost or could cost, and
what they must decide or fund, without technical jargon.

## Structure (two pages plus appendices)
1. **Summary (5 lines):** what happened, when it was detected, current status (contained /
   recovered), impact, and the one decision needed.
2. **Impact:** systems and data affected, customers or employees affected, downtime, financial
   estimate (ranges are fine), regulatory notifications made or required.
3. **Timeline (high level, 5-10 rows):** initial access, detection, containment, recovery, with dates.
4. **What we did:** containment, eradication, recovery, external help engaged.
5. **Root cause:** one paragraph in plain words ("an internet-facing VPN appliance was missing
   a patch released three weeks earlier").
6. **Residual risk:** what is not yet known or fixed.
7. **Recommendations and decisions:** each with owner, cost range, date, and risk if not done.
8. Appendices: technical timeline, IOCs, detailed findings (for technical readers).

## Writing rules
- Facts versus assessment: label confidence ("we assess with moderate confidence that no data left the network, based on...").
- No acronyms without expansion; no tool names unless needed.
- Numbers with units and comparisons ("4 hours of order processing downtime on 3 Oct").
- Do not speculate on attribution unless it changes a decision.
- Have legal review before distribution if there is any regulatory or litigation exposure;
  mark as privileged where counsel directs.

## Timing
- Initial brief within 24 hours of a major incident (facts known so far, next update time).
- Final report within the agreed window (often 2-4 weeks) after closure.

## Gotchas
- Reports written only for the technical team bury the decision on page six.
- Blame language ("the user failed to...") kills reporting culture; describe conditions and controls.
- Inconsistent numbers between the executive report and regulator notifications create legal risk: one source of truth.

## Verify
- [ ] A non-technical reviewer can state the impact and the decision after reading page one.
- [ ] Every recommendation has an owner and date.
