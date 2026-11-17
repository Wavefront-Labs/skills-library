---
id: computing-software.digital-forensics-incident-response.incident-response-process.building-the-ir-escalation-matrix
name: building-the-ir-escalation-matrix
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [escalation-matrix, incident-response-plan, incident-severity, dfir, notification]
level: practitioner
status: draft
description: "Build the escalation and notification matrix: who is told at each severity, by when, through which channel, and who can declare or downgrade."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://csrc.nist.gov/pubs/sp/800/61/r2/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Building the IR escalation matrix

**Goal:** remove judgement calls about "should I wake the CISO?" by writing down, per severity,
who must be notified, within what time, and how.

## Structure
One table, rows = severity, columns = audiences:

| Severity | SOC lead | IR manager | CISO | Legal / privacy | Exec / board | Comms / PR | Regulators |
|---|---|---|---|---|---|---|---|
| Sev-1 (critical) | immediate | 15 min | 30 min | 1 h | 2 h | 2 h | per clock table |
| Sev-2 (high) | immediate | 30 min | 4 h | 4 h if PII | next business day | on request | assess |
| Sev-3 (medium) | 1 h | next shift | weekly report | if PII | none | none | none |
| Sev-4 (low) | queue | none | none | none | none | none | none |

For each cell record: channel (phone call, page, Signal, email), primary + deputy, and
acknowledgement requirement (page re-fires until acknowledged).

## Rules to write alongside
- **Who can declare / upgrade / downgrade:** any analyst may upgrade; only the IR manager or
  incident commander may downgrade, with a recorded reason.
- **Automatic escalators:** suspected ransomware, domain admin compromise, confirmed regulated
  data exposure, extortion contact, media enquiry - always Sev-1 regardless of scale.
- **Time-boxing:** if a Sev-2 is not scoped within N hours, escalate.
- **After hours:** paging tool rota, not personal mobile numbers in a spreadsheet.
- **Legal early:** legal is notified before written conclusions are circulated, to preserve
  privilege options.

## Implementation
- Encode it in the paging tool (PagerDuty/Opsgenie escalation policies) so it is executed,
  not remembered.
- Mirror the matrix in the case platform severity field so changing severity triggers the
  right notifications.

## Gotchas
- Notifying executives by email for a Sev-1 when email may be compromised (BEC).
- Matrices that require notifying a regulator before legal has assessed applicability.
- No deputy column: holidays break the chain.

## Verify
Run a paging test for each severity quarterly and record time-to-acknowledge per role.
