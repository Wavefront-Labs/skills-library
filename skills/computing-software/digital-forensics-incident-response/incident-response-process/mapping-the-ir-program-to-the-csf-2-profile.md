---
id: computing-software.digital-forensics-incident-response.incident-response-process.mapping-the-ir-program-to-the-csf-2-profile
name: mapping-the-ir-program-to-the-csf-2-profile
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [csf-2-profile, nist-sp-800-61r3, nist-csf, ir-program, gap-assessment, dfir]
level: practitioner
status: draft
description: "Map an incident response program to the NIST CSF 2.0 community profile in SP 800-61r3: score each Govern-to-Recover outcome, find gaps and build a target profile."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://www.nist.gov/cyberframework", "https://csrc.nist.gov/pubs/cswp/29/the-nist-cybersecurity-framework-csf-20/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mapping the IR program to the CSF 2.0 profile (SP 800-61r3)

SP 800-61r3 (April 2025) drops the old four-phase lifecycle as the organising model and instead presents incident response as a **CSF 2.0 Community Profile**: every CSF function contributes. Preparation lives in Govern/Identify/Protect, handling lives in Detect/Respond/Recover, and improvement (ID.IM) runs across all of them.

## How the profile is laid out
For each CSF subcategory 800-61r3 gives a priority (High / Medium / Low for IR) and IR-specific considerations. Examples worth anchoring on:
| Function | Subcategories IR owners usually own | Evidence you should be able to show |
|---|---|---|
| Govern | GV.RR (roles), GV.PO (policy), GV.SC (supplier IR duties) | Approved IR policy, RACI, contract IR clauses |
| Identify | ID.AM (assets), ID.RA (risk), ID.IM (improvement) | Crown-jewel list, lessons-learned tracker |
| Protect | PR.PS-04 (log generation), PR.DS-11 (backups) | Logging baseline, tested immutable backups |
| Detect | DE.CM (monitoring), DE.AE (adverse event analysis, incl. declaration criteria) | Alert triage SOP, declaration thresholds |
| Respond | RS.MA, RS.AN, RS.CO, RS.MI | Playbooks, forensic procedure, comms plan, containment authority |
| Recover | RC.RP, RC.CO | Restore runbooks, recovery comms |

## Procedure
1. Export the profile table from 800-61r3 into a sheet: one row per subcategory, columns `priority`, `current state (0-4)`, `evidence link`, `owner`, `target`, `gap action`.
2. Score current state from evidence, not interviews: a policy that exists but was never exercised scores no higher than "partial".
3. Set the target profile using the 800-61r3 priority plus your risk register; not every Low needs closing.
4. Gap actions become tracked items with owners and dates; High-priority Respond/Recover gaps go first.
5. Re-score after every major incident and each tabletop; feed ID.IM.

## Gotchas
- Do not relabel the old Preparation/Detection/Containment/Post-incident plan sections and call it done; auditors now expect outcome language tied to CSF IDs.
- Many High items sit outside the SOC (backups, asset inventory, supplier contracts). Name non-security owners explicitly.
- Keep the old lifecycle in playbooks where it helps responders; the profile is a program-management view.

## Verify
Every High-priority subcategory has an owner, an evidence link that a third party could open, and either a current score at target or a dated gap action.
