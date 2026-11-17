---
id: computing-software.it-support-helpdesk.servicenow.problem-closure-and-fix-verification
name: problem-closure-and-fix-verification
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, problem-management, problem-closure, fix-verification, accept-risk, recurrence-monitoring, known-error-retirement, itil-4]
level: practitioner
status: draft
description: "Close problems on evidence: monitoring windows after a fix, recurrence checks against linked incidents, retiring known errors, accept-risk closures, and closure notes for reuse."
sources:
  - "https://www.axelos.com/certifications/itil-service-management"
  - "https://www.servicenow.com/docs/"
  - "https://www.thinkhdi.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# problem-closure-and-fix-verification

Goal: problems close because the fault is gone, proven by data — and the
knowledge they produced stays findable.

## Verify the fix
1. Fix deployed via change — change closed successful, deployment coverage
   confirmed (e.g. all affected devices have the new driver, not just the
   pilot).
2. **Monitoring window** sized to the problem's frequency: if it recurred
   weekly, watch 4+ weeks; daily, 1–2 weeks.
3. Query for new incidents with the same symptom/CI since the fix date
   (same search used to find the trend). Zero or near-baseline → proceed.
4. If incidents continue: reopen RCA — the cause was partial or the fix
   didn't reach everyone.

## Close
- Resolution notes: root cause (one paragraph), fix (change number),
  verification evidence (incident counts before/after), preventive
  measures.
- **Retire or update the known-error article** (mark fixed in version X).
- Notify stakeholders and optionally the callers of linked incidents ("the
  issue you reported has been permanently fixed").
- Close problem tasks.

## Accept risk
When fixing costs more than the impact, or no fix exists (vendor won't fix,
legacy system retiring): business owner formally accepts the risk; record
who and why, keep the workaround published, set a review date.

## Problem board metrics
Problems closed with verified fix, average age, incidents avoided
(estimated from pre-fix rate), problems reopened.

## Gotchas
- Closing on change completion alone skips verification — a classic audit
  finding.
- Long monitoring windows keep problems "Resolved" — fine; that's what the
  state is for.

## Verify
Every closed problem has before/after incident evidence and a disposition
for its known-error article.
