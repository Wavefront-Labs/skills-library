---
id: computing-software.digital-forensics-incident-response.incident-response-process.updating-playbooks-and-the-ir-plan-after-an-incident
name: updating-playbooks-and-the-ir-plan-after-an-incident
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [playbook-update, ir-plan-review, lessons-learned, runbooks, dfir]
level: practitioner
status: draft
description: "Update playbooks and the IR plan after an incident: mine the decision log for deviations, edit steps and contacts, version and approve changes, then exercise the new version."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r2/final", "https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://www.cisa.gov/sites/default/files/publications/Federal_Government_Cybersecurity_Incident_and_Vulnerability_Response_Playbooks_508C.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Updating playbooks and the IR plan after an incident

A playbook nobody followed during the incident is telling you something. Each real incident is the best test of the plan; changes should be made within weeks, not saved for the annual review.

## Find what to change
Walk the decision log and timeline side by side with the playbook used:
- **Skipped steps**: why? Irrelevant (remove or make conditional) or forgotten (move earlier, add a check)?
- **Improvised steps**: anything responders did that was not written down and worked: add it.
- **Blocked steps**: missing access, tool, contact or authority: add the prerequisite to preparation.
- **Wrong order**: e.g. reset passwords before blocking the attacker's persistence; fix sequencing.
- **Missing playbook**: if the incident type had no playbook, write one from this case.
Also check the plan: severity criteria that misclassified the incident, escalation paths that failed, contacts that were stale, notification timelines missed.

## Making the change
1. Edit in the controlled copy (version-controlled repo or document management), one change set per incident referencing the case ID.
2. Write steps as actions with an owner and a done-check ("IR lead disables account in Entra; verify sign-in logs show no new successful sign-ins").
3. Have the people who ran the incident review the change; get plan-level changes approved by the plan owner.
4. Bump version, record a changelog line, publish to every location (IR platform, offline jump-kit copy).
5. Remove superseded copies; old PDFs in shared drives cause responders to follow dead procedures.

## Exercise
Run a short tabletop on the changed section within the quarter. A change that was never exercised is a guess.

## Gotchas
- Do not over-fit to one incident; generalise the step so it works for the next variant.
- Automations in SOAR mirror the playbook; update them in the same change.

## Verify
The changelog shows a playbook or plan change linked to each major incident in the last year, and the offline copy carries the latest version number.
