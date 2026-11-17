---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.verifying-full-functionality-and-preventive-measures
name: verifying-full-functionality-and-preventive-measures
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, troubleshooting, verify-full-functionality, preventive-measures, document-findings, user-acceptance, regression-check, comptia-a-plus]
level: intro
status: draft
description: "CompTIA steps 5-6: verify the whole system works for the user (not just the symptom), apply preventive measures, then document findings, actions and outcomes."
sources:
  - "https://www.comptia.org/certifications/a"
  - "https://www.thinkhdi.com/"
  - "https://library.serviceinnovation.org/KCS/KCS_v6/KCS_v6_Practices_Guide"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# verifying-full-functionality-and-preventive-measures

Goal: the user can do their whole job again, the fault is less likely to
come back, and the next technician can learn from what happened (A+
220-1201 5.1 steps 5 and 6).

## Step 5: verify full system functionality
- Test the **original failing action** with the user, in their normal
  context (their account, their network, not just your admin session).
- Check **related functions** the fix might have affected: reinstalling
  Office → Outlook profile, Teams add-in, default apps; driver change →
  sleep/resume, external displays; network reset → VPN, Wi-Fi profiles.
- Reboot test where relevant (some fixes don't survive a restart).
- Get **user confirmation**; for intermittent issues agree a monitoring
  period and follow-up date.

## Preventive measures (also step 5)
- Same fault on other devices? (model-wide driver, fleet setting) → raise a
  problem or proactive fix.
- User behaviour → brief coaching or KB link, without blame.
- Monitoring/alerting so it's caught earlier next time (disk space alert,
  certificate expiry reminder).
- Update baseline/standard build if the gap was there.

## Step 6: document findings, actions and outcomes
- Ticket: cause, fix, verification, preventive actions (see resolution
  notes skill).
- Knowledge: create or improve the KB article.
- CMDB/asset: hardware replaced, configuration changed.
- Lessons for the team if novel (team chat, huddle).

## Gotchas
- "Works for me" in an admin session misses permission-related failures.
- Closing intermittent issues after one success leads to reopens — agree a
  watch period.

## Verify
User confirms, related functions checked and noted, preventive action
recorded (or explicitly "none needed"), and the ticket/KB updated.
