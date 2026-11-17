---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.ishikawa-fault-tree-and-one-change-at-a-time
name: ishikawa-fault-tree-and-one-change-at-a-time
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, ishikawa, fault-tree-analysis, one-change-at-a-time, fishbone-diagram, root-cause-analysis, controlled-testing]
level: practitioner
status: draft
description: "Use Ishikawa fishbone diagrams and fault tree analysis to structure root cause work, and test fixes one change at a time so you know what actually fixed the problem."
sources:
  - "https://asq.org/quality-resources/fishbone"
  - "https://www.nrc.gov/docs/ML1007/ML100780465.pdf"
  - "https://www.comptia.org/en/certifications/a/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ishikawa-fault-tree-and-one-change-at-a-time

## Ishikawa (fishbone) diagram
Use in a group when causes are unclear and many teams are involved.
1. Write the problem (effect) at the head: specific and measurable ("Logon takes over
   3 minutes for 40% of Site B users since 3 March").
2. Draw bones for cause categories. For IT, adapt the classic 6 Ms:
   People, Process, Technology/Hardware, Software/Configuration, Network/Environment,
   Suppliers/Data.
3. Brainstorm causes onto each bone; ask "why?" on each cause to add sub-causes (combine
   with 5 Whys).
4. Mark causes with evidence vs speculation; plan tests for the likely ones.
- Its value is breadth: it stops a team fixating on "it's the network".

## Fault tree analysis (FTA)
Top-down, logical: start with the undesired event and decompose with AND/OR gates.
```
                [Users can't print at Site B]
                         OR
     +-------------------+--------------------+
 [Print server down] [Queue/driver fault] [Network path down]
                                               AND
                                  +------------+-----------+
                             [Primary link down] [Backup link down]
```
- OR gate: any child causes the parent. AND gate: all children are needed.
- Useful to find single points of failure (OR gates directly under the top event) and
  to show that redundancy works (AND gates).
- Assign rough likelihoods to prioritise testing; check the most likely, cheapest-to-test
  branches first.

## One change at a time
- Change one variable, test, record the result, then decide the next change. If you
  change the driver, the BIOS and the cable together and it works, you don't know which
  fixed it and can't write the KB or problem record.
- Revert changes that made no difference (unless they're harmless improvements, which
  you note), so you don't leave a trail of unexplained modifications.
- Keep a change log in the ticket: time, change, result.
- Exception: in a major incident, restore service first (several changes may be needed);
  then reproduce in test one change at a time to find the true cause.

## Verify
The RCA shows the method used and evidence for the chosen cause; the ticket's change
log identifies the single change that resolved the issue.
