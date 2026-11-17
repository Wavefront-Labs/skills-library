---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.kepner-tregoe-is-is-not-analysis
name: kepner-tregoe-is-is-not-analysis
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, kepner-tregoe, problem-analysis, is-is-not, root-cause-analysis, problem-management]
level: practitioner
status: draft
description: "Apply Kepner-Tregoe problem analysis to IT faults: specify What/Where/When/Extent as IS and IS NOT, extract distinctions and changes, then test causes against the spec."
sources:
  - "https://kepner-tregoe.com/training/problem-solving-decision-making/"
  - "https://www.axelos.com/certifications/itil-service-management/itil-4-practice-manager"
  - "https://www.comptia.org/en/certifications/a/core-1-v15/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# kepner-tregoe-is-is-not-analysis

Use it when a fault has resisted quick fixes, many people have theories, or a problem
record needs a defensible cause.

## 1. State the deviation
One object, one defect: "Outlook on finance laptops freezes when opening attachments",
not "email is slow".

## 2. Specify IS / IS NOT
| Dimension | IS | IS NOT (could be, but is not) | Distinction |
|---|---|---|---|
| What object | Outlook desktop on finance laptops | Outlook on the web, Outlook on HR laptops | Finance image has PDF add-in X |
| What defect | Freezes 30-60 s on attachment open | Crash, error message | |
| Where (geography) | Head office and home | — | Location not relevant |
| Where (on object) | PDF and Excel attachments | Plain text, images | Preview handlers |
| When (first) | Since Tuesday 14 Oct | Before 14 Oct | |
| When (pattern) | Every time | Intermittent | |
| Extent | 40 of 45 finance users | Other departments | 5 unaffected were on leave |

The IS NOT column is the power: it rules causes out.

## 3. Distinctions and changes
For each distinction, ask what changed in or around it near the "first seen" date
(update rings, add-in version, policy changes; see correlating-faults-with-recent-changes).

## 4. Possible causes, then test against the spec
Each cause must explain every IS and every IS NOT. "Network latency" fails (OWA works,
HR unaffected). "PDF add-in update pushed 13 Oct to finance ring" explains all rows.

## 5. Verify the true cause
Prove it cheaply and reversibly: disable the add-in for two users; confirm the freeze
stops; then roll back for all and close the problem with evidence.

## Gotchas
- Vague specs ("some users", "sometimes") produce useless analysis; get numbers.
- Do not skip IS NOT because it feels obvious; that is where assumptions hide.

## Verify
The written spec, the cause that survives every row, and a test result that confirms it
are attached to the problem record.
