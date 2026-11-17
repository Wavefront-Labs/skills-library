---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.identifying-the-problem-before-touching-anything
name: identifying-the-problem-before-touching-anything
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, troubleshooting, identify-the-problem, questioning-techniques, recent-changes, backup-before-changes, policy-check, comptia-a-plus]
level: intro
status: draft
description: "CompTIA step 1 done properly: gather information from the user and the system, ask about recent changes, duplicate the problem, check policy, and back up before making changes."
sources:
  - "https://www.comptia.org/certifications/a"
  - "https://www.thinkhdi.com/"
  - "https://grow.google/certificates/it-support/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# identifying-the-problem-before-touching-anything

Goal: know exactly what's wrong, for whom, since when and what changed —
before the first fix attempt (A+ 220-1201 5.1, step 1: identify the problem).

## The A+ sub-steps
1. **Gather information from the user** and from logs/monitoring.
2. **Identify user changes to the computer** (new software, updates,
   moved desk, new peripheral, password change) — and changes IT made
   (check change calendar, recent deployments).
3. **Perform backups before making changes** if data could be at risk
   (OneDrive sync status, copy local files, restore point).
4. **Inquire regarding environmental or infrastructure changes** (power
   work, network maintenance, office move).
5. **Duplicate the problem** if possible.
6. Approach multiple problems individually.
7. Check corporate policies/procedures before making changes (is this
   allowed? is there a standard fix?).

## Questioning technique
- Start **open**: "Tell me what happens when you try to…", "What were you
  doing when it started?"
- Narrow with **closed** questions: "Does it happen on Wi-Fi and wired?",
  "Did it work yesterday?", "Anyone else near you affected?"
- The magic questions: **What changed? When did it last work? Who else is
  affected? Can you show me?**
- Paraphrase back: "So since this morning, only on your laptop, Outlook
  closes when you open the Finance calendar — right?"

## Gather from the system, not just the user
Event logs, monitoring alerts, service health, Intune device status, recent
tickets from the same user/device, known errors. Users report the symptom
they noticed, not necessarily the first one.

## Scope it
One user / one device / one site / everyone? Scope decides priority and
direction (device vs service).

## Gotchas
- Fixing before understanding destroys evidence (reboots clear state,
  reinstalls remove logs).
- Users minimise their changes ("I didn't install anything" — the browser
  extension doesn't count in their mind); ask specifically.
- Multiple reported issues: separate tickets, one at a time.

## Verify
Ticket shows symptom, scope, start time, recent changes and a reproduced
or observed failure before any fix steps are logged.
