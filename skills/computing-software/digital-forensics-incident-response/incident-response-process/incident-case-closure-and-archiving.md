---
id: computing-software.digital-forensics-incident-response.incident-response-process.incident-case-closure-and-archiving
name: incident-case-closure-and-archiving
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [case-closure, incident-documentation, case-archiving, evidence-retention, dfir]
level: practitioner
status: draft
description: "Close an incident case properly: closure criteria checklist, sign-off, final record completeness, archiving case files and evidence under retention and legal hold."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r2/final", "https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://docs.strangebee.com/thehive/user-guides/analyst-corner/cases/close-a-case/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Incident case closure and archiving

Cases left "open" forever distort metrics, and cases closed too early lose evidence. Closure is a defined state change with criteria and an owner.

## Closure criteria (all must be true, or explicitly waived by the incident commander)
- Containment and eradication complete; verification sweep found no remaining IOCs.
- Recovery done and systems returned to production with heightened monitoring period finished.
- Root cause determined, or documented as undetermined with the reason.
- Notifications decided: regulatory, customer, insurer, law enforcement (sent or a recorded decision not to).
- Final report delivered and accepted; lessons-learned session held; action items created in the tracker with owners (open items do not block closure; they live in the tracker).
- Evidence register reconciled: every item has a location, hash and disposition decision.
- IOCs and detections handed to the SOC; any temporary blocks reviewed for removal or permanence.

## Closing in the case platform
Set the resolution status (true positive / false positive / benign / duplicate), impact category and summary. In TheHive the close dialog asks for status and summary; make both mandatory via templates. Record final metrics: detection time, containment time, closure time, dwell time.

## Archiving
1. Freeze the case record (export to PDF/JSON with the timeline, decision log and comms log) and store with the evidence.
2. Move evidence from working storage to archive storage, recording each transfer on the chain-of-custody form; re-hash after move.
3. Apply the retention schedule: legal hold overrides normal deletion dates; note the hold reference.
4. Revoke temporary access granted for the incident (external IR firm accounts, shared folders, break-glass credentials).

## Gotchas
- Litigation or regulatory inquiry can arrive months later; check with Legal before scheduling disposal.
- Reopening is normal; link a reopened case to the original rather than starting fresh.

## Verify
A reviewer who was not on the case can open the archive and find the report, timeline, evidence list with hashes and the closure sign-off.
