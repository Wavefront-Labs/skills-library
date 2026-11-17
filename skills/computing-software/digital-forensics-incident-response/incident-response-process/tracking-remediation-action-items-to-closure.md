---
id: computing-software.digital-forensics-incident-response.incident-response-process.tracking-remediation-action-items-to-closure
name: tracking-remediation-action-items-to-closure
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [action-item-tracking, lessons-learned, remediation-tracking, risk-acceptance, dfir]
level: practitioner
status: draft
description: "Track post-incident remediation action items to closure: item schema, owners and due dates, evidence-based closure, risk acceptance, aging reports and recurrence checks."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://csrc.nist.gov/pubs/sp/800/61/r2/final", "https://sre.google/workbook/postmortem-culture/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tracking remediation action items to closure

Repeat incidents usually trace to an action item from last time that nobody finished. 800-61r3 places this under ID.IM (improvement); the mechanism is a tracker with ownership and evidence, reviewed on a cadence.

## Item schema
| Field | Notes |
|---|---|
| ID, source incident | Link to the case and the finding |
| Finding / contributing factor | One sentence |
| Action | Specific and testable ("Enforce phishing-resistant MFA for all admins"), not "improve MFA" |
| Type | Prevent / detect / respond / recover |
| Priority | From risk: likelihood of recurrence x impact |
| Owner | A named person in the owning team (not "IT") |
| Due date | Agreed with the owner |
| Closure evidence | Config screenshot, detection rule ID, test result |
| Status | Open / in progress / done / risk-accepted |

## Procedure
1. Create items in the organisation's normal work tracker (Jira, ServiceNow) so owners see them alongside other work; tag with the incident ID for reporting.
2. Confirm each owner accepted the item and date within a week; unaccepted items escalate to the incident sponsor.
3. Closure requires evidence reviewed by the IR team; for detection items, a test (e.g. an Atomic Red Team run) showing the alert fires.
4. Items that will not be done get a formal risk acceptance signed by the accountable executive, with a review date.
5. Report monthly: open items by age and priority, overdue items, items closed. Present overdue high-priority items to the risk committee.

## Recurrence check
When a new incident occurs, search the tracker for prior items on the same control. A recurrence with an overdue item is itself a finding.

## Gotchas
- Closing on "ticket raised with vendor" is not closure.
- Too many low-value items drown the important ones; cap at the handful that would have changed the outcome, and log the rest as suggestions.
- Owners change jobs; reassign during quarterly review.

## Verify
Every action from the last three post-incident reviews is either closed with evidence, open and within date, or formally risk-accepted.
