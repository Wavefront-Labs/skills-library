---
id: computing-software.digital-forensics-incident-response.incident-response-process.writing-the-final-incident-report
name: writing-the-final-incident-report
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [incident-report, lessons-learned, dfir-report, executive-summary, documentation, dfir]
level: practitioner
status: draft
description: "Write the final incident report: executive summary, scope, timeline, findings with evidence, impact, root cause, remediation, recommendations and appendices."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://csrc.nist.gov/pubs/sp/800/86/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Writing the final incident report

**Goal:** a report that executives, auditors, regulators, insurers and future responders can
each use, with every finding traceable to evidence.

## Structure
1. **Executive summary** (1 page): what happened, when, impact (data, systems, business),
   how it was resolved, key root cause, top 3-5 recommendations. No jargon.
2. **Scope and methodology**: questions investigated, evidence sources, tools, limitations
   (log gaps, systems not examined).
3. **Timeline**: condensed master timeline; full version in appendix.
4. **Findings** by attack stage (initial access, execution, persistence, privilege
   escalation, lateral movement, collection, exfiltration, impact) with evidence references
   and confidence.
5. **Impact**: systems affected, data accessed/exfiltrated (with how determined), downtime,
   notification decisions (by counsel).
6. **Root cause and contributing factors.**
7. **Response actions**: containment, eradication, recovery with dates.
8. **Recommendations**: prioritised, owner, effort, mapped to root causes.
9. **Appendices**: IOCs (machine-readable too), affected asset list, evidence register,
   detailed technical analysis, ATT&CK mapping.

## Writing rules
- Facts vs assessments: use explicit confidence language; say what you could not determine.
- Define "accessed" vs "exfiltrated" carefully; regulators and lawyers read these words.
- UTC timestamps throughout, stated once.
- Version-controlled drafts; legal review before distribution; mark privilege only if real.
- Separate versions if needed: privileged full report vs remediation summary for wide use.

## Gotchas
- Overstating certainty in the exec summary that the body does not support.
- Recommendations without owners never happen.

## Verify
Peer review: a second examiner checks five random findings back to evidence, and a
non-technical reader confirms the executive summary stands alone.
