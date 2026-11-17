---
id: computing-software.cybersecurity-defensive.security-operations.soc-shift-handover
name: soc-shift-handover
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [soc-management, shift-handover, soc, follow-the-sun, open-cases, situational-awareness, handover-template]
level: practitioner
status: draft
description: "Run SOC shift handovers that lose nothing: a written template, open-case ownership transfer, watch items and a short verbal brief."
sources: ["CySA+ CS0-003 objective 4.2 (communication)", "NIST SP 800-61r3 (incident handling coordination)", "MITRE 11 Strategies of a World-Class Cybersecurity Operations Center"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SOC shift handover

**Goal:** the incoming shift knows every live issue, owns every open case, and watches for
what the outgoing shift was waiting on.

## Written handover (same template every shift, in the case system or a shared channel)
```
Shift: 2026-10-16 day -> night   Outgoing: <names>   Incoming: <names>
1. Active incidents (sev, case ID, owner now, next action, deadline)
2. Open alerts/cases older than SLA and why
3. Watch items: "expect EDR isolation confirmation for HOST-123 by 22:00"
4. Changes in the environment: maintenance windows, new detections deployed, log sources down
5. Escalations made and pending replies (who, when, contact route)
6. Queue stats: new / closed / open by priority
7. Anything unusual not yet a case
```

## Verbal brief (10-15 minutes, both shifts present)
- Walk sections 1, 3 and 4. Incoming lead reads back owners and deadlines.
- Explicitly **reassign** each open case in the tool; "the team has it" is how cases die.
- Hand over any live calls/bridges in person, with the incident commander informed.

## Rules
- A case with a pending external action (waiting on IT, waiting on user) has a follow-up time, not just a status.
- During a major incident, hand over to the incoming incident commander with an overlap of at least 30 minutes.
- Follow-the-sun teams: write handovers for readers in another language and time zone; avoid shorthand.

## Gotchas
- Verbal-only handovers vanish; written-only handovers go unread. Do both.
- Alerts that arrive during the handover meeting: one person stays on the queue.
- Pending SOAR automation (scheduled re-checks, timed unisolations) must be listed or they surprise the next shift.

## Verify
- [ ] Zero open cases with an owner who is off shift (report from the case tool after handover).
- [ ] Handover record exists for every shift; spot-check a week.
